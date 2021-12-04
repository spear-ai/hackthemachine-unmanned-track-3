import json
import os
from pathlib import Path
from typing import List
import imageio
import numpy as np


default_map_size_list = [
    8,
    12,
    16,
    24,
    32,
    40,
    48,
    56,
    64,
    96,
    112,
    128,
    144,
    160,
    176,
    192,
    224,
    240,
    256,
    288,
    320,
    352,
    384,
    416,
    480,
    512,
    576,
    640,
    704,
    768,
    832,
    896,
    960,
    1024
]

# Define map tiles (map directly to neural-mmo tiles)
map_tiles = {
    'border': 5,  # neural-mmo STONE
    'land': 2,  # neural-mmo GRASS
    'water': 1,
}


def create_map(
    size: int,
    latitude: float = None,
    longitude: float = None
):
    # TODO: Replace this function with something better
    assert size >= 6, 'Map size must be at least 6×6'
    assert latitude is None, 'Not implemented'
    assert longitude is None, 'Not implemented'

    # **Note**: A map is represented with standard Python lists.
    # Replace this with your library of choice.

    # Create a blank map of water:
    # * A map cell is either land or not-land (no water depth for now)
    map = [[{'is_land': False} for y in range(size)] for x in range(size)]

    # Draw wide coast in the top-right corner of the map
    coast_width = (size // 2) + 1

    for i in range(0, 1):
        for j in range(0, coast_width):
            x = -j - 1
            y = i
            map[y][x] = {'is_land': True}

    # Draw narrow coast in the bottom-right corner of the map
    coast_width = (size // 3) + 1

    for i in range(0, 1):
        for j in range(0, coast_width):
            x = -j - 1
            y = -i - 1
            map[y][x] = {'is_land': True}

    # Draw continent in the top-right corner of the map
    if size >= 8:
        continent_size = (size // 2)

        for i in range(0, continent_size):
            for j in range(continent_size - i):
                x = size - j - 1
                y = i
                map[y][x] = {'is_land': True}

    # Draw continent in bottom-right corner of the map
    if size >= 8:
        continent_size = (size // 3)

        for i in range(continent_size):
            for j in range(continent_size - i):
                x = size - j - 1
                y = -i - 1
                map[y][x] = {'is_land': True}

    # Draw island in the center of the map
    if size >= 8:
        island_size = (size // 10) + 1
        island_offset = (size // 2) - island_size

        for i in range(island_offset, island_offset + island_size):
            for j in range(island_offset, island_offset + island_size):
                x = j
                y = size - i - 1
                map[y][x] = {'is_land': True}

    return map


def load_texture(file_path: str):
    texture = imageio.imread(file_path)
    texture = texture[:, :, :3][::4, ::4]
    texture = texture.reshape(-1, 3).mean(0).astype(np.uint8)
    texture = texture.reshape(1, 1, 3)
    return texture


def load_static_environment(map_size: int, border_size: int):
    dir = os.path.normpath(os.path.join(
        __file__,
        f'../../static/{map_size}x{map_size}'
    ))

    try:
        file_path = os.path.join(dir, 'map.npy')
        encoded_map = np.load(file_path)

        file_path = os.path.join(dir, 'data.json')
        with open(file_path) as file:
            data = json.load(file)

        data['border_size'] = border_size

        data['northern_port_list'] = [
            [port[0] + border_size, port[1] + border_size]
            for port in data['northern_port_list']
        ]

        data['southern_port_list'] = [
            [port[0] + border_size, port[1] + border_size]
            for port in data['southern_port_list']
        ]

        # Flip the map's y-coordinates
        encoded_map = np.flipud(encoded_map)

        # Fill in the rest of the map border
        encoded_map = np.pad(
            encoded_map,
            constant_values=map_tiles['border'],
            pad_width=border_size
        )

        return {'data': data, 'encoded_map': encoded_map}
    except OSError:
        return None


def generate_environments(
    border_size: int = 16,
    map_size_list: List[int] = default_map_size_list,
    output: str = None
):
    if output is None:
        output = os.path.normpath(os.path.join(__file__, '../../generated'))

    # Load textures for each map tyle
    textures_dir = os.path.normpath(os.path.join(__file__, '../../textures'))

    map_tile_textures = {
        map_tiles['border']: load_texture(os.path.join(textures_dir, 'border.png')),
        map_tiles['land']: load_texture(os.path.join(textures_dir, 'land.png')),
        map_tiles['water']: load_texture(os.path.join(textures_dir, 'water.png')),
    }

    for map_size in map_size_list:
        environment_size = map_size + (2 * border_size)

        static_environment = load_static_environment(
            border_size=border_size,
            map_size=map_size
        )

        if static_environment is None:
            map = create_map(map_size)

            # A list of northern and southern ports that can be used to
            # create start/end points for vessels.
            northern_port_list = []
            southern_port_list = []

            for i in range(1, map_size // 3):
                for j in range(1, map_size - 1):
                    x = j

                    # If a northern water tile has land above or to the right, then it's a port
                    y = i
                    if not map[y][x]['is_land']:
                        if map[y - 1][x]['is_land']:
                            northern_port_list.append([
                                x + border_size,
                                y + border_size
                            ])
                        elif map[y][x + 1]['is_land']:
                            northern_port_list.append([
                                x + border_size,
                                y + border_size
                            ])

                    # If a southern water tile has land below or to the right, then it's a port
                    y = map_size - i - 1
                    if not map[y][x]['is_land']:
                        if map[y + 1][x]['is_land']:
                            southern_port_list.append([
                                x + border_size,
                                y + border_size
                            ])
                        elif map[y][x + 1]['is_land']:
                            southern_port_list.append([
                                x + border_size,
                                y + border_size
                            ])

            # Encode map to numpy arrays
            encoded_map = np.empty(shape=(environment_size, environment_size))
            encoded_map.fill(map_tiles['border'])

            for y in range(map_size):
                for x in range(map_size):
                    i = y + border_size
                    j = x + border_size

                    if map[y][x]['is_land']:
                        encoded_map[i][j] = map_tiles['land']
                        continue

                    encoded_map[i][j] = map_tiles['water']

            # Create environment JSON data
            data = {
                'border_size': border_size,
                'map_tiles': map_tiles,
                'northern_port_list': northern_port_list,
                'southern_port_list': southern_port_list
            }
        else:
            data = static_environment['data']
            encoded_map = static_environment['encoded_map']

        # Create thumbnail from encoded map
        thumbnail = [
            [map_tile_textures[tile] for tile in tile_row]
            for tile_row in encoded_map
        ]
        thumbnail = np.vstack([np.hstack(tile) for tile in thumbnail])

        environment_dir = os.path.join(
            output,
            f'{environment_size}x{environment_size}/training-1'
        )

        # Ensure the environment directory exists
        Path(environment_dir).mkdir(exist_ok=True, parents=True)

        # Save encoded map to `{environment_dir}/map.npy`
        file_path = os.path.join(environment_dir, 'map.npy')
        np.save(file_path, encoded_map.astype(int))

        # Save thumbnail to `{environment_dir}/thumbnail.png`
        file_path = os.path.join(environment_dir, 'thumbnail.png')
        imageio.imsave(file_path, thumbnail)

        # Save environment data to `{environment_dir}/data.json`
        file_path = os.path.join(environment_dir, 'data.json')
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)


if __name__ == '__main__':
    generate_environments()
