import json
import os
from pathlib import Path
from typing import List
import imageio
import numpy as np
import xarray as xr


default_environment_name_list = [
    'grid004_025deg_72x72',
    'grid004_010deg_180x180',
]

map_tiles = {
    'border': 0,
    'land': 2,
    'water': 1
}

def load_texture(file_path: str):
    texture = imageio.imread(file_path)
    texture = texture[:, :, :3][::4, ::4]
    texture = texture.reshape(-1, 3).mean(0).astype(np.uint8)
    texture = texture.reshape(1, 1, 3)
    return texture

def create_thumbnail(environment):
    # Load textures for each map tile
    textures_dir = os.path.normpath(os.path.join(__file__, '../../textures'))

    textures = {
        map_tiles['border']: load_texture(os.path.join(textures_dir, 'border.png')),
        map_tiles['land']: load_texture(os.path.join(textures_dir, 'land.png')),
        map_tiles['water']: load_texture(os.path.join(textures_dir, 'water.png')),
    }

    thumbnail = [
        [textures[tile] for tile in tile_row]
        for tile_row in environment['encoded_map']
    ]

    thumbnail = np.vstack([np.hstack(tile) for tile in thumbnail])

    return thumbnail

def load_original_environment(environment_name: str):
    file_path = os.path.normpath(os.path.join(
        __file__,
        f'../../../../data/{environment_name}'
    ))

    with xr.open_dataset(f'{file_path}.nc') as dataset:
        mask = dataset.mask.values

    encoded_map = np.empty(shape=mask.shape)

    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            if mask[y][x] == 0:
                encoded_map[y][x] = map_tiles['land']
            elif mask[y][x] == 1:
                encoded_map[y][x] = map_tiles['water']
    
    encoded_map = np.flipud(encoded_map)
    map = []

    for y in range(encoded_map.shape[0]):
        map.append([])

        for x in range(encoded_map.shape[1]):
            map[y].append({'is_land': encoded_map[y][x] == map_tiles['land']})

    return {
        'encoded_map': encoded_map,
        'map': map
    }


def generate_environments(
    environment_name_list: List[str] = default_environment_name_list,
    output: str = None
):
    if output is None:
        output = os.path.normpath(os.path.join(__file__, '../../generated-tiger-deer'))

    for environment_name in environment_name_list:
        environment = load_original_environment(environment_name)

        # A list of northern and southern ports that can be used to
        # create start/end points for vessels.
        northern_port_list = environment['northern_port_list'] = []
        southern_port_list = environment['southern_porn_list'] = []
        map = environment['map']
        map_size = len(map)

        for i in range(1, map_size // 3):
            for j in range(1, map_size - 1):
                x = j

                # A top water tile with land above or to the right is a northern port
                y = i
                if not map[y][x]['is_land']:
                    if map[y - 1][x]['is_land']:
                        northern_port_list.append([x, y])
                    elif map[y][x + 1]['is_land']:
                        northern_port_list.append([x, y])

                # If bottom water tile with land below or to the right is a southern port
                y = map_size - i - 1
                if not map[y][x]['is_land']:
                    if map[y + 1][x]['is_land']:
                        southern_port_list.append([x, y])
                    elif map[y][x + 1]['is_land']:
                        southern_port_list.append([x, y])

        # Create environment JSON data
        data = {
            'border_size': 0,
            'map': map,
            'map_tiles': map_tiles,
            'northern_port_list': northern_port_list,
            'southern_port_list': southern_port_list
        }

        environment_dir = os.path.join(
            output,
            f'{map_size}x{map_size}/training-1'
        )

        # Ensure the environment directory exists
        Path(environment_dir).mkdir(exist_ok=True, parents=True)

        # Save encoded map to `{environment_dir}/map.npy`
        file_path = os.path.join(environment_dir, 'map.npy')
        np.save(file_path, environment['encoded_map'].astype(int))

        # Save thumbnail to `{environment_dir}/thumbnail.png`
        file_path = os.path.join(environment_dir, 'thumbnail.png')
        imageio.imsave(file_path, create_thumbnail(environment))

        # Save environment data to `{environment_dir}/data.json`
        file_path = os.path.join(environment_dir, 'data.json')
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)


if __name__ == '__main__':
    generate_environments()
