import * as AWS from 'aws-sdk';

const sagemaker = new AWS.SageMaker({
  region: 'us-east-1',
});

const options: AWS.SageMaker.DescribeAlgorithmInput = {
  AlgorithmName: 'example-hackthemachine-unmanned-track-3-neural-mmo-v2',
};

sagemaker.describeAlgorithm(options, (error, data) => {
  if (error) {
    console.error(error, error.stack);
  } else {
    console.log(data);
  }
});