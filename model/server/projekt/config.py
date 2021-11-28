from pdb import set_trace as T
import os
from neural_mmo.forge.blade import core
from neural_mmo.forge.trinity.scripted import baselines
from neural_mmo.forge.trinity.agent import Agent


class RLlibConfig:
    '''Base config for RLlib Models

    Extends core Config, which contains environment, evaluation,
    and non-RLlib-specific learning parameters'''

    @property
    def MODEL(self):
        return self.__class__.__name__

    # Checkpointing. Resume will load the latest trial, e.g. to continue training
    # Restore (overrides resume) will force load a specific checkpoint (e.g. for rendering)
    PATH_ROOT = os.path.normpath(os.path.join(__file__, '../..'))
    RESUME = False
    RESTORE = os.path.normpath(os.path.join(
        PATH_ROOT,
        'experiments/CompetitionRound1/Dev_9fe1/checkpoint_001000/checkpoint-1000')
    )

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


class PathsConfig:
    # Update paths to use the /model directory.
    # The library shouldn’t search for assets in the current working directory…
    PATH_ROOT = os.path.normpath(os.path.join(__file__, '../../..'))
    PATH_BASELINES = os.path.join(PATH_ROOT, 'server/baselines')
    PATH_ALL_EVALUATIONS = os.path.join(PATH_BASELINES, 'server/evaluations')
    PATH_CHECKPOINTS = os.path.join(PATH_ROOT, 'server/checkpoints')
    PATH_ALL_MODELS = os.path.join(PATH_BASELINES, 'server/models')
    PATH_RESOURCE = os.path.join(PATH_ROOT, 'server/resources')
    PATH_ASSETS = os.path.join(PATH_RESOURCE, 'assets')
    PATH_ENVIRONMENT = os.path.normpath(os.path.join(PATH_ROOT, 'environment'))
    PATH_MAPS_SMALL = os.path.join(PATH_RESOURCE, 'maps/procedural-small')
    PATH_MAPS_LARGE = os.path.join(PATH_RESOURCE, 'maps/procedural-large')
    PATH_MAPS = PATH_MAPS_LARGE
    PATH_TILE = os.path.join(PATH_ASSETS, 'tiles/{}.png')
    PATH_TEXT = os.path.join(PATH_ASSETS, 'text')
    PATH_LOGO = os.path.join(PATH_TEXT, 'ascii.txt')
    PATH_THEMES = os.path.join(
        PATH_ROOT,
        'server/neural_mmo/forge/blade/systems/visualizer'
    )
    PATH_THEME_PUB = os.path.join(PATH_THEMES, 'index_publication.html')
    PATH_THEME_WEB = os.path.join(PATH_THEMES, 'index_web.html')


def spawn_agents():
    # This function is completely broken and needs to be fixed.
    return [(14, 1)]


class DefaultConfig(core.Config, RLlibConfig, PathsConfig, core.config.AllGameSystems):
    # Note: Consider extending only some of the core `config.*` classes:
    # * core.config.Combat
    # * core.config.NPC
    # * core.config.Progression
    # * core.config.Resource

    @property
    def SPAWN(self):
        # Spawn "concurrent" creates agents before the game begins,
        # so we choose this mode to get that behavior.
        return self.SPAWN_CONCURRENT

    @property
    def SPAWN_CONCURRENT(self):
        # We need to override this function because
        # the spawn behavior doesn't do what we want.
        return spawn_agents

    # Various model training settings
    NUM_WORKERS = 1
    RESUME = None
    ROLLOUT_FRAGMENT_LENGTH = 256
    SGD_MINIBATCH_SIZE = 32
    TRAIN_BATCH_SIZE = 16 * 256 * NUM_WORKERS

    # The number of time steps an agent looks into the future to maximize their reward
    TRAIN_HORIZON = 10
    EVALUATION_HORIZON = 10

    # Assume maps are generated with a border of size 1.
    # Are there ramifications to changing the default border size?
    TERRAIN_BORDER = 1

    # Arbitrarily set map size to 16.
    # This will be overriden by `Forge.py` at run time anyway.
    TERRAIN_SIZE = 16

    # This setting alters default neural-mmo spawn behavior.
    # We need to ignore default spawn behavior anyway, so this should have no effect.
    TERRAIN_CENTER = TERRAIN_SIZE / 2

    # The number of maps to train and evaluate on.
    TERRAIN_EVAL_MAPS = 0
    TERRAIN_TRAIN_MAPS = 1

    # Update path settings
    PATH_ROOT = os.path.normpath(os.path.join(__file__, '../../..'))
    PATH_ENVIRONMENT = os.path.normpath(os.path.join(PATH_ROOT, 'environment'))
    PATH_MAPS = os.path.join(
        PATH_ENVIRONMENT,
        f'generated/{TERRAIN_SIZE}x{TERRAIN_SIZE}'
    )
    PATH_MAPS_LARGE = PATH_MAPS  # We distinguish maps by size, not by "large" or "small"
    PATH_MAPS_SMALL = PATH_MAPS  # We distinguish maps by size, not by "large" or "small"
    PATH_MAP_SUFFIX = 'map.npy'

    # Agents spawned per tick
    PLAYER_SPAWN_ATTEMPTS = 24

    # The number of entitites. I think this used to enable multiple entities to co-exist on a tile.
    # Perhaps there's a way to bring that behavior back?
    NENT = 1

    NMOB = 1


class EastPacificOcean(DefaultConfig):
    pass


class LargeMaps(core.Config, RLlibConfig, core.config.AllGameSystems):
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


class SmallMaps(RLlibConfig, PathsConfig, core.config.AllGameSystems, core.config.SmallMaps):
    '''Small scale Neural MMO training setting
    Features up to 128 concurrent agents and 32 concurrent NPCs,
    60x60 maps (excluding the border), and 1000 timestep train/eval horizons.

    This setting is modeled off of v1.1-v1.4 It is appropriate as a quick train
    task for new ideas, a transfer target for agents trained on large maps,
    or as a primary research target for PCG methods.'''

    # Memory/Batch Scale
    NUM_WORKERS = 1
    TRAIN_BATCH_SIZE = 16 * 256 * NUM_WORKERS
    ROLLOUT_FRAGMENT_LENGTH = 256
    SGD_MINIBATCH_SIZE = 32

    # Horizon
    TRAIN_HORIZON = 10
    EVALUATION_HORIZON = 10


class Debug(SmallMaps, core.config.AllGameSystems):
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


class CompetitionRound1(core.config.Achievement, SmallMaps):
    @property
    def SPAWN(self):
        return self.SPAWN_CONCURRENT

    NENT = 128
    NPOP = 1


class CompetitionRound2(core.config.Achievement, SmallMaps):
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

    AGENT_LOADER = core.config.TeamLoader
    COOPERATIVE = True
    TEAM_SPIRIT = 1.0


class CompetitionRound3(core.config.Achievement, LargeMaps):
    @property
    def SPAWN(self):
        return self.SPAWN_CONCURRENT

    NENT = 1024
    NPOP = 32
    COOPERATIVE = True
    TEAM_SPIRIT = 1.0
    AGENT_LOADER = core.config.TeamLoader


# NeurIPS Experiments
class SmallMultimodalSkills(SmallMaps, core.config.AllGameSystems):
    pass


class LargeMultimodalSkills(LargeMaps, core.config.AllGameSystems):
    pass


class MagnifyExploration(SmallMaps, core.config.Resource, core.config.Progression):
    pass


class Population4(MagnifyExploration):
    NENT = 4


class Population32(MagnifyExploration):
    NENT = 32


class Population256(MagnifyExploration):
    NENT = 256


class DomainRandomization16384(SmallMaps, core.config.AllGameSystems):
    TERRAIN_TRAIN_MAPS = 16384


class DomainRandomization256(SmallMaps, core.config.AllGameSystems):
    TERRAIN_TRAIN_MAPS = 256


class DomainRandomization32(SmallMaps, core.config.AllGameSystems):
    TERRAIN_TRAIN_MAPS = 32


class DomainRandomization1(SmallMaps, core.config.AllGameSystems):
    TERRAIN_TRAIN_MAPS = 1


class TeamBased(MagnifyExploration, core.config.Combat):
    NENT = 128
    NPOP = 32
    COOPERATIVE = True
    TEAM_SPIRIT = 0.5

    @property
    def SPAWN(self):
        return self.SPAWN_CONCURRENT
