from pdb import set_trace as T
from neural_mmo.forge.blade import core
from neural_mmo.forge.blade.core import config
from neural_mmo.forge.blade.io.stimulus.static import Stimulus
from neural_mmo.forge.trinity.scripted import baselines
from neural_mmo.forge.trinity.agent import Agent
from neural_mmo.forge.blade.systems.ai import behavior
from projekt import rllib_wrapper
import os


class RLlibConfig:
    '''Base config for RLlib Models

    Extends core Config, which contains environment, evaluation,
    and non-RLlib-specific learning parameters'''

    @property
    def MODEL(self):
        return self.__class__.__name__

    # Checkpointing. Resume will load the latest trial, e.g. to continue training
    # Restore (overrides resume) will force load a specific checkpoint (e.g. for rendering)
    RESUME = False
    RESTORE = 'experiments/CompetitionRound1/Dev_9fe1/checkpoint_001000/checkpoint-1000'
    # PATH_ROOT = os.path.normpath(os.path.join(__file__, '../..'))
    # RESTORE = os.path.join(
    #    PATH_ROOT,
    #    'experiments/CompetitionRound1/Dev_9fe1/checkpoint_001000/checkpoint-1000'
    # )

    # Policy specification
    AGENTS = [Agent]
    EVAL_AGENTS = [baselines.Meander,
                   baselines.Forage, baselines.Combat, Agent]
    EVALUATE = False  # Reserved param

    #Hardware and debug
    NUM_WORKERS = 1
    NUM_GPUS_PER_WORKER = 0
    NUM_GPUS = 0
    EVALUATION_NUM_WORKERS = 1
    LOCAL_MODE = False
    LOG_LEVEL = 1

    # Training and evaluation settings
    EVALUATION_INTERVAL = 1
    EVALUATION_NUM_EPISODES = 3
    EVALUATION_PARALLEL = True
    TRAINING_ITERATIONS = 3
    KEEP_CHECKPOINTS_NUM = 3
    CHECKPOINT_FREQ = 1
    LSTM_BPTT_HORIZON = 2
    NUM_SGD_ITER = 1

    # Model
    SCRIPTED = None
    N_AGENT_OBS = 100
    NPOLICIES = 1
    HIDDEN = 64
    EMBED = 64

    # Reward
    TEAM_SPIRIT = 0.0
    ACHIEVEMENT_SCALE = 1.0/15.0


class LargeMaps(core.Config, RLlibConfig, config.AllGameSystems):
    '''Large scale Neural MMO training setting

    Features up to 1000 concurrent agents and 1000 concurrent NPCs,
    1km x 1km maps, and 5/10k timestep train/eval horizons

    This is the default setting as of v1.5 and allows for large
    scale multiagent research even on relatively modest hardware'''

    # Memory/Batch Scale
    NUM_WORKERS = 14
    TRAIN_BATCH_SIZE = 64 * 256 * NUM_WORKERS
    ROLLOUT_FRAGMENT_LENGTH = 32
    SGD_MINIBATCH_SIZE = 128

    # Horizon
    TRAIN_HORIZON = 8192
    EVALUATION_HORIZON = 8192


class SmallMaps(RLlibConfig, config.AllGameSystems, config.SmallMaps):
    '''Small scale Neural MMO training setting

    Features up to 128 concurrent agents and 32 concurrent NPCs,
    60x60 maps (excluding the border), and 1000 timestep train/eval horizons.

    This setting is modeled off of v1.1-v1.4 It is appropriate as a quick train
    task for new ideas, a transfer target for agents trained on large maps,
    or as a primary research target for PCG methods.'''

    # Memory/Batch Scale
    NUM_WORKERS = 2
    TRAIN_BATCH_SIZE = 64 * 256 * NUM_WORKERS
    ROLLOUT_FRAGMENT_LENGTH = 256
    SGD_MINIBATCH_SIZE = 128

    # Horizon
    TRAIN_HORIZON = 1024
    EVALUATION_HORIZON = 1024


class Debug(SmallMaps, config.AllGameSystems):
    '''Debug Neural MMO training setting

    A version of the SmallMap setting with greatly reduced batch parameters.
    Only intended as a tool for identifying bugs in the model or environment'''
    LOAD = False
    LOCAL_MODE = True
    NUM_WORKERS = 1

    SGD_MINIBATCH_SIZE = 100
    TRAIN_BATCH_SIZE = 400
    TRAIN_HORIZON = 200
    EVALUATION_HORIZON = 50

    HIDDEN = 2
    EMBED = 2


# AICrowd competition settings
class CompetitionRound1(config.Achievement, SmallMaps):
    @property
    def SPAWN(self):
        return self.SPAWN_CONCURRENT

    # Debug
    TERRAIN_BORDER = 1
    TERRAIN_EVAL_MAPS = 0
    TERRAIN_RENDER = True
    TERRAIN_SIZE = 5
    TERRAIN_TRAIN_MAPS = 1

    # Update paths to use the /model/server directory.
    # The library shouldn’t search for assets in the current working directory…
    PATH_ROOT = os.path.normpath(os.path.join(__file__, '../..'))
    print('HERE', PATH_ROOT)
    PATH_BASELINES = os.path.join(PATH_ROOT, 'baselines')
    PATH_ALL_EVALUATIONS = os.path.join(PATH_BASELINES, 'evaluations')
    PATH_CHECKPOINTS = os.path.join(PATH_ROOT, 'checkpoints')
    PATH_ALL_MODELS = os.path.join(PATH_BASELINES, 'models')
    PATH_RESOURCE = os.path.join(PATH_ROOT, 'resources')
    PATH_ASSETS = os.path.join(PATH_RESOURCE, 'assets')
    PATH_MAPS = os.path.normpath(os.path.join(
        PATH_ROOT,
        '../environment/generated/16x16')
    )
    print('THERE')
    print(PATH_MAPS)
    PATH_MAPS_LARGE = os.path.join(PATH_MAPS, 'large')
    PATH_MAPS_SMALL = os.path.join(PATH_MAPS, 'small')
    PATH_TILE = os.path.join(PATH_ASSETS, 'tiles/{}.png')
    PATH_TEXT = os.path.join(PATH_ASSETS, 'text')
    PATH_LOGO = os.path.join(PATH_TEXT, 'ascii.txt')
    PATH_THEMES = os.path.join(
        PATH_ROOT,
        'neural_mmo/forge/blade/systems/visualizer'
    )
    PATH_THEME_PUB = os.path.join(PATH_THEMES, 'index_publication.html')
    PATH_THEME_WEB = os.path.join(PATH_THEMES, 'index_web.html')

    NENT = 128
    NPOP = 1


class CompetitionRound2(config.Achievement, SmallMaps):
    @property
    def SPAWN(self):
        return self.SPAWN_CONCURRENT

    @property
    def NENT(self):
        return 8 * len(self.AGENTS)

    NPOP = 16
    AGENTS = NPOP*[Agent]
    EVAL_AGENTS = 8*[baselines.Meander,
                     baselines.Forage, baselines.Combat, Agent]

    AGENT_LOADER = config.TeamLoader
    COOPERATIVE = True
    TEAM_SPIRIT = 1.0


class CompetitionRound3(config.Achievement, LargeMaps):
    @property
    def SPAWN(self):
        return self.SPAWN_CONCURRENT

    NENT = 1024
    NPOP = 32
    COOPERATIVE = True
    TEAM_SPIRIT = 1.0
    AGENT_LOADER = config.TeamLoader


# NeurIPS Experiments
class SmallMultimodalSkills(SmallMaps, config.AllGameSystems):
    pass


class LargeMultimodalSkills(LargeMaps, config.AllGameSystems):
    pass


class MagnifyExploration(SmallMaps, config.Resource, config.Progression):
    pass


class Population4(MagnifyExploration):
    NENT = 4


class Population32(MagnifyExploration):
    NENT = 32


class Population256(MagnifyExploration):
    NENT = 256


class DomainRandomization16384(SmallMaps, config.AllGameSystems):
    TERRAIN_TRAIN_MAPS = 16384


class DomainRandomization256(SmallMaps, config.AllGameSystems):
    TERRAIN_TRAIN_MAPS = 256


class DomainRandomization32(SmallMaps, config.AllGameSystems):
    TERRAIN_TRAIN_MAPS = 32


class DomainRandomization1(SmallMaps, config.AllGameSystems):
    TERRAIN_TRAIN_MAPS = 1


class TeamBased(MagnifyExploration, config.Combat):
    NENT = 128
    NPOP = 32
    COOPERATIVE = True
    TEAM_SPIRIT = 0.5

    @property
    def SPAWN(self):
        return self.SPAWN_CONCURRENT
