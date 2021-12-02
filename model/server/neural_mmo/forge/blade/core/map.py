from pdb import set_trace as T
import numpy as np

from neural_mmo.forge.blade import core
from neural_mmo.forge.blade.lib import material

import os


class Map:
    '''Map object representing a list of tiles

    Also tracks a sparse list of tile updates
    '''

    def __init__(self, config, realm):
        self.config = config

        sz = config.TERRAIN_SIZE
        self.tiles = np.zeros((sz, sz), dtype=object)

        for r in range(sz):
            for c in range(sz):
                self.tiles[r, c] = core.Tile(config, realm, r, c)

    @property
    def packet(self):
        '''Packet of degenerate resource states'''
        missingResources = []
        for e in self.updateList:
            missingResources.append(e.pos)
        return missingResources

    @property
    def repr(self):
        '''Flat matrix of tile material indices'''
        return [[t.mat.index for t in row] for row in self.tiles]

    def reset(self, realm, idx):
        '''Reuse the current tile objects to load a new map'''
        self.updateList = set()
        materials = {mat.index: mat for mat in material.All}

        if idx > 0:
            # A positive index refers to a training map
            file_path = os.path.join(
                self.config.PATH_MAPS,
                self.config.PATH_MAP_SUFFIX_EVAL.format(idx)
            )
        elif idx < 0:
            # A negative index refers to an evaluation map
            file_path = os.path.join(
                self.config.PATH_MAPS,
                self.config.PATH_MAP_SUFFIX_TRAIN.format(-idx)
            )
        else:
            assert idx != 0, 'Index should be a positive or negative integer'

        for r, row in enumerate(np.load(file_path)):
            for c, idx in enumerate(row):
                mat = materials[idx]
                tile = self.tiles[r, c]
                tile.reset(mat, self.config)

    def step(self):
        '''Evaluate updatable tiles'''
        for e in self.updateList.copy():
            if e.static:
                self.updateList.remove(e)
            e.step()

    def harvest(self, r, c):
        '''Called by actions that harvest a resource tile'''
        self.updateList.add(self.tiles[r, c])
        return self.tiles[r, c].harvest()
