import * as cdk from '@aws-cdk/core';
import * as cdkEc2 from '@aws-cdk/aws-ec2';
import * as cdkIam from '@aws-cdk/aws-iam';
import * as cdkS3 from '@aws-cdk/aws-s3';
import * as cdkSagemaker from '@aws-cdk/aws-sagemaker';
import * as cdkStepfunctions from '@aws-cdk/aws-stepfunctions';
import * as cdkStepfunctionsTasks from '@aws-cdk/aws-stepfunctions-tasks';

export interface SagemakerStackProperties extends cdk.StackProps {
  env: cdk.StackProps['env'] & {
    isSandbox: boolean;
  };
};

export class SagemakerStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, properties: SagemakerStackProperties) {
    super(scope, id, properties);

    const { isSandbox } = properties.env;

    const sagemakerS3Bucket = new cdkS3.Bucket(this, 'sagemakerS3Bucket', {
      autoDeleteObjects: isSandbox,
      removalPolicy: isSandbox ? cdk.RemovalPolicy.DESTROY : cdk.RemovalPolicy.RETAIN,
      versioned: true,
    });

    const sagemakerIamRole = new cdkIam.Role(this, 'sagemakerIamRole', {
      assumedBy: new cdkIam.ServicePrincipal('sagemaker.amazonaws.com'),
      managedPolicies: [
        cdkIam.ManagedPolicy.fromAwsManagedPolicyName('AmazonSageMakerFullAccess'),
      ],
    });

    sagemakerS3Bucket.grantReadWrite(sagemakerIamRole);

    const sagemakerTrainingJob = new cdkStepfunctionsTasks.SageMakerCreateTrainingJob(
      this,
      'sagemakerTrainingJob',
      {
        algorithmSpecification: {
          algorithmName: 'example-hackthemachine-unmanned-track-3-neural-mmo-v2',
          trainingInputMode: cdkStepfunctionsTasks.InputMode.FILE,
        },
        inputDataConfig: [{
          channelName: 'environmental_data',
          dataSource: {
            s3DataSource: {
              s3DataType: cdkStepfunctionsTasks.S3DataType.S3_PREFIX,
              s3Location: cdkStepfunctionsTasks.S3Location.fromBucket(
                sagemakerS3Bucket,
                'environment/test',
              ),
            },
          },
        }],
        outputDataConfig: {
          s3OutputLocation: cdkStepfunctionsTasks.S3Location.fromBucket(
            sagemakerS3Bucket,
            'training-jobs',
          ),
        },
        resourceConfig: {
          instanceCount: 1,
          instanceType: new cdkEc2.InstanceType(
            // cdkStepfunctions.JsonPath.stringAt('$.instanceType'),
            'ml.m4.xlarge',
          ),
          volumeSize: cdk.Size.gibibytes(32),
        },
        stoppingCondition: {
          maxRuntime: cdk.Duration.minutes(10),
        },
        trainingJobName: cdkStepfunctions.JsonPath.stringAt(
          '$.trainingJobName',
          // 'hackthemachine-unmanned-track-3-neural-mmo-v2-1',
        ),
      },
    );

    new cdkStepfunctions.StateMachine(this, 'stateMachine', {
      definition: sagemakerTrainingJob,
      role: sagemakerIamRole,
    });
  }
}
