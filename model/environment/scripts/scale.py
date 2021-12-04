import json
import os
from pathlib import Path
from typing import List
import numpy as np

default_scale_list = list(range(2, 42))


def scale_static_environments(
    original_map_size: int = 24,
    scale_list: List[int] = default_scale_list
):
    static_dir = os.path.normpath(os.path.join(__file__, f'../../static'))

    original_dir = os.path.normpath(os.path.join(
        static_dir,
        f'{original_map_size}x{original_map_size}'
    ))

    file_path = os.path.join(original_dir, 'map.npy')
    original_encoded_map = np.load(file_path)

    file_path = os.path.join(original_dir, 'data.json')
    with open(file_path) as file:
        original_data = json.load(file)

    for scale in scale_list:
        scaled_encoded_map_size = original_map_size * scale

        scaled_dir = os.path.normpath(os.path.join(
            static_dir,
            f'{scaled_encoded_map_size}x{scaled_encoded_map_size}'
        ))

        # Increase the map size by scaling factor.
        scaled_encoded_map = np.kron(
            original_encoded_map,
            np.ones((scale, scale))
        )

        scaled_data = original_data.copy()

        # Update the port points by scaling factor.
        # This isn't ideal because the number of ports should increase also.
        scaled_data['northern_port_list'] = [
            [scale * point[0], scale * point[1]]
            for point in original_data['northern_port_list']
        ]

        scaled_data['southern_port_list'] = [
            [scale * point[0], scale * point[1]]
            for point in original_data['southern_port_list']
        ]

        # Ensure the scaled static directory exists
        Path(scaled_dir).mkdir(exist_ok=True, parents=True)

        # Save encoded map to `{scaled_dir}/map.npy`
        np.save(os.path.join(scaled_dir, 'map.npy'), scaled_encoded_map)

        # Save environment data to `{scaled_dir}/data.json`
        file_path = os.path.join(scaled_dir, 'data.json')
        with open(file_path, 'w') as file:
            json.dump(scaled_data, file, indent=2)


if __name__ == '__main__':
    scale_static_environments()
