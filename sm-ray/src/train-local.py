from ray import tune
from ray.rllib.models import ModelCatalog
from ray.tune.registry import register_env
from ray.rllib.env.wrappers.pettingzoo_env import ParallelPettingZooEnv
from pettingzoo.magent import tiger_deer_v3
import supersuit as ss
from ray import shutdown
from custom.models.custom_cnn_torch import CNNModelV2
from custom.envs.drug_runner import parallel_env


def env_creator(args):
    env = parallel_env(map_size=68, minimap_mode=False, destroyer_step_recover=-0.1, panga_attacked=-0.1, max_cycles=500, extra_features=False)
    env = ss.pad_action_space_v0(env)
    env = ss.dtype_v0(env, 'float32')
    env = ss.resize_v0(env, x_size=84, y_size=84)
    env = ss.frame_stack_v1(env, 3)
    env = ss.normalize_obs_v0(env, env_min=0, env_max=1)
    return env


if __name__ == "__main__":
    shutdown()

    env_name = "drug_runner"
    register_env(env_name, lambda config: ParallelPettingZooEnv(env_creator(config)))

    test_env = ParallelPettingZooEnv(env_creator({}))
    obs_space = test_env.observation_space
    act_space = test_env.action_space

    ModelCatalog.register_custom_model("CNNModelV2", CNNModelV2)

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

    tune.run(
        "PPO",
        name="PPO",
        stop={"episodes_total": 1000},
        checkpoint_freq=10,
        local_dir="~/ray_results/"+env_name,
        config={
            # Environment specific
            "env": env_name,
            # General
            "log_level": "INFO",
            "framework": "torch",
            "num_gpus": 0,
            "num_workers": 6,
            "num_cpus_per_worker": 1,
            "num_envs_per_worker": 1,
            "batch_mode": 'truncate_episodes',
            'use_gae': True,
            "lambda": 0.9,
            "gamma": .99,
            "clip_param": 0.4,
            'grad_clip': 0.001,
            "entropy_coeff": 0.1,
            'vf_loss_coeff': 0.25,
            "compress_observations": True,
            "sgd_minibatch_size": 4,
            "num_sgd_iter": 10, # epoc
            'rollout_fragment_length': 4,
            "train_batch_size": 16,
            'lr': 2e-05,
            "clip_actions": True,
            # Method specific
            "multiagent": {
                "policies": policies,
                "policy_mapping_fn": (
                    lambda agent_id: policy_ids[0]),
            },
        },
    )