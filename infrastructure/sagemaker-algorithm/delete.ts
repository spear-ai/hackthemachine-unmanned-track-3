import * as AWS from 'aws-sdk';
import { algorithmName, region } from './settings';

const sagemaker = new AWS.SageMaker({ region });

const options: AWS.SageMaker.DeleteAlgorithmInput = {
  AlgorithmName: algorithmName,
};

sagemaker.deleteAlgorithm(options, (error, data) => {
  if (error) {
    console.error(error, error.stack);
  } else {
    console.log(JSON.stringify(data, null, 2));
  }
});
