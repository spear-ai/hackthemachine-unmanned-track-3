import geopandas as gpd
from shapely.geometry import Polygon
import numpy as np
# points = gpd.read_file('points.shp')

left = -91.55238
right = -72.94178
bottom = 1.85661
top = 17.29835

xmin, ymin, xmax, ymax = left, bottom, right, top

grid_columns = 240
grid_rows = 240

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
grid.to_file("240by240.json", driver="GeoJSON")