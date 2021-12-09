import * as AWS from 'aws-sdk';
import { hackTheMachineUnmannedTrack3 as outputs } from '../../cdk.outputs.json';
import { algorithmName, region } from './settings';

const sagemaker = new AWS.SageMaker({ region });

const createOptions: AWS.SageMaker.CreateAlgorithmInput = {
  AlgorithmDescription: 'HACKtheMACHINE: Unmanned Track 3 reinforcement learning algorithm with neural-mmo.',
  AlgorithmName: algorithmName,
  CertifyForMarketplace: false,
  TrainingSpecification: {
    // MetricDefinitions: [
    //   {
    //     Name: 'policy_reward_mean',
    //     Regex: 'policy_reward_mean = (.*?);',
    //   },
    // ],
    SupportsDistributedTraining: false,
    SupportedHyperParameters: [
      // Set all hyperparameters to `isTunable=false` until we can parse metrics from stdout.
      {
        Description: 'The number of iterations between each checkpoint save.',
        IsRequired: false,
        IsTunable: false,
        Name: 'checkpoint-save-frequency',
        Type: 'Integer',
      },
      {
        Description: 'The name of the configuration file to use.',
        IsRequired: false,
        IsTunable: false,
        Name: 'config-file-name',
        Type: 'FreeText',
      },
      {
        Description: 'The default ratio of training workers to evaluation workers. Used to set default values for `training-worker-count` and `evaluation-worker-count`.',
        IsRequired: false,
        IsTunable: false,
        Name: 'default-worker-ratio',
        Type: 'Continuous',
      },
      {
        Description: 'The embedding layer size.',
        IsRequired: false,
        IsTunable: false,
        // IsTunable: true,
        Name: 'embedding-layer-size',
        Range: {
          IntegerParameterRangeSpecification: {
            MaxValue: '1024',
            MinValue: '0',
          }
        },
        Type: 'Integer',
      },
      {
        Description: 'The number of time steps an evaluating agent looks in the future to maximize their reward.',
        IsRequired: false,
        IsTunable: false,
        // IsTunable: true,
        Name: 'evaluation-horizon',
        Range: {
          IntegerParameterRangeSpecification: {
            MaxValue: '16384',
            MinValue: '0',
          }
        },
        Type: 'Integer',
      },
      {
        Description: 'The number of rollout worker actors dedicated to evaluation.',
        IsRequired: false,
        IsTunable: false,
        Name: 'evaluation-worker-count',
        Range: {
          IntegerParameterRangeSpecification: {
            MaxValue: '128',
            MinValue: '1'
          }
        },
        Type: 'Integer'
      },
      {
        Description: 'The number of total GPUs to allocate.',
        IsRequired: false,
        IsTunable: false,
        Name: 'gpu-count',
        Range: {
          IntegerParameterRangeSpecification: {
            MaxValue: '32',
            MinValue: '0'
          }
        },
        Type: 'Integer'
      },
      {
        Description: 'The number of GPUs to allocate each worker.',
        IsRequired: false,
        IsTunable: false,
        Name: 'gpu-count-per-worker',
        Range: {
          'ContinuousParameterRangeSpecification': {
            MaxValue: '32',
            MinValue: '0'
          }
        },
        Type: 'Continuous'
      },
      {
        Description: 'The hidden layer size.',
        IsRequired: false,
        IsTunable: false,
        // IsTunable: true,
        Name: 'hidden-layer-size',
        Range: {
          IntegerParameterRangeSpecification: {
            MaxValue: '1024',
            MinValue: '0',
          }
        },
        Type: 'Integer',
      },
      {
        Description: 'The LSTM’s sequence length or horizon.',
        IsRequired: false,
        IsTunable: false,
        // IsTunable: true,
        Name: 'lstm-horizon',
        Range: {
          IntegerParameterRangeSpecification: {
            MaxValue: '512',
            MinValue: '1'
          }
        },
        Type: 'Integer'
      },
      {
        Description: 'The maximum number of checkpoints saved.',
        IsRequired: false,
        IsTunable: false,
        Name: 'max-checkpoints-saved',
        Type: 'Integer',
      },
      {
        Description: 'The rollout fragment length divides episodes into fragments.',
        IsRequired: false,
        IsTunable: false,
        // IsTunable: true,
        Name: 'rollout-fragment-length',
        Range: {
          IntegerParameterRangeSpecification: {
            MaxValue: '4096',
            MinValue: '1'
          }
        },
        Type: 'Integer'
      },
      {
        Description: 'The minibatch size iterated on by each rollout worker. Note: The effective minibatch size is `training_worker_count * sgd_minibatch_size`.',
        IsRequired: false,
        IsTunable: false,
        Name: 'sgd-minibatch-size',
        Range: {
          IntegerParameterRangeSpecification: {
            MaxValue: '4096',
            MinValue: '1'
          }
        },
        Type: 'Integer'
      },
      {
        Description: 'The training batch size is divided by `rollout_fragment_length` to determine the number of steps in each epoch.',
        IsRequired: false,
        IsTunable: false,
        Name: 'training-batch-size',
        Range: {
          IntegerParameterRangeSpecification: {
            MaxValue: '4194304',
            MinValue: '1'
          }
        },
        Type: 'Integer'
      },
      {
        Description: 'The number of time steps a training agent looks in the future to maximize their reward.',
        IsRequired: false,
        IsTunable: false,
        // IsTunable: true,
        Name: 'training-horizon',
        Range: {
          IntegerParameterRangeSpecification: {
            MaxValue: '16384',
            MinValue: '0'
          }
        },
        Type: 'Integer'
      },
      {
        Description: 'The number of total training iterations.',
        IsRequired: false,
        IsTunable: false,
        // IsTunable: true,
        Name: 'training-iteration-count',
        Range: {
          IntegerParameterRangeSpecification: {
            MaxValue: '100000',
            MinValue: '1'
          }
        },
        Type: 'Integer'
      },
      {
        Description: 'The number of rollout worker actors dedicated to training.',
        IsRequired: false,
        IsTunable: false,
        Name: 'training-worker-count',
        Range: {
          IntegerParameterRangeSpecification: {
            MaxValue: '256',
            MinValue: '1'
          }
        },
        Type: 'Integer'
      },
      {
        Description: 'The verbosity mode of model training logs.',
        IsRequired: false,
        IsTunable: false,
        Name: 'training-verbosity',
        Range: {
          IntegerParameterRangeSpecification: {
            MaxValue: '3',
            MinValue: '0'
          }
        },
        Type: 'Integer'
      },
      {
        Description: 'The API key used to send logs to WandB.',
        IsRequired: true,
        IsTunable: false,
        Name: 'wandb-api-key',
        Type: 'FreeText',
      }
    ],
    SupportedTrainingInstanceTypes: [
      'ml.c4.2xlarge',
      'ml.c4.4xlarge',
      'ml.c4.8xlarge',
      'ml.c4.xlarge',
      'ml.c5.18xlarge',
      'ml.c5.2xlarge',
      'ml.c5.4xlarge',
      'ml.c5.9xlarge',
      'ml.g4dn.12xlarge',
      'ml.g4dn.16xlarge',
      'ml.g4dn.2xlarge',
      'ml.g4dn.4xlarge',
      'ml.g4dn.8xlarge',
      'ml.g4dn.xlarge',
      'ml.m4.10xlarge',
      'ml.m4.16xlarge',
      'ml.m4.2xlarge',
      'ml.m4.4xlarge',
      'ml.m4.xlarge',
      'ml.m5.2xlarge',
      'ml.m5.4xlarge',
      'ml.m5.large',
      'ml.m5.xlarge',
      'ml.p2.16xlarge',
      'ml.p2.8xlarge',
      'ml.p2.xlarge',
      'ml.p3.16xlarge',
      'ml.p3.2xlarge',
      'ml.p3.8xlarge',
    ],
    SupportedTuningJobObjectiveMetrics: [
      {
        MetricName: 'policy_reward_mean',
        Type: 'Maximize',
      },
    ],
    TrainingChannels: [{
      Description: 'Environmental data (maps, weather, etc.) used to simulate the environment.',
      IsRequired: true,
      Name: 'environment',
      SupportedContentTypes: [],
      SupportedInputModes: ['File'],
    }],
    TrainingImage: outputs.sagemakerAlgorithmDockerImageUri,
  },
};

const run = async () => {
  try {
    console.log('Removing old algorithm…'); // eslint-disable-line no-console
    await sagemaker.deleteAlgorithm({ AlgorithmName: algorithmName }).promise();
    console.log('Removed old algorithm');
  } catch (error) {
    console.error(error);
    console.log('No algorithm to remove');
  }

  console.log('Adding new algorithm…'); // eslint-disable-line no-console

  try {
    const data = await sagemaker.createAlgorithm(createOptions).promise();
    console.log('Added new algorithm:', JSON.stringify(data, null, 2)); // eslint-disable-line no-console
  } catch (error) {
    console.error(error); // eslint-disable-line no-console
  }
};

run();
