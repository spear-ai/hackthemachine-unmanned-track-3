import json
import math
import os
from pathlib import Path
from typing import List
import imageio
import numpy as np
# from neural_mmo.forge.blade.core import terrain
import xarray as xr

nc_file = 'data/grid002_100km_24x24.nc'
npy_file = nc_file.replace('.nc', '.npy')
json_file = nc_file.replace('.nc', '.json')

with xr.open_dataset(nc_file) as DS:
    longitude = DS.lon.values
    latitude = DS.lat.values
    mask = DS.mask.values

map_shape = mask.shape
encoded_map = np.empty(shape=map_shape)

# Define map tiles (map directly to neural-mmo tiles)
map_tiles = {
    'border': 0,  # neural-mmo LAVA
    'land': 2,  # neural-mmo GRASS
    'water': 1,
}

ny = map_shape[0]
nx = map_shape[1]

for y in range(ny):
    for x in range(nx):
        if y == 0:
            encoded_map[y][x] = map_tiles['border']
            continue
        if y == ny - 1:
            encoded_map[y][x] = map_tiles['border']
            continue
        if x == 0:
            encoded_map[y][x] = map_tiles['border']
            continue
        if x == nx - 1:
            encoded_map[y][x] = map_tiles['border']
            continue
        if mask[y][x] == 0:
            encoded_map[y][x] = map_tiles['land']
            continue
        if mask[y][x] == 1:
            encoded_map[y][x] = map_tiles['water']
            continue

# Save encoded map to *.npy file
np.save(npy_file, encoded_map.astype(int))

# Save environment data to *.json
map = [[{'is_land': False} for x in range(nx)] for y in range(ny)]  # Create a blank map of water
for y in range(ny):
    for x in range(nx):
        if mask[y][x] == 0:
            map[y][x] = {'is_land': True}

data = {'map': map, 'map_tiles': map_tiles}
with open(json_file, 'w') as file:
    json.dump(data, file, indent=2)

# def create_map(
#     size: int,
#     latitude: float = None,
#     longitude: float = None
# ):
#     # TODO: Replace this function with something better
#     assert size >= 6, 'Map size must be at least 6×6'
#     assert latitude is None, 'Not implemented'
#     assert longitude is None, 'Not implemented' 

#     # **Note**: A map is represented with standard Python lists.
#     # Replace this with your library of choice.

#     # Create a blank map of water:
#     # * A map cell is either land or not-land (no water depth for now)
#     map = [[{'is_land': False} for y in range(size)] for x in range(size)]

#     # Draw wide coast in the top-right corner of the map
#     coast_width = (size // 2) + 1

#     for i in range(0, 2):
#         for j in range(0, coast_width):
#             x = -j - 1
#             y = i
#             map[y][x] = {'is_land': True}

#     # Draw narrow coast in the bottom-right corner of the map
#     coast_width = (size // 3) + 1

#     for i in range(0, 2):
#         for j in range(0, coast_width):
#             x = -j - 1
#             y = -i - 1
#             map[y][x] = {'is_land': True}

#     # Draw continent in the top-right corner of the map
#     if size >= 7:
#         continent_size = (size // 2) + 1

#         for i in range(1, continent_size + 1):
#             for j in range(continent_size - i):
#                 x = size - j - 1
#                 y = i
#                 map[y][x] = {'is_land': True}

#     # Draw continent in bottom-right corner of the map
#     if size >= 9:
#         continent_size = (size // 3) + 1

#         for i in range(1, continent_size + 1):
#             for j in range(continent_size - i):
#                 x = size - j - 1
#                 y = -i - 1
#                 map[y][x] = {'is_land': True}

#     # Draw island in the center of the map
#     if size >= 8:
#         island_size = (size // 10) + 1
#         island_offset = (size // 2) - island_size

#         for i in range(island_offset, island_offset + island_size):
#             for j in range(island_offset, island_offset + island_size):
#                 x = j
#                 y = size - i - 1
#                 map[y][x] = {'is_land': True}

#     return map


# def load_texture(file_path: str):
#     texture = imageio.imread(file_path)
#     texture = texture[:, :, :3][::4, ::4]
#     texture = texture.reshape(-1, 3).mean(0).astype(np.uint8)
#     texture = texture.reshape(1, 1, 3)
#     return texture


# def generate_model_environments(
#     map_size_list: List[int] = default_map_size_list,
#     output: str = None
# ):
#     if output is None:
#         output = os.path.normpath(os.path.join(__file__, '../../generated'))

#     # Define map tiles (map directly to neural-mmo tiles)
#     map_tiles = {
#         'border': 0,  # neural-mmo LAVA
#         'land': 2,  # neural-mmo GRASS
#         'water': 1,
#     }

#     # Load textures for each map tyle
#     textures_dir = os.path.normpath(os.path.join(__file__, '../../textures'))

#     map_tile_textures = {
#         map_tiles['border']: load_texture(os.path.join(textures_dir, 'border.png')),
#         map_tiles['land']: load_texture(os.path.join(textures_dir, 'land.png')),
#         map_tiles['water']: load_texture(os.path.join(textures_dir, 'water.png')),
#     }

#     for map_size in map_size_list:
#         map = create_map(map_size)
#         data = {'map': map, 'map_tiles': map_tiles}
#         environment_dir = os.path.join(output, f'{map_size}x{map_size}')

#         # Encode map to numpy arrays
#         encoded_map = np.empty(shape=(map_size, map_size))

#         for y in range(map_size):
#             for x in range(map_size):
#                 if y == 0:
#                     encoded_map[y][x] = map_tiles['border']
#                     continue

#                 if y == map_size - 1:
#                     encoded_map[y][x] = map_tiles['border']
#                     continue

#                 if x == 0:
#                     encoded_map[y][x] = map_tiles['border']
#                     continue

#                 if x == map_size - 1:
#                     encoded_map[y][x] = map_tiles['border']
#                     continue

#                 if map[y][x]['is_land']:
#                     encoded_map[y][x] = map_tiles['land']
#                     continue

#                 encoded_map[y][x] = map_tiles['water']

#         # Create thumbnail from encoded map
#         thumbnail = [
#             [map_tile_textures[tile] for tile in tile_row]
#             for tile_row in encoded_map
#         ]
#         thumbnail = np.vstack([np.hstack(tile) for tile in thumbnail])

#         # Ensure the environment directory exists
#         Path(environment_dir).mkdir(exist_ok=True, parents=True)

#         # Save encoded map to `{environment_dir}/map.npy`
#         file_path = os.path.join(environment_dir, 'map.npy')
#         np.save(file_path, encoded_map.astype(int))

#         # Save thumbnail to `{environment_dir}/thumbnail.png`
#         file_path = os.path.join(environment_dir, 'thumbnail.png')
#         imageio.imsave(file_path, thumbnail)

#         # Save environment data to `{environment_dir}/data.json`
#         file_path = os.path.join(environment_dir, 'data.json')
#         with open(file_path, 'w') as file:
#             json.dump(data, file, indent=2)


# if __name__ == '__main__':
#     generate_model_environments()
