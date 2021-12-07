import os
import ray

# Get the virtual env directory containing the ray module
ray_file_dir = os.path.abspath(os.path.join(ray.__file__, '..'))

# Get the diff file path
diff_file_path = os.path.abspath(os.path.join(__file__, '../patch.diff'))

os.system(f'cd "{ray_file_dir}" && patch -N -p1 < "{diff_file_path}"')
