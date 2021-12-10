# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# or in the "license" file accompanying this file. This file is distributed 
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either 
# express or implied. See the License for the specific language governing 
# permissions and limitations under the License.
import sys
sys.path.append("./src/common/")

import os
import json
import gym
import ray

from ray.tune.registry import register_env
from ray.tune import registry
from ray.rllib.models import ModelCatalog
from ray.tune.registry import register_env
from ray.rllib.env.wrappers.pettingzoo_env import PettingZooEnv
from pettingzoo.magent import tiger_deer_v3
from ray.rllib.env.wrappers.pettingzoo_env import ParallelPettingZooEnv
import torch
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
import supersuit as ss
from torch import nn

from ray.tune.tune import run_experiments, run
from ray.tune.schedulers import create_scheduler
from ray.tune.experiment import convert_to_experiment_list, Experiment

from common.sagemaker_rl.ray_launcher import SageMakerRayLauncher

from ray_experiment_builder import RayExperimentBuilder

from utils.loader import load_algorithms, load_preprocessors

from custom.envs.drug_runner import parallel_env


# CPU
# 462105765813.dkr.ecr.<region>.amazonaws.com/sagemaker-rl-ray-container:ray-1.6.0-torch-cpu-py36
# 462105765813.dkr.ecr.<region>.amazonaws.com/sagemaker-rl-ray-container:ray-1.6.0-tf-cpu-py37

# GPU
# 462105765813.dkr.ecr.<region>.amazonaws.com/sagemaker-rl-ray-container:ray-1.6.0-torch-gpu-py36
# 462105765813.dkr.ecr.<region>.amazonaws.com/sagemaker-rl-ray-container:ray-1.6.0-tf-gpu-py37


def gen_policy(i):
    config = {
        "model": {
            "custom_model": "CNNModelV2",
        },
        "gamma": 0.99,
    }
    return (None, obs_space, act_space, config)


def env_creator(args):
    env = parallel_env(map_size=68, minimap_mode=False, destroyer_step_recover=-0.1, panga_attacked=-0.1, max_cycles=500, extra_features=False)
    env = ss.pad_action_space_v0(env)
    env = ss.dtype_v0(env, 'float32')
    env = ss.resize_v0(env, x_size=84, y_size=84)
    env = ss.frame_stack_v1(env, 3)
    env = ss.normalize_obs_v0(env, env_min=0, env_max=1)
    return env
    

class MyLauncher(SageMakerRayLauncher):
    def register_env_creator(self):
        from custom.envs.drug_runner import parallel_env
        env_name = "drug_runner"
        register_env(env_name, lambda config: ParallelPettingZooEnv(env_creator(config)))
    
    def register_algorithms_and_preprocessors(self):
        # from custom.models.impala_cnn_torch import ImpalaCNN
        from custom.models.custom_cnn_torch import CNNModelV2
        ModelCatalog.register_custom_model("CNNModelV2", CNNModelV2)

    def get_experiment_config(self):
        self.register_algorithms_and_preprocessors()


        test_env = ParallelPettingZooEnv(env_creator({}))
        obs_space = test_env.observation_space
        act_space = test_env.action_space
        
        def gen_policy(i):
            config = {
                "model": {
                    "custom_model": "CNNModelV2",
                },
                "gamma": 0.99,
            }
            return (None, obs_space, act_space, config)

        policies = {"policy_0": gen_policy(0)}

        policy_ids = list(policies.keys())
        
        return {
            "training": {
                "run": "PPO",
                "stop": {"episodes_total": 1000},
                "config": {
                    "framework": "torch",
                    "log_level": "INFO",
                    "env": "drug_runner",
                    "gamma": 0.995,
                    'use_gae': True,
                    "lambda": 0.9,
                    "gamma": .99,
                    "kl_coeff": 1.0,
                    "num_sgd_iter": 20,
                    "compress_observations": True,
                    'lr': 2e-05,
                    'grad_clip': 0.001,
                    "clip_param": 0.4,
                    'vf_loss_coeff': 0.25,
                    "sgd_minibatch_size": 8,
                    "train_batch_size": 256,
                    "num_workers": 5,
                    "num_cpus_per_worker": 3,
                    "num_envs_per_worker": 1,
                    "num_gpus": 2,
                    "ignore_worker_failures": True,
                    "multiagent": {
                        "policies": policies,
                        "policy_mapping_fn": (
                            lambda agent_id: policy_ids[0]),
                    }
                },

            }
        }


if __name__ == "__main__":
    MyLauncher().train_main()