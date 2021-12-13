import * as cdk from '@aws-cdk/core';
import * as cdkEcr from '@aws-cdk/aws-ecr';
import * as cdkEcrAssets from '@aws-cdk/aws-ecr-assets';
import * as cdkIam from '@aws-cdk/aws-iam';
import * as cdkS3 from '@aws-cdk/aws-s3';
import * as cdkS3Deployment from '@aws-cdk/aws-s3-deployment';
import * as cdkEcrDeployment from 'cdk-ecr-deployment';
import path from 'path';

export interface SagemakerStackProperties extends cdk.StackProps {
  env: cdk.StackProps['env'] & {
    isSandbox: boolean;
  };
};

export class SagemakerStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, properties: SagemakerStackProperties) {
    super(scope, id, properties);

    const { isSandbox } = properties.env;

    const sagemakerIamRole = new cdkIam.Role(this, 'sagemakerIamRole', {
      assumedBy: new cdkIam.ServicePrincipal('sagemaker.amazonaws.com'),
      managedPolicies: [
        cdkIam.ManagedPolicy.fromAwsManagedPolicyName('AmazonSageMakerFullAccess'),
      ],
    });

    const environmentDataS3Bucket = new cdkS3.Bucket(this, 'environmentDataS3Bucket', {
      autoDeleteObjects: isSandbox,
      removalPolicy: isSandbox ? cdk.RemovalPolicy.DESTROY : cdk.RemovalPolicy.RETAIN,
      versioned: true,
    });

    new cdkS3Deployment.BucketDeployment(this, 'environmentDataS3Files', {
      destinationBucket: environmentDataS3Bucket,
      sources: [cdkS3Deployment.Source.asset(path.join(__dirname, '../../model/environment/generated'))],
    });

    environmentDataS3Bucket.grantReadWrite(sagemakerIamRole);

    const modelS3Bucket = new cdkS3.Bucket(this, 'modelS3Bucket', {
      autoDeleteObjects: isSandbox,
      removalPolicy: isSandbox ? cdk.RemovalPolicy.DESTROY : cdk.RemovalPolicy.RETAIN,
      versioned: true,
    });

    modelS3Bucket.grantReadWrite(sagemakerIamRole);

    const sagemakerAlgorithmDockerImage = new cdkEcrAssets.DockerImageAsset(this, 'sagemakerAlgorithmDockerImage', {
      directory: path.join(__dirname, '../..'),
      file: 'Dockerfile.sagemaker.neural-mmo',
    });

    const sagemakerEcrRepository = new cdkEcr.Repository(this, 'sagemakerEcrRepository');

    new cdkEcrDeployment.ECRDeployment(this, 'sagemakerAlgorithmDockerImageDeployment', {
      dest: new cdkEcrDeployment.DockerImageName(
        `${sagemakerEcrRepository.repositoryUri}:algorithm-neural-mmo`,
      ),
      src: new cdkEcrDeployment.DockerImageName(
        sagemakerAlgorithmDockerImage.imageUri,
      ),
    });

    new cdk.CfnOutput(this, 'environmentDataS3Path', {
      description: 'Environmental data S3 Bucket URL',
      value: `${environmentDataS3Bucket.s3UrlForObject()}`,
    });

    new cdk.CfnOutput(this, 'modelCheckpointsS3Path', {
      description: 'Model checkpoints S3 Bucket URL',
      value: `${modelS3Bucket.s3UrlForObject('checkpoints')}`,
    });

    new cdk.CfnOutput(this, 'modelOutputS3Path', {
      description: 'Model output S3 Bucket URL',
      value: `${modelS3Bucket.s3UrlForObject('output')}`,
    });

    new cdk.CfnOutput(this, 'sagemakerAlgorithmDockerImageUri', {
      description: 'Neural MMO Sagemaker algorithm Docker Image URI',
      value: `${sagemakerEcrRepository.repositoryUri}:algorithm-neural-mmo`,
    });
  }
}
