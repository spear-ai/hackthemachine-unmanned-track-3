import argparse
import Forge


def add_args_to_parser(parser):
    parser.add_argument(
        '--config-file-name',
        default='EastPacificOcean',
        help='The name of the configuration file to use.',
        type=str
    )

    parser.add_argument(
        '--embedding-layer-size',
        default=argparse.SUPPRESS,
        help='The embedding layer size.',
        type=int
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
        default=argparse.SUPPRESS,
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

    if 'embedding_layer_size' in args:
        anvil.config.EMBED = args.embedding_layer_size

    if 'evaluation_horizon' in args:
        anvil.config.EVALUATION_HORIZON = args.evaluation_horizon

    if 'evaluation_worker_count' in args:
        anvil.config.EVALUATION_NUM_WORKERS = args.evaluation_worker_count

    if 'gpu_count' in args:
        anvil.config.GPUS = args.gpu_count

    if 'hidden_layer_size' in args:
        anvil.config.HIDDEN = args.hidden_layer_size

    if 'gpu_count_per_worker' in args:
        anvil.config.NUM_GPUS_PER_WORKER = args.gpu_count_per_worker

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

    if 'training_worker_count' in args:
        anvil.config.NUM_WORKERS = args.cpu_worker_count

    if 'wandb_api_key' in args:
        anvil.config.WANDB_API_KEY = args.wandb_api_key

    # Assume this is a training job
    anvil.train()


if __name__ == '__main__':
    main()
