import argparse
import os
import Forge
import torch


def add_args_to_parser(parser):
    parser.add_argument(
        '--checkpoint-save-frequency',
        default=argparse.SUPPRESS,
        help='The number of iterations between each checkpoint save.',
        type=int
    )

    parser.add_argument(
        '--config-file-name',
        default='EastPacificOcean',
        help='The name of the configuration file to use.',
        type=str
    )

    parser.add_argument(
        '--default-worker-ratio',
        default=15/3,
        help='The default ratio of training workers to evaluation workers. Used to set default values for `training-worker-count` and `evaluation-worker-count`.',
        type=float
    )

    parser.add_argument(
        '--embedding-layer-size',
        default=argparse.SUPPRESS,
        help='The embedding layer size.',
        type=int
    )

    parser.add_argument(
        '--environment-data-file-path',
        default=os.getenv('SM_CHANNEL_ENVIRONMENT', argparse.SUPPRESS),
        help='The file path to environment data',
        type=str
    )

    parser.add_argument(
        '--evaluation-horizon',
        default=argparse.SUPPRESS,
        help='The number of time steps an evaluating agent looks in the future to maximize their reward.',
        type=int
    )

    parser.add_argument(
        '--evaluation-worker-count',
        default=argparse.SUPPRESS,
        help='The number of rollout worker actors dedicated to evaluation.',
        type=int
    )

    parser.add_argument(
        '--gpu-count',
        default=int(os.getenv('SM_GPU_COUNT', torch.cuda.device_count())),
        help='',
        type=int
    )

    parser.add_argument(
        '--gpu-count-per-worker',
        default=argparse.SUPPRESS,
        help='The number of GPUs to allocate each rollout worker actor.',
        type=int
    )

    parser.add_argument(
        '--hidden-layer-size',
        default=argparse.SUPPRESS,
        help='The hidden layer size.',
        type=int
    )

    parser.add_argument(
        '--lstm-horizon',
        default=argparse.SUPPRESS,
        help='The LSTM’s sequence length or horizon.',
        type=int,
    )

    parser.add_argument(
        '--max-checkpoints-saved-count',
        default=10,
        help='The maximum number of checkpoints saved.',
        type=int
    )

    parser.add_argument(
        '--rollout-fragment-length',
        default=argparse.SUPPRESS,
        help='The rollout fragment length divides episodes into fragments.',
        type=int
    )

    parser.add_argument(
        '--sgd-minibatch-size',
        default=argparse.SUPPRESS,
        help='The minibatch size iterated on by each rollout worker. Note: The effective minibatch size is `training_worker_count * sgd_minibatch_size`.',
        type=int
    )

    parser.add_argument(
        '--training-batch-size',
        default=argparse.SUPPRESS,
        help='The training batch size is divided by `rollout_fragment_length` to determine the number of steps in each epoch.',
        type=int
    )

    parser.add_argument(
        '--training-horizon',
        default=argparse.SUPPRESS,
        help='The number of time steps a training agent looks in the future to maximize their reward.',
        type=int
    )

    parser.add_argument(
        '--training-iteration-count',
        default=argparse.SUPPRESS,
        help='The number of total training iterations.',
        type=int
    )

    parser.add_argument(
        '--training-worker-count',
        default=argparse.SUPPRESS,
        help='The number of rollout worker actors dedicated to training.',
        type=int
    )

    parser.add_argument(
        '--training-verbosity',
        default=3,
        help='The verbosity mode of model training logs.',
        type=int
    )

    parser.add_argument(
        '--wandb-api-key',
        default=argparse.SUPPRESS,
        help='The API key used to send logs to WandB.',
        required=True,
        type=str
    )


def main():
    arg_parser = argparse.ArgumentParser()
    add_args_to_parser(arg_parser)
    args = arg_parser.parse_args()
    anvil = Forge.Anvil(config=args.config_file_name)
    cpu_count = int(os.getenv('SM_NUM_CPUS', os.cpu_count()))

    if 'checkpoint_save_frequency' in args:
        anvil.config.CHECKPOINT_FREQ = args.checkpoint_save_frequency

    if 'embedding_layer_size' in args:
        anvil.config.EMBED = args.embedding_layer_size

    if 'environment_data_file_path' in args:
        anvil.config.PATH_ENVIRONMENT_GENERATED = args.environment_data_file_path

    if 'evaluation_horizon' in args:
        anvil.config.EVALUATION_HORIZON = args.evaluation_horizon

    if 'gpu_count' in args:
        anvil.config.NUM_GPUS = args.gpu_count

    if 'hidden_layer_size' in args:
        anvil.config.HIDDEN = args.hidden_layer_size

    if 'gpu_count_per_worker' in args:
        anvil.config.NUM_GPUS_PER_WORKER = args.gpu_count_per_worker

    if 'lstm_horizon' in args:
        anvil.config.LSTM_BPTT_HORIZON = args.lstm_horizon

    if 'max_checkpoints_saved_count' in args:
        anvil.config.KEEP_CHECKPOINTS_NUM = args.max_checkpoints_saved_count

    if 'rollout_fragment_length' in args:
        anvil.config.ROLLOUT_FRAGMENT_LENGTH = args.rollout_fragment_length

    if 'sgd_minibatch_size' in args:
        anvil.config.SGD_MINIBATCH_SIZE = args.sgd_minibatch_size

    if 'training_bath_size' in args:
        anvil.config.TRAIN_BATCH_SIZE = args.training_batch_size

    if 'training_horizon' in args:
        anvil.config.TRAIN_HORIZON = args.training_horizon

    if 'training_iteration_count' in args:
        anvil.config.TRAINING_ITERATIONS = args.training_iteration_count

    if 'training_verbosity' in args:
        anvil.config.LOG_LEVEL = args.training_verbosity

    if 'wandb_api_key' in args:
        anvil.config.WANDB_API_KEY = args.wandb_api_key

    if 'SM_MODEL_DIR' in os.environ:
        anvil.config.EXPERIMENT_DIR = os.environ['SM_MODEL_DIR']

    # Default `checkpoint_save_frequency` to a value that
    # preserves the model's training history
    if 'checkpoint_save_frequency' not in args:
        args.checkpoint_save_frequency = int(
            anvil.config.TRAINING_ITERATIONS // (
                args.max_checkpoints_saved_count or anvil.config.TRAINING_ITERATIONS
            )
        )

    anvil.config.CHECKPOINT_FREQ = args.checkpoint_save_frequency

    # The first CPU is allocated to the driver process
    worker_cpu_count = cpu_count - 1

    # Default `evaluation_worker_count` to `worker_ratio * cpu_count)`.
    if 'evaluation_worker_count' not in args:
        args.evaluation_worker_count = 1 + int(
            worker_cpu_count // args.default_worker_ratio
        )

    # Default `training_worker_count` to the remaining cpus.
    if 'training_worker_count' not in args:
        args.training_worker_count = max(
            worker_cpu_count - args.evaluation_worker_count, 1
        )

    anvil.config.EVALUATION_NUM_WORKERS = args.evaluation_worker_count
    anvil.config.NUM_WORKERS = args.training_worker_count

    # Print arguments
    print('args:')
    for key, value in vars(args).items():
        print(f'  {key}: {value}')

    # Print config file properties
    print('config:')
    for key, value in vars(anvil.config).items():
        if not key.startswith('_'):
            if not callable(value):
                print(f'  {key}: {value}')

    # Assume this is a training job
    anvil.train()


if __name__ == '__main__':
    main()
