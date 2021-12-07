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

    new cdkS3Deployment.BucketDeployment(this, 'environmentDataS3Files', {
      destinationBucket: sagemakerS3Bucket,
      destinationKeyPrefix: 'environment',
      sources: [cdkS3Deployment.Source.asset(path.join(__dirname, '../../model/environment/generated'))],
    });

    const sagemakerAlgorithmDockerImage = new cdkEcrAssets.DockerImageAsset(this, 'sagemakerAlgorithmDockerImage', {
      directory: path.join(__dirname, '../..'),
      file: 'Dockerfile.sagemaker',
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

    new cdk.CfnOutput(this, 'sagemakerAlgorithmDockerImageUri', {
      description: 'Neural MMO Sagemaker algorithm Docker Image URI',
      value: `${sagemakerEcrRepository.repositoryUri}:algorithm-neural-mmo`,
    });
  }
}
