import geopandas as gpd
from shapely.geometry import Polygon
import numpy as np

### Pick bounds, adjust desired columns and rows, and pick output .json file location

left = -99
right = -76
bottom = -4
top = 16.5

xmin, ymin, xmax, ymax = left, bottom, right, top

grid_columns = 16
grid_rows = 16

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
grid.to_file("16by16.json", driver="GeoJSON")