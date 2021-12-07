import json
import math
import os
from pathlib import Path
from typing import List
import numpy as np
from scipy import interpolate

# from neural_mmo.forge.blade.core import terrain
import xarray as xr

# grid_file = 'data/grid004_025deg_72x72.nc'
grid_file = 'data/grid004_010deg_180x180.nc'
weath_file = 'data/weather_gfs_20211207.nc'
waves_file = 'data/waves_ww3_20211207.nc'

# Read grid
with xr.open_dataset(grid_file) as DS:
    lon0 = DS.lon.values
    lat0 = DS.lat.values

# 1-D lon and lat vectors for interp2d:
x0 = lon0[0,:]
y0 = lat0[:,0]

# Read weather data, interpolate, and save numpy file
for var in ['cloud_ceiling','cloud_cover','precip','wave_height']:
    if var == 'wave_height':
        file = waves_file
    else:
        file = weath_file

    npy_file = grid_file.replace('.nc', '_'+var+'.npy')

    with xr.open_dataset(file) as DS:
        lon1 = DS.lon.values
        lat1 = DS.lat.values
        time = DS.time
        data1 = DS[var].values
    
    # Step through time and interpolate
    data = np.zeros((len(time),len(y0),len(x0)))
    for t in range(len(time)):
        f = interpolate.interp2d(lon1, lat1, data1[t,:,:], kind='linear')
        data[t,:,:] = f(x0, y0)

    np.save(npy_file, data)

