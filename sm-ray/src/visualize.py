import ray
# import pickle5 as pickle
import pickle
from ray.tune.registry import register_env
from ray.rllib.agents.ppo import PPOTrainer
import supersuit as ss
from ray.rllib.env.wrappers.pettingzoo_env import PettingZooEnv
from PIL import Image
from ray.rllib.models import ModelCatalog
import numpy as np
import os
import argparse
from pathlib import Path
from ray import tune
from ray.rllib.models import ModelCatalog
from ray.tune.registry import register_env
from ray.rllib.env.wrappers.pettingzoo_env import ParallelPettingZooEnv
from pettingzoo.magent import tiger_deer_v3
import supersuit as ss
from ray import shutdown
from custom.models.custom_cnn_torch import CNNModelV2
from custom.envs.drug_runner import parallel_env
from pettingzoo.magent.render import Renderer
from pettingzoo.utils.conversions import from_parallel_wrapper, parallel_wrapper_fn
from pettingzoo.magent.magent_env import magent_parallel_env, make_env
from pettingzoo.utils import from_parallel

os.environ["SDL_VIDEODRIVER"] = "dummy"

parser = argparse.ArgumentParser(
    description="Render pretrained policy loaded from checkpoint"
)
parser.add_argument(
    "checkpoint_path",
    help="Path to the checkpoint. This path will likely be something like this: `~/ray_results/pistonball_v5/PPO/PPO_pistonball_v5_660ce_00000_0_2021-06-11_12-30-57/checkpoint_000050/checkpoint-50`",
)

args = parser.parse_args()

checkpoint_path = os.path.expanduser(args.checkpoint_path)
params_path = Path(checkpoint_path).parent.parent / "params.pkl"

ModelCatalog.register_custom_model("CNNModelV2", CNNModelV2)


def env_creator(args):
    env = parallel_env(
        map_size=68,
        minimap_mode=False,
        destroyer_step_recover=-0.1,
        panga_attacked=-0.1,
        max_cycles=300,
        extra_features=False,
    )
    env = ss.pad_action_space_v0(env)
    env = ss.dtype_v0(env, "float32")
    env = ss.resize_v0(env, x_size=84, y_size=84)
    env = ss.frame_stack_v1(env, 3)
    env = ss.normalize_obs_v0(env, env_min=0, env_max=1)
    return env


env = env_creator({})
env = from_parallel(env)
env.reset()


# print(env)
env_name = "drug_runner"
register_env(env_name, lambda config: PettingZooEnv(env_creator({})))

with open(params_path, "rb") as f:
    config = pickle.load(f)
    # num_workers not needed since we are not training
    del config["num_workers"]
    del config["num_gpus"]

ray.init(num_cpus=8, num_gpus=0)
# PPOagent = PPOTrainer(env=env_name, config=config)
# PPOagent.restore(checkpoint_path)


# PPOagent

reward_sum = 0
frame_list = []
i = 0
# env.reset()



# print(env.render("rgb_array"))

# renderer = Renderer(env, 24, "rgb_array")

# print(renderer.render("rgb_array"))

for agent in env.agent_iter():
    observation, reward, done, info = env.last()
    reward_sum += reward
    # print(reward)
    if done:
        action = None
    else:
        action=5
        # action, _, _ = PPOagent.get_policy("policy_0").compute_single_action(observation)

    env.step(action)
    i += 1
    if i % (len(env.possible_agents)+1) == 0:
        frame_list.append(Image.fromarray(env.render(mode='rgb_array')))
env.close()


print(reward_sum)
frame_list[0].save("out.gif", save_all=True, append_images=frame_list[1:], duration=3, loop=0)
