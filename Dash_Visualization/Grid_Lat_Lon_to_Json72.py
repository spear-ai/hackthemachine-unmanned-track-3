import geopandas as gpd
from shapely.geometry import Polygon
import numpy as np
# points = gpd.read_file('points.shp')

left = -93.5
right = -75.5
bottom = 0
top = 18

xmin, ymin, xmax, ymax = left, bottom, right, top

grid_columns = 72
grid_rows = 72

length = abs(top - bottom) / grid_rows
wide = abs(right - left) / grid_columns


cols = list(np.linspace(xmin, xmax, num= grid_columns+1))
rows = list(np.linspace(ymin, ymax, num= grid_rows+1))



polygons = []
for x in cols[:-1]:
    for y in rows[:-1]:
        polygons.append(Polygon([(x,y), (x+wide, y), (x+wide, y+length), (x, y+length)]))

grid = gpd.GeoDataFrame({'geometry':polygons})
# dats = grid.to_json()
grid.to_file("72by72.json", driver="GeoJSON")