import argparse
from sagemaker.estimator import Estimator
import sagemaker_job


def main():
    arg_parser = argparse.ArgumentParser()
    sagemaker_job.add_args_to_parser(arg_parser)

    arg_parser.add_argument(
        '--role-arn',
        help='Role ARN assumed during training.',
        required=True,
        type=str
    )

    args = arg_parser.parse_args()

    estimator = Estimator(
        hyperparameters=vars(args),
        image_uri='algorithm-neural-mmo',
        role=args.role_arn,
        train_instance_count=1,
        train_instance_type='local'
    )

    estimator.fit()
    predictor = estimator.deploy(1, 'local')

if __name__ == '__main__':
    main()