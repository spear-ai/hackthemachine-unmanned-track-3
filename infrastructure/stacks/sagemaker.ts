import * as cdk from '@aws-cdk/core';
import * as cdkIam from '@aws-cdk/aws-iam';
import * as cdkSagemaker from '@aws-cdk/aws-sagemaker';
import * as cdkS3 from '@aws-cdk/aws-s3';

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

    new cdkSagemaker.CfnNotebookInstance(this, 'sagemakerNotebookInstance', {
      // acceleratorTypes: undefined,
      additionalCodeRepositories: ['https://github.com/spear-ai/hackthemachine-unmanned-track-3'],
      defaultCodeRepository: 'https://github.com/aws/sagemaker-rl-container.git',
      // directInternetAccess: undefined,
      instanceType: 'ml.t2.medium',
      // lifecycleConfigName: undefined,
      notebookInstanceName: 'DevNotebook',
      // platformIdentifier: undefined,
      roleArn: sagemakerIamRole.roleArn,
      // rootAccess: undefined,
      // subnetId: undefined,
      // volumeSizeInGb: undefined,
    });
  }
}
