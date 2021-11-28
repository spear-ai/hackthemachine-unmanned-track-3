import * as AWS from 'aws-sdk';

const sagemaker = new AWS.SageMaker();

const options: AWS.SageMaker.CreateAlgorithmInput = {
  AlgorithmDescription: 'HACKtheMACHINE: Unmanned Track 3 reinforcement learning algorithm with neural-mmo.',
  AlgorithmName: 'hackthemachine-unmanned-track-3-neural-mmo-v3',
  CertifyForMarketplace: false,
  TrainingSpecification: {
    MetricDefinitions: [
      {
        Name: 'policy_reward_mean',
        Regex: 'policy_reward_mean = (.*?);',
      },
    ],
    SupportsDistributedTraining: false,
    SupportedHyperParameters: [
      {
        DefaultValue: '1024',
        Description: 'The number of time steps an agent looks into the future to maximize their reward during training.',
        IsRequired: false,
        IsTunable: true,
        Name: 'EVALUATION_HORIZON',
        Range: {
          IntegerParameterRangeSpecification: {
            MaxValue: '16384',
            MinValue: '0',
          }
        },
        Type: 'Integer',
      },
      {
        DefaultValue: '1',
        Description: 'The number of RLLib CPU workers to create during evaluation.',
        IsRequired: false,
        IsTunable: true,
        Name: 'EVALUATION_NUM_WORKERS',
        Range: {
          IntegerParameterRangeSpecification: {
            MaxValue: '128',
            MinValue: '1'
          }
        },
        Type: 'Integer'
      },
      {
        DefaultValue: '1024',
        Description: 'The number of time steps an agent looks into the future to maximize their reward during evaluation.',
        IsRequired: false,
        IsTunable: true,
        Name: 'HORIZON',
        Range: {
          IntegerParameterRangeSpecification: {
            MaxValue: '16384',
            MinValue: '0'
          }
        },
        Type: 'Integer'
      },
      {
        DefaultValue: '0',
        Description: 'The number of total GPUs to allocate.',
        IsRequired: false,
        IsTunable: true,
        Name: 'NUM_GPUS',
        Range: {
          IntegerParameterRangeSpecification: {
            MaxValue: '32',
            MinValue: '0'
          }
        },
        Type: 'Integer'
      },
      {
        DefaultValue: '0',
        Description: 'The number of GPUs to allocate each worker.',
        IsRequired: false,
        IsTunable: true,
        Name: 'NUM_GPUS_PER_WORKER',
        Range: {
          'ContinuousParameterRangeSpecification': {
            MaxValue: '32',
            MinValue: '0'
          }
        },
        Type: 'Continuous'
      },
      {
        DefaultValue: '1',
        Description: 'The number of RLLib CPU workers to create during training.',
        IsRequired: false,
        IsTunable: true,
        Name: 'NUM_WORKERS',
        Range: {
          IntegerParameterRangeSpecification: {
            MaxValue: '256',
            MinValue: '1'
          }
        },
        Type: 'Integer'
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
      'ml.m4.10xlarge',
      'ml.m4.16xlarge',
      'ml.m4.2xlarge',
      'ml.m4.4xlarge',
      'ml.m4.xlarge',
      'ml.m5.12large',
      'ml.m5.24large',
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
        Type: '',
      },
    ],
    TrainingChannels: [{
      Description: 'Environmental data (maps, assets, etc.) used to simulate the environment.',
      IsRequired: true,
      Name: 'environmental_data',
      SupportedContentTypes: null,
      SupportedInputModes: null,
    }],
    TrainingImage: '763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-training:1.8.1-gpu-py36-cu111-ubuntu18.04',
  },
};

sagemaker.createAlgorithm(options, (error, data) => {
  if (error) {
    console.error(error, error.stack);
  } else {
    console.log(data);
  }
});