import math
import warnings
import json
from pathlib import Path

import magent
import numpy as np
from gym.spaces import Box, Discrete
from gym.utils import EzPickle

from pettingzoo import AECEnv
from pettingzoo.magent.render import Renderer
from pettingzoo.utils import agent_selector
from pettingzoo.utils.conversions import from_parallel_wrapper, parallel_wrapper_fn

from pettingzoo.magent.magent_env import magent_parallel_env, make_env


# Base Env can be found at https://github.com/Farama-Foundation/MAgent/blob/master/magent/gridworld.py


default_map_size = 68
max_cycles_default = 300
minimap_mode_default = False
default_env_args = dict(destroyer_step_recover=-0.1, panga_attacked=-0.1)


def parallel_env(map_size=default_map_size, max_cycles=max_cycles_default, minimap_mode=minimap_mode_default, extra_features=False, **env_args):
    env_env_args = dict(**default_env_args)
    env_env_args.update(env_args)
    return _parallel_env(map_size, minimap_mode, env_env_args, max_cycles, extra_features)


def raw_env(map_size=default_map_size, max_cycles=max_cycles_default, minimap_mode=minimap_mode_default, extra_features=False, **env_args):
    return from_parallel_wrapper(parallel_env(map_size, max_cycles, minimap_mode, extra_features, **env_args))


env = make_env(raw_env)

# TODO: Load Complete packages at once rather than individual agents.
# class ForcePackageLoader:
#     def __init__(self):
#         pass
    
#     @classmethod
#     def load_from_json(cls):
#         with open(file_path, "r") as f:
#             agent_data = json.load(f)
#         return cls()        


class AgentLoader:
    def __init__(self, name, details, options):
        self.name = name
        self.details = details
        self.options = options
    
    @classmethod
    def load_from_json(cls, file_path, gw):
        with open(file_path, "r") as f:
            agent_data = json.load(f)
        agent_data['options']['view_range'] = gw.CircleRange(agent_data['options']['view_distance'])
        agent_data['options']['attack_range'] = gw.CircleRange(agent_data['options']['attack_distance'])
        del agent_data['options']['attack_distance']
        del agent_data['options']['attack_shape']
        del agent_data['options']['view_distance']
        del agent_data['options']['view_shape']
        return cls(**agent_data)
    

def get_config(map_size, minimap_mode, destroyer_step_recover, panga_attacked):
    gw = magent.gridworld
    cfg = gw.Config()

    cfg.set({"map_width": map_size, "map_height": map_size})
    cfg.set({"embedding_size": 10})
    cfg.set({"minimap_mode": minimap_mode})

    file_dir = Path(__file__).parent

    
    # Red Team
    panga_agent = AgentLoader.load_from_json(str(file_dir / "assets/vehicles/panga.json"), gw)
    panga = cfg.register_agent_type(panga_agent.name, panga_agent.options)

    # Blue Team
    destroyer_agent = AgentLoader.load_from_json(str(file_dir / "assets/vehicles/destroyer.json"), gw)
    destroyer = cfg.register_agent_type(destroyer_agent.name, destroyer_agent.options)

    #neutral_group = cfg.add_group(neutral)
    panga_group = cfg.add_group(panga)
    blue_force = cfg.add_group(destroyer)

    
    a = gw.AgentSymbol(blue_force, index='any')
    b = gw.AgentSymbol(blue_force, index='any')
    c = gw.AgentSymbol(panga_group, index='any')

    # destroyers get reward when they attack a panga simultaneously
    e1 = gw.Event(a, 'attack', c)
    e2 = gw.Event(b, 'attack', c)
    destroyer_attack_rew = 1
    
    # reward is halved because the reward is double counted
    cfg.add_reward_rule(e1 & e2, receiver=[a, b], value=[destroyer_attack_rew / 2, destroyer_attack_rew / 2])
    cfg.add_reward_rule(e1, receiver=[c], value=[panga_attacked])

    return cfg


class _parallel_env(magent_parallel_env, EzPickle):
    metadata = {'render.modes': ['human', 'rgb_array'], 'name': "drug_runner_v0"}

    def __init__(self, 
                 map_size, 
                 minimap_mode, 
                 reward_args, 
                 max_cycles,
                 extra_features):
        
        EzPickle.__init__(self, map_size, minimap_mode, reward_args, max_cycles, extra_features)
        assert map_size >= 10, "size of map must be at least 10"
        env = magent.GridWorld(get_config(map_size, minimap_mode, **reward_args), map_size=map_size)

        handles = env.get_handles()
        reward_vals = np.array([1, -1] + list(reward_args.values()))
        reward_range = [np.minimum(reward_vals, 0).sum(), np.maximum(reward_vals, 0).sum()]

        names = ["panga", "destroyer"]
        super().__init__(env, handles, names, map_size, max_cycles, reward_range, minimap_mode, extra_features)

        
    def generate_map(self):
        env, map_size = self.env, self.map_size
        handles = env.get_handles()

#         env.add_walls(method="custom", pos=[(1,2), (4,5), (9,8)])
#         env.add_agents(handles[0], method="custom", pos=[(1,2), (4,5), (9,8)])
        
        env.add_walls(method="random", n=map_size * map_size * 0.04)
        env.add_agents(handles[0], method="random", n=30)
        env.add_agents(handles[1], method="random", n=3)
