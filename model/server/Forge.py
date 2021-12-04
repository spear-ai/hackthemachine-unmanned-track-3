#!/usr/bin/env python

'''Main file for the neural-mmo/projekt demo

/projeckt contains all necessary RLlib wrappers to train and
evaluate capable policies on Neural MMO as well as rendering,
logging, and visualization tools.

Associated docs and tutorials are hosted on jsuarez5341.github.io.'''
from pdb import set_trace as T
from fire import Fire
from copy import deepcopy
import os
import numpy as np
import torch
import ray
from ray import rllib, tune
from ray.tune import CLIReporter
from ray.tune.integration.wandb import WandbLoggerCallback
from projekt import rllib_wrapper as wrapper
from projekt import config as base_config


class ConsoleLog(CLIReporter):
    def report(self, trials, done, *sys_info):
        os.system('cls' if os.name == 'nt' else 'clear')
        super().report(trials, done, *sys_info)


def run_tune_experiment(config):
    '''Ray[RLlib, Tune] integration for Neural MMO

    Setup custom environment, observations/actions, policies,
    and parallel training/evaluation'''

    ray.init(local_mode=config.LOCAL_MODE)

    # Obs and actions
    obs = wrapper.observationSpace(config)
    atns = wrapper.actionSpace(config)

    # Register custom env and policies
    ray.tune.registry.register_env(
        'HACKtheMACHINE',
        lambda config: wrapper.RLlibEnv(config)
    )

    rllib.models.ModelCatalog.register_custom_model(
        'godsword',
        wrapper.RLlibPolicy
    )

    def mapPolicy(agentID):
        return 'policy_{}'.format(agentID % config.NPOLICIES)

    policies = {}
    for i in range(config.NPOLICIES):
        params = {
            "agent_id": i,
            "obs_space_dict": obs,
            "act_space_dict": atns
        }
        key = mapPolicy(i)
        policies[key] = (None, obs, atns, params)

    # Evaluation config
    eval_config = deepcopy(config)
    eval_config.EVALUATE = True
    eval_config.AGENTS = eval_config.EVAL_AGENTS

    # Create rllib config
    rllib_config = {
        'callbacks': wrapper.RLlibLogCallbacks,
        'env': 'HACKtheMACHINE',
        'env_config': {
            'config': config
        },
        'evaluation_config': {
            'env_config': {
                'config': eval_config
            },
        },
        'evaluation_interval': config.EVALUATION_INTERVAL,
        'evaluation_num_episodes': config.EVALUATION_NUM_EPISODES,
        'evaluation_num_workers': config.EVALUATION_NUM_WORKERS,
        'evaluation_parallel_to_training': config.EVALUATION_PARALLEL,
        'framework': 'torch',
        'horizon': np.inf,
        'model': {
            'custom_model': 'godsword',
            'custom_model_config': {'config': config},
            'max_seq_len': config.LSTM_BPTT_HORIZON
        },
        'multiagent': {
            'count_steps_by': 'agent_steps',
            'policies': policies,
            'policy_mapping_fn': mapPolicy
        },
        'no_done_at_end': False,
        'num_envs_per_worker': 1,
        'num_gpus': config.NUM_GPUS,
        'num_gpus_per_worker': config.NUM_GPUS_PER_WORKER,
        'num_sgd_iter': config.NUM_SGD_ITER,
        'num_workers': config.NUM_WORKERS,
        'render_env': config.RENDER,
        'rollout_fragment_length': config.ROLLOUT_FRAGMENT_LENGTH,
        'sgd_minibatch_size': config.SGD_MINIBATCH_SIZE,
        'soft_horizon': False,
        'train_batch_size': config.TRAIN_BATCH_SIZE
    }

    tune.run(
        wrapper.RLlibTrainer,
        callbacks=[WandbLoggerCallback(
            api_key_file='.wandb_api_key',
            log_config=False,
            project='HACKtheMACHINE'
        )],
        checkpoint_at_end=True,
        checkpoint_freq=config.CHECKPOINT_FREQ,
        config=rllib_config,
        keep_checkpoints_num=config.KEEP_CHECKPOINTS_NUM,
        local_dir=os.path.normpath(os.path.join(
            __file__,
            '../experiments'
        )),
        name=config.__class__.__name__,
        progress_reporter=ConsoleLog(),
        restore=config.RESTORE,
        resume=config.RESUME,
        reuse_actors=True,
        stop={'training_iteration': config.TRAINING_ITERATIONS},
        trial_dirname_creator=lambda _: 'Run',
        verbose=config.LOG_LEVEL
    )


class Anvil():
    '''Neural MMO CLI powered by Google Fire

    Main file for the RLlib demo included with Neural MMO.

    Usage:
       python Forge.py <COMMAND> --config=<CONFIG> --ARG1=<ARG1> ...

    The User API documents core env flags. Additional config options specific
    to this demo are available in projekt/config.py.

    The --config flag may be used to load an entire group of options at once.
    Select one of the defaults from projekt/config.py or write your own.
    '''

    def __init__(self, **kwargs):
        # TODO: We should refactor this code to use Python Argparse instead
        if 'help' in kwargs:
            return

        assert 'config' in kwargs, 'Specify a config'
        config = kwargs.pop('config')
        config = getattr(base_config, config)()
        config.override(**kwargs)
        self.config = config

        # Round and round the num_threads flags go
        # Which are needed nobody knows!
        torch.set_num_threads(1)
        os.environ['MKL_NUM_THREADS'] = '1'
        os.environ['OMP_NUM_THREADS'] = '1'
        os.environ['NUMEXPR_NUM_THREADS'] = '1'

    def evaluate(self, **kwargs):
        '''Evaluate a model against EVAL_AGENTS models'''
        self.config.TRAINING_ITERATIONS = 0
        self.config.EVALUATE = True
        self.config.EVALUATION_NUM_WORKERS = self.config.NUM_WORKERS
        self.config.EVALUATION_NUM_EPISODES = self.config.NUM_WORKERS

        run_tune_experiment(self.config)

    def generate(self, **kwargs):
        '''Generate game maps for the current --config setting'''
        from neural_mmo.forge.blade.core import terrain
        terrain.MapGenerator(self.config).generate()

    def render(self, **kwargs):
        '''Start a WebSocket server that autoconnects to the 3D Unity client'''
        self.config.RENDER = True
        self.config.NUM_WORKERS = 1
        self.evaluate(**kwargs)

    def train(self, **kwargs):
        '''Train a model using the current --config setting'''
        run_tune_experiment(self.config)


if __name__ == '__main__':
    def Display(lines, out):
        text = "\n".join(lines) + "\n"
        out.write(text)

    from fire import core
    core.Display = Display
    Fire(Anvil)
