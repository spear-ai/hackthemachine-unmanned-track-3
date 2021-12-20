import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import json
import numpy as np
import base64
import math as m
from urllib.request import urlopen
from ortools.sat.python import cp_model
# import pickle

# filename = 'graph.pkl'
# with open(filename, 'wb') as f:
#     pickle.dump(fig, f)




mapbox_access_token = "pk.eyJ1IjoiamtvZWhsZXIxMSIsImEiOiJja2d2MmMyYWswNDlzMnNtdW9jbDU0NXhmIn0.5Ynkm6tAvtl18Q5QBQT_7g"

# #AIS DAta
# url = 'https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/AIS/PassengerVessel.csv'
# df_ais_blue = pd.read_csv(url)
# df_ais_red = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/AIS/Tanker.csv')
# df_ais_green = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/AIS/Cargo.csv')

# df_histroutes = pd.read_csv ('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/HistoricalTraffickingRoutePoints.csv')

# ##Weather Data
# df_fog = pd.read_csv('https://github.com/spear-ai/hackthemachine-unmanned-track-3/blob/dash_visual/Dash_Visualization/synthetic_data/Weather/Visibility/fog3.csv?raw=true')
# df_mediumclouds = pd.read_csv ('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Weather/Visibility/medium_clouds.csv')
# df_highclouds = pd.read_csv ('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Weather/Visibility/higher.csv')
# df_highestclouds = pd.read_csv ('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Weather/Visibility/highest.csv')

# ## Read in trafficking data
# df_Blackroute = pd.read_csv ('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Targets/Blackroute.csv')

# ##Navigation
# navigation = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Navigability/NoNavigationPoints2.csv')

## Airbases
airbases = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Points_Of_Origin_Destination/Airbases.csv')

## Persisten Threat Detection System
ptds = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/PTDS5.csv')
ptds['sensor'] = 160

## p8 flight
# p8flight = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/p8_new.csv')
p8flight = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/p8_72.csv')

#Load 12 mile territorial line

# f = open(r'C:\Users\tjack\Documents\HackTheMachine\12milefileid.json',)
 
# # returns JSON object as
# # a dictionary
# jdata = json.load(f)

# urljson1 = "https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Grids/12milefile.json"
  
# # store the response of URL
# # response1 = urlopen(urljson1)
  
# # storing the JSON response 
# # from url in data
# # jdata = json.loads(response1.read())

# # values
# jdatadf = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Grids/12milefileid.csv')



# ## Read in 20 x 20 grid and Data
# # Opening JSON file
# # parameter for urlopen
# urljson = "https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Grids/20by20.json"
  
# # store the response of URL
# response = urlopen(urljson)
  
# # storing the JSON response 
# # from url in data
# data_json = json.loads(response.read())
# # f20 = open('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Grids/20by20.json',)
 
# # returns JSON object as
# # a dictionary
# grid20df = data_json

# #Load 24 x 24 data

urljson = 'https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/24by24.json'
  
# store the response of URL
response = urlopen(urljson)
  
# storing the JSON response 
# from url in data
data_json = json.loads(response.read())

# f24 = open('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/24by24.json',)
grid24df = data_json

# returns JSON object as
# a dictionary
# data1 = json.load(f24)

# grid24df = data1

urljson1 = 'https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/72by72.json'
response1 = urlopen(urljson1)
data_json1 = json.loads(response1.read())
# returns JSON object as
# a dictionary
# data240 = json.load(f240)

grid240df = data_json1

#For new json

for k in range(len(grid240df['features'])):
    grid240df['features'][k]['id'] = k

ids240 = [features['id'] for features in grid240df["features"]]

df_griddata240 = pd.DataFrame()
df_griddata240['ids'] = (ids240)
df_griddata240['value'] = 3

df_griddata = df_griddata240
df_griddata['text'] =  df_griddata.apply(lambda x: "Gameboard Index:" + str(x.ids), axis=1)




# df_griddatain = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\grid_data_20x20.csv')
# df_griddatain = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/grid_data_20x20.csv')
# df_griddatain = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\grid_data_24x24.csv')
df_griddatain = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/grid_data_72x721.csv')

## Edit navigation
# tozero = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Grids\24tozero.csv')
# toone = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Grids\24toone.csv')

# df_griddatain.loc[df_griddatain['ids'].isin(tozero['tozero']), 'Navigation'] = 0
# df_griddatain.loc[df_griddatain['ids'].isin(toone['toone']), 'Navigation'] = 1


# df_griddata['AIS'] = df_griddatain['AIS']
# df_griddata['Navigation'] = df_griddatain['Navigation']
# # Navigation Binary
# df_griddata['Navigation'].values[df_griddata['Navigation'].values > 1] = 1
# ## Initiate Plot with Target Data
# df_griddata['Fog'] = df_griddatain['Fog']
df_griddata['Origin'] = df_griddatain['origins']
df_griddata['Destination'] = df_griddatain['destinations']
# df_griddata['Historical Trafficking Routes'] = df_griddatain['Historical Trafficking Routes']


## New fog
# df_fogarray = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Weather\Visibility\fogtime.csv')
df_fogarray = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Weather/Visibility/fog_ceiling_72.csv')
# s = len(df_fogarray)




# rltracks3999 = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\targ72.csv')

##warship Track
# warship = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\warship72.csv')
warship = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/Destroyer_220.csv')
destroyer0 = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/Dest0_s.csv')

warship['sensor'] = 104
warship['velocity'] = 56

destroyer0['sensor'] = 104
destroyer0['velocity'] = 56

##warship Track
# destroyer1 = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\DestroyerPath15cent.csv')
destroyer1 = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/DestroyerPath15cent.csv')
# destroyer1 = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\DestroyerPath15cent_2.csv')
destroyer1['sensor'] = 104
destroyer1['velocity'] = 56

##warship Track
# destroyer2 = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\Destroyer33.csv')
destroyer2 = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/Destroyer3_r.csv')
destroyer2['sensor'] = 104
destroyer2['velocity'] = 56

##heli0 Track
# heli1 = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\heli72.csv')
heli1 = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/Heli_00.csv')
heli1['symbol'] = 'heliport'

# heli1 = pd.read_csv(r'C:/Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\heli72.csv')
heli00 = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/Heli_000.csv')


##heli1 Track
# heli_1 = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\Heli2cent.csv')

heli_1 = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/Heli_11.csv')
heli_1['symbol'] = 'heliport'
heli_1['altitude'] = np.where(heli_1['altitude']>=5000, 5000, heli_1['altitude'])


heli_2 = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/Heli_33.csv')
heli_2['symbol'] = 'heliport'

heli_2['altitude'] = heli_1['Altitude']
heli_2['sensor1'] = 100
heli_2['sensor2'] = 45
heli_2['velocity'] = 250
# heli_2['stationtime'] = 3.5

## p8 flight
p8flight = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/p8_72.csv')

## p8 flight Caribean
p8flight_car = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/P8car.csv')
p8flight_car['radar'] = 470
p8flight_car['velocity'] = 815


## p8 flight Pacific
p8flight_pac = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/P8pac_2.csv')


## My Fake
pathfake = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/Route_test.csv')

## Nueral MMO
nmmo72 = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Grids/72x72map.csv')

## Read in Caribean Target
# ctrack0 = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\CarribeanRoutes_Track2cent.csv')
# ais_all = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\AIS\ais_aall.csv')

ais_all = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/AIS/ais_paths3.csv')
ais_all.set_index('idx', inplace=True)
# ais_all.set_index('Unnamed: 0', inplace=True)
# ais_all['size'] = 5


# ctrack0 = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\CarribeanRoutes_all.csv')

# ctrack0 = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\car2cent.csv')
ctrack0 = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/car_moved_2.csv')
ctrack0.set_index('Unnamed: 0.1', inplace=True)
# ctrack0['size'] = 5
# ctrack0['symbol'] = 'circle'

## Read in Caribean Target
ctrack15 = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/CarribeanRoutes_Track15cent.csv')
ctrack15['detectsize'] = 1
ctrack15['detectsize'].loc[90:] = 19
ctrack15['color'] = '#6fa832'
ctrack15['color'].loc[104:] = '#f7d602'

## Read in Sail Drone
# sd = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization\synthetic_data\Routes\sd_car_all.csv')
sd = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/sd_line_c.csv')

sd.set_index('Unnamed: 0', inplace=True)

##Pac line 1
sd_1 = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/sd_line_p_1.csv')

sd_1.set_index('Unnamed: 0', inplace=True)

##Pac line 2
sd_2 = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/sd_line_p_2.csv')

sd_2.set_index('Unnamed: 0', inplace=True)


## Waves
waves = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Grids/waves72.csv')

## Cloud Ceiling
df_cloud_ceilings = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Grids/cloud_ceilings.csv')

## Cloud Ceiling
df_precipitations = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Grids/precipitations72.csv')


# df = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\route_full.csv')

# df = pathfake
N = 286
# N = 178


##Set radar size km enter
def radarsize(x):
    b = x/168 *30
    return b

def radarsizezoom(x):
    b = x/27 *18.5
    return b

# 25/26*28
# APS147 = use radar range func
heli_EO = 45
heli_EOpx = radarsize(heli_EO)

destroyer_AN = 104
destroyer_ANpx = radarsize(destroyer_AN)
destroyer_ANpxz = radarsizezoom(destroyer_AN)

p8_APY10 = 470
p8_APY10px = radarsize(p8_APY10)
p8_APY10pxz = radarsizezoom(p8_APY10)

heli_1['pxsize'] = radarsizezoom(heli_1['sensor1'])
heli_1['pxsize'] = np.where( heli_1['pxsize'] <= 6, 6, heli_1['pxsize'])


heli_1['pxsize2'] = radarsize(heli_1['sensor1'])
heli_1['pxsize2'] = np.where( heli_1['pxsize2'] <= 6, 6, heli_1['pxsize2'])
heli_1['pxsize3'] = heli_1['pxsize2'] * 1.5

heli_2['pxsize2'] = radarsize(heli_1['sensor1'])
heli_2['pxsize2'] = np.where( heli_1['pxsize2'] >= 6, 6, heli_1['pxsize2'])
heli_2['pxsize3'] = heli_2['pxsize2'] * 1.5

p8flight_car['rangesizez'] = radarsizezoom(470)
p8flight_car['rangesizez'] = np.where(p8flight_car['Longitude'] == p8flight_car['Longitude'].iloc[0], 5, p8flight_car['rangesizez'])
p8flight_car['rangesize2'] = p8flight_car['rangesize'] * 1.5
p8flight_pac['rangesize2'] = p8flight_pac['rangesize'] * 1.5

ptds['pxsize'] = radarsize(ptds['sensor'])

sd_rn = 18
sd_rn_px = radarsize(sd_rn)

ais_all['size'] = radarsize(30)

sd['size'] = 5
sd_1['size'] = 5
sd_2['size'] = 5

#Kevins Path
# df_rosa = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\rosa3.csv')
# df_rosa = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\rosa72.csv')

# df_rosa = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\PacRoutes_all.csv')
df_rosa = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/pac_moved.csv')
# df_rosa = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\pac2cent.csv')
df_rosa.set_index('Unnamed: 0.1', inplace=True)
df_rosa['color'] = '#d61111'

df_rosa2 = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/rosa72_part2.csv')

# df_rosa3 = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\pac2cent.csv')
df_rosa3 = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/pac_moved0.csv')
df_rosa3.set_index('Unnamed: 0.1', inplace=True)
df_rosa3['color'] = '#d61111'
## Daylight Data

df_daylight = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Navigability/twilights.csv')
# s2 = len(df_daylight)


####CP Solver

## X destroyers
## Y p8
## Z helis
### Sail_Drone
### PTDS

# cost_Sail_Drone = 1500000
# cost_PTDS = 600000000
# costx = 1800000000
# costy = 150000000
# costz = 10000000
# budgetmax = 5730000000


# class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
#     """Print intermediate solutions."""

#     def __init__(self, variables):
#         cp_model.CpSolverSolutionCallback.__init__(self)
#         self.__variables = variables
#         self.__solution_count = 0

#     def on_solution_callback(self):
#         self.__solution_count += 1
#         for v in self.__variables:
#             strings = ('%s=%i' % (v, self.Value(v)), end=' ')
#         # print()

#     def solution_count(self):
#         return self.__solution_count


# def SearchForAllSolutionsSampleSat():
#     """Showcases calling the solver to search for all solutions."""
#     # Creates the model.
#     model = cp_model.CpModel()

#     # Creates the variables.
#     var_upper_bound = max(50, 45, 37, 1000, 10)
#     x = model.NewIntVar(0, var_upper_bound, 'destroyer')
#     y = model.NewIntVar(0, var_upper_bound, 'p8')
    
#     # Need a helicopter for both seas
#     z = model.NewIntVar(2, var_upper_bound, 'SH-60')
    
#     Sail_Drone = model.NewIntVar(0, var_upper_bound, 'Sail_Drone')
    
#     PTDS = model.NewIntVar(3, var_upper_bound, 'PTDS')
    

#     #cost rule
#     model.Add(costx * x + costy * y + costz * z + cost_Sail_Drone * Sail_Drone + cost_PTDS * PTDS <= budgetmax)
    
#     #at least one destroyer per heli
#     model.Add(- x + z <= 0)

#     # Create a solver and solve.
#     solver = cp_model.CpSolver()
#     solution_printer = VarArraySolutionPrinter([x, y, z, Sail_Drone, PTDS])
#     # Enumerate all solutions.
#     solver.parameters.enumerate_all_solutions = True
#     # Solve.
#     status = solver.Solve(model, solution_printer)

#     return strings

#     # print('Status = %s' % solver.StatusName(status))
#     # print('Number of solutions found: %i' % solution_printer.solution_count())




##Add in airbases
trace_airbases = {

                "name": "Airbases", 
                "mode": "markers",
                "type": "scattermapbox",
                # "xsrc": "jacksonk:59:eefdd4", 
                "lat": airbases['Latitude'], 
                # "ysrc": "jacksonk:59:de0e34", 
                "lon": airbases['Longitude'], 
                "marker": {
                    "size": 8, 
                    "color": "rgb(255, 215, 0)",
                    'opacity' : 0.6
                    # "symbol": "asterisk-open"
                }, 
                "showlegend": True, 
                # "stackgroup": None
                }

##Add in ptds
trace_ptds = {

                "name": "Persistent Threat Detection System", 
                "mode": "markers",
                "type": "scattermapbox",
                # "xsrc": "jacksonk:59:eefdd4", 
                "lat": ptds['Latitude'], 
                # "ysrc": "jacksonk:59:de0e34", 
                "lon": ptds['Longitude'], 
                "marker": {
                    "size": ptds['pxsize'], 
                    "color": "rgb(218, 66, 245)",
                    'opacity' : 0.6
                    # "symbol": "asterisk-open"
                }, 
                "showlegend": True, 
                'legendgroup': 'assets',
                'legendgrouptitle' : dict( text = "Force Package"),
                # "stackgroup": None
                }





daylightchlor = { 
                            'type' : 'choroplethmapbox',
                            'name' : 'Daylight',
                            'z' : df_daylight['Daylight2'][df_daylight['time']==0],
                            'locations': df_daylight['ids'][df_daylight['time']==0],
                            'zmin': 0,
                            'zmax': 2,
                            'colorscale': [[0, 'rgba(0, 0, 0, 0.2)'], [1.0, 'rgba(236, 245, 66, 0.2)']],
                            # 'colorscale'='purp',
                            'colorbar':dict(thickness=20, ticklen=3),
                            'geojson': grid24df,
                            'legendgroup': "Dynamic Scenario Elements",  # this can be any string, not just "group"
                            'legendgrouptitle' : dict( text = "Dynamic Scenario Elements"),
                            'showlegend':True,
                            'showscale':False,
                            # 'text' : df_daylight['Daylight2'][df_daylight['time']==0],
                            # 'visible' =  "legendonly",
                            'hovertemplate': "Daylight (0-Night, 1-Twilight, 2-Day) : %{z}",
                            'marker_line_width':1, 
                            # marker_opacity=0.5
} 

fogchlor = {
                            'type' : 'choroplethmapbox',
                            'name' : 'Visibility',
                            'z': df_fogarray['Fog'][df_fogarray['time'] == 0],
                            'locations':df_fogarray['ids'][df_fogarray['time'] == 0],
                            'colorscale': [[0, 'rgba(2, 71, 156, 0.0)'], [1.0, 'rgba(250, 250, 250, 0.9)']],
                            # 'colorscale':'purp',
                            # 'colorbar':dict(thickness:20, ticklen:3),
                            'geojson': grid240df,
                            'legendgroup' : "Dynamic Scenario Elements",  # this can be any string, not just "group"
                            # legendgrouptitle :"Weather",
                            'showlegend':True,
                            'showscale':False,
                            'text' : df_fogarray['Fog'][df_fogarray['time'] == 0],
                            'visible' :  "legendonly",
                            'hovertemplate': "Visibility Rating (fog/rain) : %{z}",
                            'marker_line_width':0, 
                            # marker_opacity:0.5
}

ceilingchlor = {
                            'type' : 'choroplethmapbox',
                            'name' : 'Cloud Ceiling',
                            'z': df_fogarray['ceiling'][df_fogarray['time'] == 0],
                            'locations': df_fogarray['ids'][df_fogarray['time'] == 0],
                            'colorscale': [[0, 'rgba(255,255,255, 0.0)'], [0.05, 'rgba(227,238,245, 0.4)'], [0.5, 'rgba(157,186,217, 0.5)'], [1.0, 'rgba(113,25,117, 0.6)']],
                            # 'colorscale':'purp',
                            # 'colorbar':dict(thickness:20, ticklen:3),
                            'geojson': grid240df,
                            'legendgroup' : "Dynamic Scenario Elements", 
                            'legendgrouptitle' : dict( text = "Dynamic Scenario Elements"), # this can be any string, not just "group"
                            # legendgrouptitle :"Weather",
                            'showlegend':True,
                            'showscale':False,
                            # 'text' : df_ceilingarray['Radar Range'][df_ceilingarray['time'] == 0],
                            'visible' :  "legendonly",
                            'hovertemplate': "Ceiling Altitude (ft) : %{z}",
                            'marker_line_width':0, 
                            # 'customdata' : np.stack((df['velocity'], df['heading'], df['freeboard']), axis=-1),
                            # 'hovertemplate': "<br>".join([
                            #     "Velocity (km/hr) : %{customdata[0]}",
                            #     "Heading (degrees) : %{customdata[1]}",
                            #     "Freeboard (kgs load) : %{customdata[2]}",
                            # marker_opacity:0.5
}

ceilingrangechlor = {
                            'type' : 'choroplethmapbox',
                            'name' : 'Cloud Ceiling Range',
                            'z': df_fogarray['Radar Range'][df_fogarray['time'] == 0],
                            'locations':df_fogarray['ids'][df_fogarray['time'] == 0],
                            'colorscale': [[0, 'rgba(255,255,255, 0.0)'], [0.05, 'rgba(227,238,245, 0.4)'], [0.5, 'rgba(157,186,217, 0.5)'], [1.0, 'rgba(113,25,117, 0.6)']],
                            # 'colorscale':'purp',
                            # 'colorbar':dict(thickness:20, ticklen:3),
                            'geojson': grid240df,
                            'legendgroup' : "Dynamic Scenario Elements",  # this can be any string, not just "group"
                            # legendgrouptitle :"Weather",
                            'showlegend':True,
                            'showscale':False,
                            # 'text' : df_ceilingarray['Radar Range'][df_ceilingarray['time'] == 0],
                            'visible' :  "legendonly",
                            'hovertemplate': "Radar Range (km) : %{z}",
                            'marker_line_width':0, 

}




originchlor = {
                            'type' : 'choroplethmapbox',
                            'name' : 'Origins',
                            'z': df_griddata['Origin'],
                            'locations':df_griddata['ids'],
                            'colorscale': [[0, 'rgba(168, 192, 247, 0.0)'], [1.0, 'rgba(0, 255, 0, 0.9)']],
                            # 'colorscale':'purp',
                            'colorbar':dict(thickness=20, ticklen=3),
                            'geojson': grid240df,
                            'showlegend':True,
                            'showscale':False,
                            'legendgroup':"Navigation",
                            'text' : df_griddata['Origin'],
                            # visible :  "legendonly",
                            'hoverinfo':'skip',
                            'marker_line_width':0.2, 
                            # marker_opacity:0.5
}

destinationchlor = {
                            'type' : 'choroplethmapbox',
                            'name' : 'Destinations',
                            'z': df_griddata['Destination'],
                            'locations':df_griddata['ids'],
                            'colorscale': [[0, 'rgba(168, 192, 247, 0.0)'], [1.0, 'rgba(238, 56, 255, 0.9)']],
                            # 'colorscale':'purp',
                            # 'colorbar':dict(thickness:20, ticklen:3),
                            'geojson': grid240df,
                            'showlegend':True,
                            'showscale':False,
                            'legendgroup':"Navigation",
                            'text' : df_griddata['Destination'],
                            # visible :  "legendonly",
                            'hoverinfo':'skip',
                            'marker_line_width':0.2, 
                            # marker_opacity:0.5
}




waveschlor = {
                            'type' : 'choroplethmapbox',
                            'name' : 'Sea State',
                            'z': waves['height'],
                            'locations': waves['ids'],
                            # 'colorscale':'jet',
                            'colorscale':[[0, 'rgba(4,115,255, 0.1)'], [1.0, 'rgba(254,41,147, 0.9)']],
                            # 'colorscale':[[0, 'rgba(4,115,255,0.1)'], [0.6, 'rgba(147,7,0,0.7)'], [0.7, 'rgba(118,0,60,0.8)'], [1.0, 'rgba(254,41,147,0.8)']],
                            # 'colorbar':dict(thickness:20, ticklen:3),
                            'geojson': grid240df,
                            'legendgroup':"Dynamic Scenario Elements",
                            'legendgrouptitle' : dict( text = "Dynamic Scenario Elements"),  # this can be any string, not just "group"
                            # legendgrouptitle:"Supplemental Data",
                            'showlegend':True,
                            'showscale':False,
                            # 'text' : waves['text'],
                            'visible' :  "legendonly",
                            'hovertemplate': "Wave Height (ft) : %{z}",
                            # 'hoverinfo':'all',
                            'marker_line_width':0, 
                            # marker_opacity:0.5
}

cloud_ceiling_chlor = {
                            'type' : 'choroplethmapbox',
                            'name' : 'Cloud Ceiling',
                            'z': df_cloud_ceilings['Altitude'],
                            'locations': df_cloud_ceilings['ids'],
                            # 'colorscale':'jet',
                            # 'colorscale': [[0, 'rgba(255,255,255, 0.4)'], [0.05, 'rgba(227,238,245, 0.4)'], [0.5, 'rgba(157,186,217, 0.5)'], [1.0, 'rgba(113,25,117, 0.0)']],
                            'colorscale': [[0, 'rgba(255,255,255, 0.6)'],   [0.6, 'rgba(113,25,117, 0.4)'], [1.0, 'rgba(113,25,117, 0.0)']],
                            # 'colorscale':[[0, 'rgba(4,115,255, 0.1)'], [1.0, 'rgba(254,41,147, 0.9)']],
                            # 'colorscale':[[0, 'rgba(4,115,255,0.1)'], [0.6, 'rgba(147,7,0,0.7)'], [0.7, 'rgba(118,0,60,0.8)'], [1.0, 'rgba(254,41,147,0.8)']],
                            # 'colorbar':dict(thickness:20, ticklen:3),
                            'geojson': grid240df,
                            'legendgroup':"Dynamic Scenario Elements",  # this can be any string, not just "group"
                            # legendgrouptitle:"Supplemental Data",
                            'showlegend':True,
                            'showscale':False,
                            # 'text' : waves['text'],
                            'visible' :  "legendonly",
                            'hovertemplate': "Cloud Ceiling (ft) : %{z}",
                            # 'hoverinfo':'all',
                            'marker_line_width':0, 
                            # marker_opacity:0.5
}

precipitation_chlor = {
                            'type' : 'choroplethmapbox',
                            'name' : 'Precipitation',
                            'z': df_precipitations['Precipitation'],
                            'locations': df_precipitations['ids'],
                            # 'colorscale':'jet',
                            # 'colorscale': [[0, 'rgba(255,255,255, 0.4)'], [0.05, 'rgba(227,238,245, 0.4)'], [0.5, 'rgba(157,186,217, 0.5)'], [1.0, 'rgba(113,25,117, 0.0)']],
                            'colorscale': [[0, 'rgba(255,255,255, 0.0)'],   [0.5, 'rgba(2, 247, 6, 0.4)'], [1.0, 'rgba(0, 125, 2, 0.8)']],
                            # 'colorscale':[[0, 'rgba(4,115,255, 0.1)'], [1.0, 'rgba(254,41,147, 0.9)']],
                            # 'colorscale':[[0, 'rgba(4,115,255,0.1)'], [0.6, 'rgba(147,7,0,0.7)'], [0.7, 'rgba(118,0,60,0.8)'], [1.0, 'rgba(254,41,147,0.8)']],
                            # 'colorbar':dict(thickness:20, ticklen:3),
                            'geojson': grid240df,
                            'legendgroup':"Dynamic Scenario Elements",  # this can be any string, not just "group"
                            # legendgrouptitle:"Supplemental Data",
                            'showlegend':True,
                            'showscale':False,
                            # 'text' : waves['text'],
                            'visible' :  "legendonly",
                            'hovertemplate': "Precipitation : %{z}",
                            # 'hoverinfo':'all',
                            'marker_line_width':0, 
                            # marker_opacity:0.5
}

###SAIL DRONE CARRIBEAN
trace_sdcar = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Sail Drone Network Carribean', 
         'lon': sd.loc[0, 'Longitude'].tolist(), 
         'lat': sd.loc[0, 'Latitude'].tolist(), 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': sd.loc[0,'size'].tolist(), 
                    'color': '#03fc29',
                    # 'colorscale': 'reds',
                    # 'cmin' : 0,
                    # 'cmax' : 4200,
                    'opacity' : 0.7,
                    # 'symbol' : [ctrack0.loc[0,'symbol']],
                    # 'color': [rltracks1200.loc[rltracks1200['time'] == 0, 'rank']]
                    },
         'mode': "markers",
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
}

###SAIL DRONE CARRIBEAN
trace_sdpac1 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Sail Drone Network Pacific 1', 
         'lon': sd_1.loc[0, 'Longitude'].tolist(), 
         'lat': sd_1.loc[0, 'Latitude'].tolist(), 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': sd_1.loc[0,'size'].tolist(), 
                    'color': '#03fc29',
                    # 'colorscale': 'reds',
                    # 'cmin' : 0,
                    # 'cmax' : 4200,
                    'opacity' : 0.7,
                    # 'symbol' : [ctrack0.loc[0,'symbol']],
                    # 'color': [rltracks1200.loc[rltracks1200['time'] == 0, 'rank']]
                    },
         'mode': "markers",
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
}

###SAIL DRONE CARRIBEAN
trace_sdpac2 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Sail Drone Network Pacific 2', 
         'lon': sd_2.loc[0, 'Longitude'].tolist(), 
         'lat': sd_2.loc[0, 'Latitude'].tolist(), 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': sd_2.loc[0,'size'].tolist(), 
                    'color': '#03fc29',
                    # 'colorscale': 'reds',
                    # 'cmin' : 0,
                    # 'cmax' : 4200,
                    'opacity' : 0.7,
                    # 'symbol' : [ctrack0.loc[0,'symbol']],
                    # 'color': [rltracks1200.loc[rltracks1200['time'] == 0, 'rank']]
                    },
         'mode': "markers",
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
}



trace_ctrack0 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Target - Carribean', 
         'lon': ctrack0.loc[0, 'Longitude'].tolist(), 
         'lat': ctrack0.loc[0, 'Latitude'].tolist(), 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': ctrack0.loc[0,'size'].tolist(), 
                    'color': ctrack0.loc[0,'color'].tolist(),
                    # 'colorscale': 'reds',
                    # 'cmin' : 0,
                    # 'cmax' : 4200,
                    'opacity' : 0.9,
                    # 'symbol' : [ctrack0.loc[0,'symbol']],
                    # 'color': [rltracks1200.loc[rltracks1200['time'] == 0, 'rank']]
                    },
         'mode': "markers",
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'targets',
         'legendgrouptitle' : dict( text = "Target Characteristics"),
         'showlegend': True, 
}

trace_ctrack0z = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Target - Carribean', 
         'lon': ctrack0.loc[80, 'Longitude'].tolist(), 
         'lat': ctrack0.loc[80, 'Latitude'].tolist(), 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': ctrack0.loc[0,'size'].tolist(), 
                    'color': '#ff3030',
                    # 'colorscale': 'reds',
                    # 'cmin' : 0,
                    # 'cmax' : 4200,
                    'opacity' : 0.9,
                    # 'symbol' : [ctrack0.loc[0,'symbol']],
                    # 'color': [rltracks1200.loc[rltracks1200['time'] == 0, 'rank']]
                    },
         'mode': "markers",
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'targets',
         'legendgrouptitle' : dict( text = "Target Characteristics"),
         'showlegend': True, 
}

trace_ctrack15 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Target - Carribean 2', 
         'lon': [ctrack15.loc[0, 'Longitude']], 
         'lat': [ctrack15.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 6, 
                    'color': '#ff3030',
                    # 'colorscale': 'reds',
                    # 'cmin' : 0,
                    # 'cmax' : 4200,
                    'opacity' : 0.9,
                    # 'symbol' : [rltracks3999.loc[0, 'symbol']]
                    # 'color': [rltracks1200.loc[rltracks1200['time'] == 0, 'rank']]
                    },
         'mode': "markers",
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'targets',
         'legendgrouptitle' : dict( text = "Target Characteristics"),
         'showlegend': True,
         'legendrank': 3, 
}

trace_ctrack15z = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Target - Carribean 2', 
         'lon': [ctrack15.loc[80, 'Longitude']], 
         'lat': [ctrack15.loc[80, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 6, 
                    'color': '#ff3030',
                    # 'colorscale': 'reds',
                    # 'cmin' : 0,
                    # 'cmax' : 4200,
                    'opacity' : 0.9,
                    # 'symbol' : [rltracks3999.loc[0, 'symbol']]
                    # 'color': [rltracks1200.loc[rltracks1200['time'] == 0, 'rank']]
                    },
         'mode': "markers",
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'targets',
         'legendgrouptitle' : dict( text = "Target Characteristics"),
         'showlegend': True,
         'legendrank': 3, 
}

trace_ctrack15detect = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Detection', 
         'lon': [ctrack15.loc[0, 'Longitude']], 
         'lat': [ctrack15.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': [ctrack15.loc[0, 'detectsize']], 
                    'color': '#6fa832',
                    # 'colorscale': 'reds',
                    # 'cmin' : 0,
                    # 'cmax' : 4200,
                    'opacity' : 0.7,
                    # 'symbol' : [rltracks3999.loc[0, 'symbol']]
                    # 'color': [rltracks1200.loc[rltracks1200['time'] == 0, 'rank']]
                    },
         'mode': "markers",
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'targets',
         'legendgrouptitle' : dict( text = "Target Characteristics"),
         'showlegend': False, 
        
}

trace_ctrack15detectz = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Detection', 
         'lon': [ctrack15.loc[80, 'Longitude']], 
         'lat': [ctrack15.loc[80, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': [ctrack15.loc[80, 'detectsize']], 
                    'color': '#6fa832',
                    # 'colorscale': 'reds',
                    # 'cmin' : 0,
                    # 'cmax' : 4200,
                    'opacity' : 0.7,
                    # 'symbol' : [rltracks3999.loc[0, 'symbol']]
                    # 'color': [rltracks1200.loc[rltracks1200['time'] == 0, 'rank']]
                    },
         'mode': "markers",
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'targets',
         'legendgrouptitle' : dict( text = "Target Characteristics"),
         'showlegend': False, 
        
}


tracerosabase = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Target Pacific', 
         'lon': df_rosa.loc[0, 'Longitude'].tolist(), 
         'lat': df_rosa.loc[0, 'Latitude'].tolist(), 
        #  'hoverinfo': 'name+text', 
         'marker': {
                    'size': df_rosa.loc[0, 'size'].tolist(),
                    'color': df_rosa.loc[0, 'color'].tolist(),
                    },
         'mode': 'markers', 
         'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'targets',
         'legendgrouptitle' : dict( text = "Target Characteristics"),
         'showlegend': True, 
        #  'customdata' : [df['heading'], df['heading'], df['freeboard']],
        #  'customdata' : np.stack((df_rosa['velocity'], df_rosa['heading'], df_rosa['freeboard']), axis=-1),
        #  'hovertemplate': "<br>".join([
        #                     "Velocity (km/hr) : %{customdata[0]}",
        #                     "Heading (degrees) : %{customdata[1]}",
        #                     "Freeboard (kgs load) : %{customdata[2]}",
        #  ])
}

tracerosabase3 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Target Pacific', 
         'lon': df_rosa3.loc[0, 'Longitude'].tolist(), 
         'lat': df_rosa.loc[0, 'Latitude'].tolist(), 
        #  'hoverinfo': 'name+text', 
         'marker': {
                    'size': df_rosa3.loc[0, 'size'].tolist(),
                    'color': df_rosa3.loc[0, 'color'].tolist(),
                    },
         'mode': 'markers', 
         'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'targets',
         'legendgrouptitle' : dict( text = "Target Characteristics"),
         'showlegend': True, 
        #  'customdata' : [df['heading'], df['heading'], df['freeboard']],
        #  'customdata' : np.stack((df_rosa['velocity'], df_rosa['heading'], df_rosa['freeboard']), axis=-1),
        #  'hovertemplate': "<br>".join([
        #                     "Velocity (km/hr) : %{customdata[0]}",
        #                     "Heading (degrees) : %{customdata[1]}",
        #                     "Freeboard (kgs load) : %{customdata[2]}",
        #  ])
}

tracerosa2 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Target Z', 
         'lon': [df_rosa2.loc[0, 'Longitude']], 
         'lat': [df_rosa2.loc[0, 'Latitude']], 
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 6, 'color':'#cc0000'},
         'mode': 'markers', 
         'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'targets',
         'legendgrouptitle' : dict( text = "Target Characteristics"),
         'showlegend': True, 
        #  'customdata' : [df['heading'], df['heading'], df['freeboard']],
         'customdata' : np.stack((df_rosa2['velocity'], df_rosa2['heading'], df_rosa2['freeboard']), axis=-1),
         'hovertemplate': "<br>".join([
                            "Velocity (km/hr) : %{customdata[0]}",
                            "Heading (degrees) : %{customdata[1]}",
                            "Freeboard (kgs load) : %{customdata[2]}",
         ])
}

trace_warship = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Destroyer 0', 
         'lon': [warship.loc[0, 'Longitude']], 
         'lat': [warship.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 18.5, 
                    'color': '#348feb',
                    'opacity' : 0.5
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
        'customdata' : np.stack((warship['sensor'], warship['velocity']), axis=-1),
         'hovertemplate': "<br>".join([
                            "AN/SPS0 67 radar range (km) : %{customdata[0]}",
                            "Cruising Speed (km/hr) : %{customdata[1]}"
                            ])
}


trace_destroyer0 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Destroyer 0', 
         'lon': [destroyer0.loc[0, 'Longitude']], 
         'lat': [destroyer0.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 18.5, 
                    'color': '#348feb',
                    'opacity' : 0.5
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
        'customdata' : np.stack((destroyer0['sensor'], destroyer0['velocity']), axis=-1),
         'hovertemplate': "<br>".join([
                            "AN/SPS0 67 radar range (km) : %{customdata[0]}",
                            "Cruising Speed (km/hr) : %{customdata[1]}"
                            ])
}


trace_warship_5 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Destroyer 0', 
         'lon': [warship.loc[0, 'Longitude']], 
         'lat': [warship.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 18.5*1.5, 
                    'color': '#348feb',
                    'opacity' : 0.5
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
        'customdata' : np.stack((warship['sensor'], warship['velocity']), axis=-1),
         'hovertemplate': "<br>".join([
                            "AN/SPS0 67 radar range (km) : %{customdata[0]}",
                            "Cruising Speed (km/hr) : %{customdata[1]}"
                            ])
}

trace_destroyer1 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Destroyer 1', 
         'lon': [destroyer1.loc[0, 'Longitude']], 
         'lat': [destroyer1.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': destroyer_ANpx, 
                    'color': '#348feb',
                    'opacity' : 0.5
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
         'customdata' : np.stack((destroyer1['sensor'], destroyer1['velocity']), axis=-1),
         'hovertemplate': "<br>".join([
                            "AN/SPS0 67 radar range (km) : %{customdata[0]}",
                            "Cruising Speed (km/hr) : %{customdata[1]}"
                            ])
 
}

trace_destroyer1_5 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Destroyer 1', 
         'lon': [destroyer1.loc[0, 'Longitude']], 
         'lat': [destroyer1.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': destroyer_ANpx*1.5, 
                    'color': '#348feb',
                    'opacity' : 0.5
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
         'customdata' : np.stack((destroyer1['sensor'], destroyer1['velocity']), axis=-1),
         'hovertemplate': "<br>".join([
                            "AN/SPS0 67 radar range (km) : %{customdata[0]}",
                            "Cruising Speed (km/hr) : %{customdata[1]}"
                            ])
 
}

trace_destroyer1z = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Destroyer 1', 
         'lon': [destroyer1.loc[80, 'Longitude']], 
         'lat': [destroyer1.loc[80, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': destroyer_ANpxz, 
                    'color': '#348feb',
                    'opacity' : 0.5
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
         'customdata' : np.stack((destroyer1['sensor'], destroyer1['velocity']), axis=-1),
         'hovertemplate': "<br>".join([
                            "AN/SPS0 67 radar range (km) : %{customdata[0]}",
                            "Cruising Speed (km/hr) : %{customdata[1]}"
                            ])
 
}

trace_destroyer2 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Destroyer 2', 
         'lon': [destroyer2.loc[0, 'Longitude']], 
         'lat': [destroyer2.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': destroyer_ANpx, 
                    'color': '#348feb',
                    'opacity' : 0.5
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
         'customdata' : np.stack((destroyer2['sensor'], destroyer2['velocity']), axis=-1),
         'hovertemplate': "<br>".join([
                            "AN/SPS0 67 radar range (km) : %{customdata[0]}",
                            "Cruising Speed (km/hr) : %{customdata[1]}"
                            ])
 
}

trace_destroyer2_5 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Destroyer 2', 
         'lon': [destroyer2.loc[0, 'Longitude']], 
         'lat': [destroyer2.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': destroyer_ANpx*1.5, 
                    'color': '#348feb',
                    'opacity' : 0.5
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
         'customdata' : np.stack((destroyer2['sensor'], destroyer2['velocity']), axis=-1),
         'hovertemplate': "<br>".join([
                            "AN/SPS0 67 radar range (km) : %{customdata[0]}",
                            "Cruising Speed (km/hr) : %{customdata[1]}"
                            ])
 
}

trace_heli = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Helicopter 0', 
         'lon': [heli1.loc[0, 'Longitude']], 
         'lat': [heli1.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 7, 
                    'color': '#9842f5',
                    'opacity' : 0.9,
                    # 'symbol' : [heli1.loc[0, 'symbol']]
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
}

trace_heli00 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Helicopter 0', 
         'lon': [heli00.loc[0, 'Longitude']], 
         'lat': [heli00.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 7, 
                    'color': '#9842f5',
                    'opacity' : 0.9,
                    # 'symbol' : [heli1.loc[0, 'symbol']]
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
}

trace_heli_5 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Helicopter 0', 
         'lon': [heli1.loc[0, 'Longitude']], 
         'lat': [heli1.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 7*1.5, 
                    'color': '#9842f5',
                    'opacity' : 0.9,
                    # 'symbol' : [heli1.loc[0, 'symbol']]
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
}

trace_heli_1 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Helicopter 1', 
         'lon': [heli_1.loc[0, 'Longitude']], 
         'lat': [heli_1.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': [heli_1.loc[0,'pxsize2']], 
                    'color': '#f77c02',
                    'opacity' : 0.7,
                    # 'symbol' : [heli1.loc[0, 'symbol']]
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
         'legendrank': 2,
         'customdata' : np.stack((heli_1['altitude'].iloc[0:1], heli_1['sensor1'].iloc[0:1], heli_1['sensor2'].iloc[0:1], heli_1['velocity'].iloc[0:1], heli_1['stationtime'].iloc[0:1]), axis=-1),
         'hovertemplate': "<br>".join([
                            "Altitude (ft) : %{customdata[0]}",
                            "APS-147 Radar (km) : %{customdata[1]}",
                            "AAS-44 MS Targeting System (km) : %{customdata[2]}",
                            "Cruising Speed (km/hr) : %{customdata[3]}",
                            "Time Left on Station (hr) : %{customdata[4]}"
                            ])
}

trace_heli_1_5 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Helicopter 1', 
         'lon': [heli_1.loc[0, 'Longitude']], 
         'lat': [heli_1.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': [heli_1.loc[0,'pxsize3']], 
                    'color': '#f77c02',
                    'opacity' : 0.7,
                    # 'symbol' : [heli1.loc[0, 'symbol']]
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
         'legendrank': 2,
         'customdata' : np.stack((heli_1['altitude'].iloc[0:1], heli_1['sensor1'].iloc[0:1], heli_1['sensor2'].iloc[0:1], heli_1['velocity'].iloc[0:1], heli_1['stationtime'].iloc[0:1]), axis=-1),
         'hovertemplate': "<br>".join([
                            "Altitude (ft) : %{customdata[0]}",
                            "APS-147 Radar (km) : %{customdata[1]}",
                            "AAS-44 MS Targeting System (km) : %{customdata[2]}",
                            "Cruising Speed (km/hr) : %{customdata[3]}",
                            "Time Left on Station (hr) : %{customdata[4]}"
                            ])
}

trace_heli_2 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Helicopter 2', 
         'lon': [heli_2.loc[0, 'Longitude']], 
         'lat': [heli_2.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': [heli_2.loc[0,'pxsize2']], 
                    'color': '#f77c02',
                    'opacity' : 0.7,
                    # 'symbol' : [heli1.loc[0, 'symbol']]
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
         'legendrank': 2,
         'customdata' : np.stack((heli_2['altitude'].iloc[0:1], heli_2['sensor1'].iloc[0:1], heli_2['sensor2'].iloc[0:1], heli_2['velocity'].iloc[0:1], heli_2['stationtime'].iloc[0:1]), axis=-1),
         'hovertemplate': "<br>".join([
                            "Altitude (ft) : %{customdata[0]}",
                            "APS-147 Radar (km) : %{customdata[1]}",
                            "AAS-44 MS Targeting System (km) : %{customdata[2]}",
                            "Cruising Speed (km/hr) : %{customdata[3]}",
                            "Time Left on Station (hr) : %{customdata[4]}"
                            ])
}

trace_heli_2_5 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Helicopter 2', 
         'lon': [heli_2.loc[0, 'Longitude']], 
         'lat': [heli_2.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': [heli_2.loc[0,'pxsize3']], 
                    'color': '#f77c02',
                    'opacity' : 0.7,
                    # 'symbol' : [heli1.loc[0, 'symbol']]
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
         'legendrank': 2,
         'customdata' : np.stack((heli_2['altitude'].iloc[0:1], heli_2['sensor1'].iloc[0:1], heli_2['sensor2'].iloc[0:1], heli_2['velocity'].iloc[0:1], heli_2['stationtime'].iloc[0:1]), axis=-1),
         'hovertemplate': "<br>".join([
                            "Altitude (ft) : %{customdata[0]}",
                            "APS-147 Radar (km) : %{customdata[1]}",
                            "AAS-44 MS Targeting System (km) : %{customdata[2]}",
                            "Cruising Speed (km/hr) : %{customdata[3]}",
                            "Time Left on Station (hr) : %{customdata[4]}"
                            ])
}

trace_heli_1z = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Helicopter 1', 
         'lon': [heli_1.loc[80, 'Longitude']], 
         'lat': [heli_1.loc[80, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': [heli_1.loc[0,'pxsize']], 
                    'color': '#f77c02',
                    'opacity' : 0.7,
                    # 'symbol' : [heli1.loc[0, 'symbol']]
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
         'legendrank': 2,
         'customdata' : np.stack((heli_1['altitude'].iloc[0:1], heli_1['sensor1'].iloc[0:1], heli_1['sensor2'].iloc[0:1], heli_1['velocity'].iloc[0:1], heli_1['stationtime'].iloc[0:1]), axis=-1),
         'hovertemplate': "<br>".join([
                            "Altitude (ft) : %{customdata[0]}",
                            "APS-147 Radar (km) : %{customdata[1]}",
                            "AAS-44 MS Targeting System (km) : %{customdata[2]}",
                            "Cruising Speed (km/hr) : %{customdata[3]}",
                            "Time Left on Station (hr) : %{customdata[4]}"
                            ])
}

trace_heli_11 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Helicopter 1_', 
         'lon': [heli_1.loc[0, 'Longitude']], 
         'lat': [heli_1.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 8, 
                    'color': '#9842f5',
                    'opacity' : 0.7,
                    # 'symbol' : [heli1.loc[0, 'symbol']]
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': False, 
         'legendrank': 200000,

}

trace_heli_11z = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Helicopter 1_', 
         'lon': [heli_1.loc[80, 'Longitude']], 
         'lat': [heli_1.loc[80, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 8, 
                    'color': '#9842f5',
                    'opacity' : 0.7,
                    # 'symbol' : [heli1.loc[0, 'symbol']]
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': False, 
         'legendrank': 200000,

}

trace_p8 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'P8 Flight', 
         'lon': [p8flight.loc[0, 'Longitude']], 
         'lat': [p8flight.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': p8_APY10px, 
                    'color': '#59e2f7',
                    'opacity' : 0.8
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
        #  'customdata' : np.stack((destroyer1['sensor'], destroyer1['velocity']), axis=-1),
        #  'hovertemplate': "<br>".join([
        #                     "AN/SPS0 67 radar range (km) : %{customdata[0]}",
        #                     "Cruising Speed (km/hr) : %{customdata[1]}"
        #                     ])
}

trace_p8_5 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'P8 Flight', 
         'lon': [p8flight.loc[0, 'Longitude']], 
         'lat': [p8flight.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': p8_APY10px*1.5, 
                    'color': '#59e2f7',
                    'opacity' : 0.8
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
        #  'customdata' : np.stack((destroyer1['sensor'], destroyer1['velocity']), axis=-1),
        #  'hovertemplate': "<br>".join([
        #                     "AN/SPS0 67 radar range (km) : %{customdata[0]}",
        #                     "Cruising Speed (km/hr) : %{customdata[1]}"
        #                     ])
}

trace_p8z = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'P8 Flight', 
         'lon': [p8flight.loc[0, 'Longitude']], 
         'lat': [p8flight.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': p8_APY10px, 
                    'color': '#59e2f7',
                    'opacity' : 0.8
                    },
         'mode': 'markers', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
}

trace_p8_car = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'P8 Flight Carib', 
         'lon': [p8flight_car.loc[0, 'Longitude']], 
         'lat': [p8flight_car.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': [p8flight_car.loc[0, 'rangesize']], 
                    'color': '#59e2f7',
                    'opacity' : 0.8
                    },
         'mode': 'markers+lines', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
         'customdata' : np.stack((p8flight_car['radar'], p8flight_car['velocity']), axis=-1),
         'hovertemplate': "<br>".join([
                            "AN/APY radar range (km) : %{customdata[0]}",
                            "Velocity (km/hr) : %{customdata[1]}"
                            ])
}

trace_p8_car_5 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'P8 Flight Carib', 
         'lon': [p8flight_car.loc[0, 'Longitude']], 
         'lat': [p8flight_car.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': [p8flight_car.loc[0, 'rangesize2']], 
                    'color': '#59e2f7',
                    'opacity' : 0.8
                    },
         'mode': 'markers+lines', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
         'customdata' : np.stack((p8flight_car['radar'], p8flight_car['velocity']), axis=-1),
         'hovertemplate': "<br>".join([
                            "AN/APY radar range (km) : %{customdata[0]}",
                            "Velocity (km/hr) : %{customdata[1]}"
                            ])
}

trace_p8_pac = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'P8 Flight Pacific', 
         'lon': [p8flight_pac.loc[0, 'Longitude']], 
         'lat': [p8flight_pac.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': [p8flight_pac.loc[0, 'rangesize']], 
                    'color': '#59e2f7',
                    'opacity' : 0.8
                    },
         'mode': 'markers+lines', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
}

trace_p8_pac_5 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'P8 Flight Pacific', 
         'lon': [p8flight_pac.loc[0, 'Longitude']], 
         'lat': [p8flight_pac.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': [p8flight_pac.loc[0, 'rangesize2']], 
                    'color': '#59e2f7',
                    'opacity' : 0.8
                    },
         'mode': 'markers+lines', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
}

trace_p8_carz = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'P8 Flight Carib', 
         'lon': [p8flight_car.loc[80, 'Longitude']], 
         'lat': [p8flight_car.loc[80, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': [p8flight_car.loc[0, 'rangesizez']], 
                    'color': '#59e2f7',
                    'opacity' : 0.8
                    },
         'mode': 'markers+lines', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'assets',
         'legendgrouptitle' : dict( text = "Force Package"),
         'showlegend': True, 
}




traceneuralmap={
        'type': 'choroplethmapbox',
        'name' : 'Navigability 72 x 72',
        'z': nmmo72['Land'],
        'locations':nmmo72['ids'],
        'colorscale': [[0, 'rgba(82, 109, 242, 0.1)'], [1.0, 'rgba(0, 107, 7, 0.6)']],
        # 'colorscale'='purp',
        'colorbar':dict(thickness=20, ticklen=3),
        'geojson': grid240df,
        'legendgroup' : "Navigation", 
        'legendgrouptitle' : dict( text = "Geographic Factors"), 
        # legendgrouptitle_'text'="Navigation",
        'showlegend':True,
        'showscale':False,
        'text' : nmmo72['map_tiles'],
        'legendrank': 1,
        'hoverinfo':'all',
#                             'text'='text',
        # 'hoverinfo':'skip',
        'marker_line_width':0.2, 
        # marker_opacity=0.5
} 

## AIS Moving
trace_aism = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'AIS Bounty', 
         'lon': ais_all.loc[0, 'Longitude'].tolist(), 
         'lat': ais_all.loc[0, 'Latitude'].tolist(), 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': ais_all.loc[0,'size'].tolist(), 
                    'color': '#03fccf',
                    # 'colorscale': 'reds',
                    # 'cmin' : 0,
                    # 'cmax' : 4200,
                    'opacity' : 0.9,
                    # 'symbol' : [ctrack0.loc[0,'symbol']],
                    # 'color': [rltracks1200.loc[rltracks1200['time'] == 0, 'rank']]
                    },
         'mode': "markers",
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'bluetargets',
         'legendgrouptitle' : dict( text = "Blue Force"),
         'showlegend': True, 
}


layoutz = dict(
            template= "plotly_dark",
            height=600,
    
            mapbox=dict(accesstoken=mapbox_access_token,
                              bearing=0,
                            #   center=dict(lat=3.5,
                            #                 lon=-95),
                              center=dict(lat=12.375,
                                            lon=-79.375),
                                            
                              pitch=0,
                              zoom=5.8,
                              style='satellite'),
            legend=dict(
                        title = 'Environment Variables',
                        yanchor="bottom",
                        y=0.05,
                        xanchor="left",
                        x=0.01,
                        groupclick = "toggleitem",
                    ),
            margin= {
                    "b": 5, 
                    "l": 5, 
                    "r": 5, 
                    "t": 5
                }
)


framesz = [dict(name=k,
               data=[



                    dict(
                           type= "scattermapbox",
                           lat= [heli_1.loc[k, 'Latitude']], 
                           lon= [heli_1.loc[k, 'Longitude']],
                           marker=dict( size = [heli_1.loc[k,'pxsize']]),

                            customdata = np.stack((heli_1['altitude'].iloc[k:k+1], heli_1['sensor1'].iloc[k:k+1], heli_1['sensor2'].iloc[k:k+1], heli_1['velocity'].iloc[k:k+1], heli_1['stationtime'].iloc[k:k+1]), axis=-1),
                            hovertemplate = "<br>".join([
                                                            "Altitude (ft) : %{customdata[0]}",
                                                            "APS-147 Radar (km) : %{customdata[1]}",
                                                            "AAS-44 MS Targeting System (km) : %{customdata[2]}",
                                                            "Cruising Speed (km/hr) : %{customdata[3]}",
                                                            "Time Left on Station (hr) : %{customdata[4]}"
                                                            ])
                        #    marker=dict( symbol = [heli1.loc[k, 'symbol']])
                           ),
                    dict(
                           type= "scattermapbox",
                           lat= [heli_1.loc[k, 'Latitude']], 
                           lon= [heli_1.loc[k, 'Longitude']],
                           ),
                    dict(
                           type= "scattermapbox",
                           lat= [destroyer1.loc[k, 'Latitude']], 
                           lon= [destroyer1.loc[k, 'Longitude']]),


                    dict(
                           type= "scattermapbox",
                           lat= [p8flight_car.loc[k, 'Latitude']], 
                           lon= [p8flight_car.loc[k, 'Longitude']],
                           marker=dict(
                                        size = [p8flight_car.loc[k, 'rangesizez']], 
                                        # 'color': [rltracks3600.loc[0, 'rank']],
                                        # 'colorscale': 'reds',
                                        # 'cmin' : 0,
                                        # 'cmax' : 4200,
                                        # 'opacity' : 0.4
                          )
                           ),

                    dict(
                           type= "scattermapbox",
                           lat=ctrack0.loc[k, 'Latitude'].tolist(), 
                           lon=ctrack0.loc[k, 'Longitude'].tolist(),
                           marker={ 
                                        # 'symbol' : [ctrack0.loc[k, 'symbol']],
                                        'size': ctrack0.loc[k, 'size'].tolist(), 
                                        'color': '#ff3030',
                                     
                           }
                           ),

                    # dict(
                    #        type= "scattermapbox",
                    #        lat=[ctrack15.loc[k, 'Latitude']], 
                    #        lon=[ctrack15.loc[k, 'Longitude']],
                    #        marker={ 

                    #                     'size': [ctrack15.loc[k, 'detectsize']], 
                    #                     'color': [ctrack15.loc[k, 'color']],
                                     
                    #        }
                    #        ),                           
                    # dict(
                    #        type= "scattermapbox",
                    #        lat=[ctrack15.loc[k, 'Latitude']], 
                    #        lon=[ctrack15.loc[k, 'Longitude']],
                    #        marker={ 

                    #                     'size': 8, 
                    #                     'color': '#ff3030',
                                     
                    #        }
                    #        ),



                   ],
               traces=[0,1,2,3,4,5,6,7,8,9]) for k in range(80,120)]

updatemenusz=[dict(type='buttons', showactive=False,
                                y=0,
                                x=1.05,
                                xanchor='right',
                                yanchor='top',
                                pad=dict(t=0, r=10),
                                buttons=[dict(label='Play',
                                              method='animate',
                                              args=[None, 
                                                    dict(frame=dict(duration=1400, 
                                                                    redraw=True),
                                                         transition=dict(duration=0),
                                                         fromcurrent=True,
                                                         mode='immediate'
                                                        )
                                                   ]
                                             ),
                                            {
                                            "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                              "mode": "immediate",
                                              "transition": {"duration": 0}}],
                                                "label": "Pause",
                                                "method": "animate"
                                                }
                                        ]
                               )
                          ]



slidersz = [dict(steps= [dict(method= 'animate',
                           args= [[k],
                                  dict(mode= 'immediate',
                                  frame= dict(duration=1400, redraw= True ),
                                              transition=dict( duration= 0))
                                 ],
                            label=k*0.25
                             ) for k in range(80,120)], 
                transition= dict(duration= 0 ),
                x=0,#slider starting position  
                y=0, 
                currentvalue=dict(font=dict(size=12), 
                                  prefix='Timestep (hours): ', 
                                  visible=True, 
                                  xanchor= 'center'),  
                len=1.0)
           ]





dataz = [

    trace_heli_1z,
    trace_heli_11z,
    trace_destroyer1z,

    trace_p8_carz,

    trace_ctrack0z,
    # trace_ctrack15detectz,
    # trace_ctrack15z,


    waveschlor,
    cloud_ceiling_chlor,
    precipitation_chlor,

    destinationchlor,
    originchlor,
    trace_airbases,

]

figz = dict(
    layout = layoutz,
    data = dataz
    )

figz.update(frames=framesz),
figz['layout'].update(updatemenus=updatemenusz,
          sliders=slidersz)

figzo = go.Figure(figz)


### old fig


layout = dict(
            template= "plotly_dark",
            height=600,
    
            mapbox=dict(accesstoken=mapbox_access_token,
                              bearing=0,
                            #   center=dict(lat=3.5,
                            #                 lon=-95),
                              center=dict(lat=8.21849,
                                            # lon=-71.3459),
                                            lon=-71),
                                            
                              pitch=0,
                              zoom=3.7,
                              style='satellite'),
            legend=dict(
                        title = 'Environment Variables',
                        yanchor="bottom",
                        y=0.05,
                        xanchor="left",
                        x=0.01,
                        groupclick = "toggleitem",
                    ),
            margin= {
                    "b": 5, 
                    "l": 5, 
                    "r": 5, 
                    "t": 5
                }
)


frames = [dict(name=k,
               data=[


                #    dict(
                #            type= "scattermapbox",
                #            lat=rltracks0.loc[:k+1, 'Latitude'].tolist(), 
                #           lon=rltracks0.loc[:k+1, 'Longitude'].tolist()),

                #     dict(
                #            type= "scattermapbox",
                #            lat=rltracks400.loc[:k+1, 'Latitude'].tolist(), 
                #           lon=rltracks400.loc[:k+1, 'Longitude'].tolist()),
                #     dict(
                #            type= "scattermapbox",
                #            lat=rltracks800.loc[:k+1, 'Latitude'].tolist(), 
                #           lon=rltracks800.loc[:k+1, 'Longitude'].tolist()),
                    dict(
                           type= "scattermapbox",
                           lat= [warship.loc[k, 'Latitude']], 
                           lon= [warship.loc[k, 'Longitude']]),
                    dict(
                           type= "scattermapbox",
                           lat= [heli1.loc[k, 'Latitude']], 
                           lon= [heli1.loc[k, 'Longitude']],
                        #    marker=dict( symbol = [heli1.loc[k, 'symbol']])
                           ),
                    # dict(
                    #        type= "scattermapbox",
                    #        lat= [heli_1.loc[k, 'Latitude']], 
                    #        lon= [heli_1.loc[k, 'Longitude']],
                    #         customdata = np.stack((heli_1['altitude'].iloc[k:k+1], heli_1['sensor1'].iloc[k:k+1], heli_1['sensor2'].iloc[k:k+1], heli_1['velocity'].iloc[k:k+1], heli_1['stationtime'].iloc[k:k+1]), axis=-1),
                    #         hovertemplate = "<br>".join([
                    #                                         "Altitude (ft) : %{customdata[0]}",
                    #                                         "APS-147 Radar (km) : %{customdata[1]}",
                    #                                         "AAS-44 MS Targeting System (km) : %{customdata[2]}",
                    #                                         "Cruising Speed (km/hr) : %{customdata[3]}",
                    #                                         "Time Left on Station (hr) : %{customdata[4]}"
                    #                                         ])
                    #     #    marker=dict( symbol = [heli1.loc[k, 'symbol']])
                    #        ),
                    dict(
                           type= "scattermapbox",
                           lat= [heli_1.loc[k, 'Latitude']], 
                           lon= [heli_1.loc[k, 'Longitude']],
                           marker=dict( size = [heli_1.loc[k,'pxsize2']]),
                            customdata = np.stack((heli_1['altitude'].iloc[k:k+1], heli_1['sensor1'].iloc[k:k+1], heli_1['sensor2'].iloc[k:k+1], heli_1['velocity'].iloc[k:k+1], heli_1['stationtime'].iloc[k:k+1]), axis=-1),
                            hovertemplate = "<br>".join([
                                                            "Altitude (ft) : %{customdata[0]}",
                                                            "APS-147 Radar (km) : %{customdata[1]}",
                                                            "AAS-44 MS Targeting System (km) : %{customdata[2]}",
                                                            "Cruising Speed (km/hr) : %{customdata[3]}",
                                                            "Time Left on Station (hr) : %{customdata[4]}"
                                                            ])
                        #    marker=dict( symbol = [heli1.loc[k, 'symbol']])
                           ),
                    dict(
                           type= "scattermapbox",
                           lat= [destroyer1.loc[k, 'Latitude']], 
                           lon= [destroyer1.loc[k, 'Longitude']]),
                    # dict(
                    #        type= "scattermapbox",
                    #        lat= [p8flight.loc[k, 'Latitude']], 
                    #        lon= [p8flight.loc[k, 'Longitude']]),

                    dict(
                           type= "scattermapbox",
                           lat= [p8flight_car.loc[k, 'Latitude']], 
                           lon= [p8flight_car.loc[k, 'Longitude']],
                           marker=dict(
                                        size = [p8flight_car.loc[k, 'rangesize']], 
                                        # 'color': [rltracks3600.loc[0, 'rank']],
                                        # 'colorscale': 'reds',
                                        # 'cmin' : 0,
                                        # 'cmax' : 4200,
                                        # 'opacity' : 0.4
                          )
                           ),

                    dict(
                           type= "scattermapbox",
                           lat= [destroyer2.loc[k, 'Latitude']], 
                           lon= [destroyer2.loc[k, 'Longitude']]),
                    dict(
                           type= "scattermapbox",
                           lat= [heli_2.loc[k, 'Latitude']], 
                           lon= [heli_2.loc[k, 'Longitude']],
                           marker=dict( size = [heli_2.loc[k,'pxsize2']]),
                            customdata = np.stack((heli_2['altitude'].iloc[k:k+1], heli_2['sensor1'].iloc[k:k+1], heli_2['sensor2'].iloc[k:k+1], heli_2['velocity'].iloc[k:k+1], heli_2['stationtime'].iloc[k:k+1]), axis=-1),
                            hovertemplate = "<br>".join([
                                                            "Altitude (ft) : %{customdata[0]}",
                                                            "APS-147 Radar (km) : %{customdata[1]}",
                                                            "AAS-44 MS Targeting System (km) : %{customdata[2]}",
                                                            "Cruising Speed (km/hr) : %{customdata[3]}",
                                                            "Time Left on Station (hr) : %{customdata[4]}"
                                                            ])
                        #    marker=dict( symbol = [heli1.loc[k, 'symbol']])
                           ),

                    dict(
                           type= "scattermapbox",
                           lat= [p8flight_pac.loc[k, 'Latitude']], 
                           lon= [p8flight_pac.loc[k, 'Longitude']],
                           marker=dict(
                                        size = [p8flight_pac.loc[k, 'rangesize']], 
                                        # 'color': [rltracks3600.loc[0, 'rank']],
                                        # 'colorscale': 'reds',
                                        # 'cmin' : 0,
                                        # 'cmax' : 4200,
                                        # 'opacity' : 0.4
                          )
                           ),
                    # dict(
                    #        type= "scattermapbox",
                    #        lat=rltracks1200.loc[:k+1, 'Latitude'].tolist(), 
                    #       lon=rltracks1200.loc[:k+1, 'Longitude'].tolist()),
                    # dict(
                    #        type= "scattermapbox",
                    #        lat=rltracks1600.loc[:k+1, 'Latitude'].tolist(), 
                    #       lon=rltracks1600.loc[:k+1, 'Longitude'].tolist()),
                    # dict(
                    #        type= "scattermapbox",
                    #        lat=rltracks2000.loc[:k+1, 'Latitude'].tolist(), 
                    #       lon=rltracks2000.loc[:k+1, 'Longitude'].tolist()),
                    # dict(
                    #        type= "scattermapbox",
                    #        lat=rltracks2800.loc[:k+1, 'Latitude'].tolist(), 
                    #       lon=rltracks2800.loc[:k+1, 'Longitude'].tolist()),
                    # dict(
                    #        type= "scattermapbox",
                    #        lat=[rltracks3600.loc[k, 'Latitude']],
                    #       lon=[rltracks3600.loc[k, 'Longitude']],
                    #       marker=dict( color = [rltracks3600.loc[k, 'rank']]
                    #                     # size = 50, 
                    #                     # 'color': [rltracks3600.loc[0, 'rank']],
                    #                     # 'colorscale': 'reds',
                    #                     # 'cmin' : 0,
                    #                     # 'cmax' : 4200,
                    #                     # 'opacity' : 0.4
                    #       )
                    #       ),
                    # dict(
                    #        type= "scattermapbox",
                    #        lat=rltracks3999.loc[:k+1, 'Latitude'].tolist(), 
                    #        lon=rltracks3999.loc[:k+1, 'Longitude'].tolist(),
                    #        marker={ 
                    #                     # symbol = rltracks3999.loc[:k+1, 'symbol'].tolist()
                    #                     'size': 8, 
                    #                     'color': rltracks3999.loc[:k+1, 'rank'].tolist(),
                    #                     'colorscale': 'reds',
                    #                     'cmin' : 0,
                    #                     'cmax' : 4200,
                    #                     'opacity' : 0.9,                                        
                    #        }
                    #        ),
                    dict(
                       type= "scattermapbox",
                       
                       lat=df_rosa.loc[k, 'Latitude'].tolist(), 
                        lon=df_rosa.loc[k, 'Longitude'].tolist(),
                        marker={ 
                                        # 'symbol' : [ctrack0.loc[k, 'symbol']],
                                        'size': df_rosa.loc[k, 'size'].tolist(),
                                        'color': df_rosa.loc[k, 'color'].tolist(),
                                     
                           }
                       ),
                    # dict(
                    #    type= "scattermapbox",
                       
                    #    lat=[df_rosa2.loc[k, 'Latitude']], 
                    #     lon=[df_rosa2.loc[k, 'Longitude']],
                        
                    #    ),
                    dict(
                           type= "scattermapbox",
                           lat= ctrack0.loc[k, 'Latitude'].tolist(), 
                           lon= ctrack0.loc[k, 'Longitude'].tolist(),
                           marker={ 
                                        # 'symbol' : [ctrack0.loc[k, 'symbol']],
                                        'size': ctrack0.loc[k, 'size'].tolist(), 
                                        'color': ctrack0.loc[k, 'color'].tolist(),
                                     
                           }
                           ),

                    # dict(
                    #        type= "scattermapbox",
                    #        lat=[ctrack15.loc[k, 'Latitude']], 
                    #        lon=[ctrack15.loc[k, 'Longitude']],
                    #        marker={ 

                    #                     'size': [ctrack15.loc[k, 'detectsize']], 
                    #                     'color': [ctrack15.loc[k, 'color']],
                                     
                    #        }
                    #        ),                           
                    # dict(
                    #        type= "scattermapbox",
                    #        lat=[ctrack15.loc[k, 'Latitude']], 
                    #        lon=[ctrack15.loc[k, 'Longitude']],
                    #        marker={ 

                    #                     'size': 8, 
                    #                     'color': '#ff3030',
                                     
                    #        }
                    #        ),

                    # dict(
                    #    type= "choroplethmapbox",
                       
                    #     z = df_daylight['Daylight2'][df_daylight['time']==(k + 4 // 2) // 4],
                    #     locations = df_daylight['ids'][df_daylight['time']==(k + 4 // 2) // 4],
                    #     geojson = grid24df,
                        
                    #    ),
                    # dict(
                    #    type= "choroplethmapbox",
                       
                    #     z = df_fogarray['Fog'][df_fogarray['time'] == (k + 4 // 2) // 4],
                    #     locations = df_fogarray['ids'][df_fogarray['time'] == (k + 4 // 2) // 4],
                    #     geojson = grid240df,
                        
                    #    ),
                    # dict(
                    #    type= "choroplethmapbox",
                       
                    #     z = df_fogarray['ceiling'][df_fogarray['time'] == (k + 4 // 2) // 4],
                    #     locations = df_fogarray['ids'][df_fogarray['time'] == (k + 4 // 2) // 4],
                    #     geojson = grid240df,
                        
                    #    ),

                    # dict(
                    #    type= "choroplethmapbox",
                       
                    #     z = df_fogarray['Radar Range'][df_fogarray['time'] == (k + 4 // 2) // 4],
                    #     locations = df_fogarray['ids'][df_fogarray['time'] == (k + 4 // 2) // 4],
                    #     geojson = grid240df,
                        
                    #    )

                   ],
               traces=[0,1,2,3,4,5,6,7,8,9,10,11,12,13]) for k in range(N)]

updatemenus=[dict(type='buttons', showactive=False,
                                y=0,
                                x=1.05,
                                xanchor='right',
                                yanchor='top',
                                pad=dict(t=0, r=10),
                                buttons=[dict(label='Play',
                                              method='animate',
                                              args=[None, 
                                                    dict(frame=dict(duration=700, 
                                                                    redraw=True),
                                                         transition=dict(duration=0),
                                                         fromcurrent=True,
                                                         mode='immediate'
                                                        )
                                                   ]
                                             ),
                                            {
                                            "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                              "mode": "immediate",
                                              "transition": {"duration": 0}}],
                                                "label": "Pause",
                                                "method": "animate"
                                                }
                                        ]
                               )
                          ]



sliders = [dict(steps= [dict(method= 'animate',
                           args= [[k],
                                  dict(mode= 'immediate',
                                  frame= dict(duration=700, redraw= True ),
                                              transition=dict( duration= 0))
                                 ],
                            label=k*0.25
                             ) for k in range(N)], 
                transition= dict(duration= 0 ),
                x=0,#slider starting position  
                y=0, 
                currentvalue=dict(font=dict(size=12), 
                                  prefix='Timestep (hours): ', 
                                  visible=True, 
                                  xanchor= 'center'),  
                len=1.0)
           ]




data = [
    # trace_0,
    # trace_400,
    # trace_800,
    trace_warship,
    trace_heli,
    trace_heli_1,
    trace_destroyer1,
    # trace_p8,
    trace_p8_car,
    trace_destroyer2,
    trace_heli_2,
    trace_p8_pac,
    # trace_1200,
    # trace_1600,
    # trace_2000,
    # trace_2800,
    # trace_3600,
    # trace_3999,
    # tracetargetbase,
    tracerosabase,
    # tracerosa2,
    trace_ctrack0,
    # trace_ctrack15detect,
    # trace_ctrack15,

    # traceBlackbase,
    # daylightchlor,
    # fogchlor,
    # ceilingchlor,
    # ceilingrangechlor,
    waveschlor,
    cloud_ceiling_chlor,
    precipitation_chlor,
    # traceneuralmap,
    # trac26nmmap,
    # tracegridbase,
    # trace2path,
    # trace50path,
    # trace300path,
    # trace500path,
    # trace1000path,
    # historicalchlor,
    # aischlor,
    # destinationchlor,
    originchlor,
    trace_airbases,
    # trace_ptds
    # trace2path,
    # trace50path,
    # trace300path,
    # trace500path,
    # trace1000path,
    # trace2000path
]

fig1 = dict(
    layout = layout,
    data = data
    )

fig1.update(frames=frames),
fig1['layout'].update(updatemenus=updatemenus,
          sliders=sliders)

fig3 = go.Figure(fig1)


##sensor change

frames2 = [dict(name=k,
               data=[


                    dict(
                           type= "scattermapbox",
                           lat= [warship.loc[k, 'Latitude']], 
                           lon= [warship.loc[k, 'Longitude']]),
                    dict(
                           type= "scattermapbox",
                           lat= [heli1.loc[k, 'Latitude']], 
                           lon= [heli1.loc[k, 'Longitude']],
                        #    marker=dict( symbol = [heli1.loc[k, 'symbol']])
                           ),

                    dict(
                           type= "scattermapbox",
                           lat= [heli_1.loc[k, 'Latitude']], 
                           lon= [heli_1.loc[k, 'Longitude']],
                           marker=dict( size = [heli_1.loc[k,'pxsize3']]),
                            customdata = np.stack((heli_1['altitude'].iloc[k:k+1], heli_1['sensor1'].iloc[k:k+1], heli_1['sensor2'].iloc[k:k+1], heli_1['velocity'].iloc[k:k+1], heli_1['stationtime'].iloc[k:k+1]), axis=-1),
                            hovertemplate = "<br>".join([
                                                            "Altitude (ft) : %{customdata[0]}",
                                                            "APS-147 Radar (km) : %{customdata[1]}",
                                                            "AAS-44 MS Targeting System (km) : %{customdata[2]}",
                                                            "Cruising Speed (km/hr) : %{customdata[3]}",
                                                            "Time Left on Station (hr) : %{customdata[4]}"
                                                            ])
                        #    marker=dict( symbol = [heli1.loc[k, 'symbol']])
                           ),
                    dict(
                           type= "scattermapbox",
                           lat= [destroyer1.loc[k, 'Latitude']], 
                           lon= [destroyer1.loc[k, 'Longitude']]),


                    dict(
                           type= "scattermapbox",
                           lat= [p8flight_car.loc[k, 'Latitude']], 
                           lon= [p8flight_car.loc[k, 'Longitude']],
                           marker=dict(
                                        size = [p8flight_car.loc[k, 'rangesize2']], 
                                        # 'color': [rltracks3600.loc[0, 'rank']],
                                        # 'colorscale': 'reds',
                                        # 'cmin' : 0,
                                        # 'cmax' : 4200,
                                        # 'opacity' : 0.4
                          )
                           ),

                    dict(
                           type= "scattermapbox",
                           lat= [destroyer2.loc[k, 'Latitude']], 
                           lon= [destroyer2.loc[k, 'Longitude']]),
                    dict(
                           type= "scattermapbox",
                           lat= [heli_2.loc[k, 'Latitude']], 
                           lon= [heli_2.loc[k, 'Longitude']],
                           marker=dict( size = [heli_2.loc[k,'pxsize3']]),
                            customdata = np.stack((heli_2['altitude'].iloc[k:k+1], heli_2['sensor1'].iloc[k:k+1], heli_2['sensor2'].iloc[k:k+1], heli_2['velocity'].iloc[k:k+1], heli_2['stationtime'].iloc[k:k+1]), axis=-1),
                            hovertemplate = "<br>".join([
                                                            "Altitude (ft) : %{customdata[0]}",
                                                            "APS-147 Radar (km) : %{customdata[1]}",
                                                            "AAS-44 MS Targeting System (km) : %{customdata[2]}",
                                                            "Cruising Speed (km/hr) : %{customdata[3]}",
                                                            "Time Left on Station (hr) : %{customdata[4]}"
                                                            ])
                        #    marker=dict( symbol = [heli1.loc[k, 'symbol']])
                           ),

                    dict(
                           type= "scattermapbox",
                           lat= [p8flight_pac.loc[k, 'Latitude']], 
                           lon= [p8flight_pac.loc[k, 'Longitude']],
                           marker=dict(
                                        size = [p8flight_pac.loc[k, 'rangesize2']], 
                                        # 'color': [rltracks3600.loc[0, 'rank']],
                                        # 'colorscale': 'reds',
                                        # 'cmin' : 0,
                                        # 'cmax' : 4200,
                                        # 'opacity' : 0.4
                          )
                           ),

                    dict(
                       type= "scattermapbox",
                       
                       lat=df_rosa.loc[k, 'Latitude'].tolist(), 
                        lon=df_rosa.loc[k, 'Longitude'].tolist(),
                        marker={ 
                                        # 'symbol' : [ctrack0.loc[k, 'symbol']],
                                        'size': df_rosa.loc[k, 'size'].tolist(),
                                        'color': df_rosa.loc[k, 'color'].tolist(),
                                     
                           }
                       ),

                    dict(
                           type= "scattermapbox",
                           lat= ctrack0.loc[k, 'Latitude'].tolist(), 
                           lon= ctrack0.loc[k, 'Longitude'].tolist(),
                           marker={ 
                                        # 'symbol' : [ctrack0.loc[k, 'symbol']],
                                        'size': ctrack0.loc[k, 'size'].tolist(), 
                                        'color': '#ff3030',
                                     
                           }
                           ),



                   ],
               traces=[0,1,2,3,4,5,6,7,8,9,10,11,12,13]) for k in range(N)]

datasensor = [
    # trace_0,
    # trace_400,
    # trace_800,
    trace_warship_5,
    trace_heli_5,
    trace_heli_1_5,
    trace_destroyer1_5,
    # trace_p8,
    trace_p8_car_5,
    trace_destroyer2_5,
    trace_heli_2_5,
    trace_p8_pac_5,

    tracerosabase,

    trace_ctrack0,
 
    waveschlor,
    cloud_ceiling_chlor,
    precipitation_chlor,

    originchlor,
    trace_airbases,
    # trace_ptds
 
]

figsens = dict(
    layout = layout,
    data = datasensor
    )

figsens.update(frames=frames2),
figsens['layout'].update(updatemenus=updatemenus,
          sliders=sliders)

fig5 = go.Figure(figsens)


## Sail Drone Vignette
framesSD = [dict(name=k,
               data=[


                    dict(
                           type= "scattermapbox",
                           lat= [destroyer0.loc[k, 'Latitude']], 
                           lon= [destroyer0.loc[k, 'Longitude']]),
                    dict(
                           type= "scattermapbox",
                           lat= [heli00.loc[k, 'Latitude']], 
                           lon= [heli00.loc[k, 'Longitude']],
                        #    marker=dict( symbol = [heli1.loc[k, 'symbol']])
                           ),

                    dict(
                           type= "scattermapbox",
                           lat= [heli_1.loc[k, 'Latitude']], 
                           lon= [heli_1.loc[k, 'Longitude']],
                           marker=dict( size = [heli_1.loc[k,'pxsize2']]),
                            customdata = np.stack((heli_1['altitude'].iloc[k:k+1], heli_1['sensor1'].iloc[k:k+1], heli_1['sensor2'].iloc[k:k+1], heli_1['velocity'].iloc[k:k+1], heli_1['stationtime'].iloc[k:k+1]), axis=-1),
                            hovertemplate = "<br>".join([
                                                            "Altitude (ft) : %{customdata[0]}",
                                                            "APS-147 Radar (km) : %{customdata[1]}",
                                                            "AAS-44 MS Targeting System (km) : %{customdata[2]}",
                                                            "Cruising Speed (km/hr) : %{customdata[3]}",
                                                            "Time Left on Station (hr) : %{customdata[4]}"
                                                            ])
                        #    marker=dict( symbol = [heli1.loc[k, 'symbol']])
                           ),
                    dict(
                           type= "scattermapbox",
                           lat= [destroyer1.loc[k, 'Latitude']], 
                           lon= [destroyer1.loc[k, 'Longitude']]),
                    


                    # dict(
                    #        type= "scattermapbox",
                    #        lat= [p8flight_car.loc[k, 'Latitude']], 
                    #        lon= [p8flight_car.loc[k, 'Longitude']],
                    #        marker=dict(
                    #                     size = [p8flight_car.loc[k, 'rangesize']], 
                    #                     # 'color': [rltracks3600.loc[0, 'rank']],
                    #                     # 'colorscale': 'reds',
                    #                     # 'cmin' : 0,
                    #                     # 'cmax' : 4200,
                    #                     # 'opacity' : 0.4
                    #       )
                    #        ),

                    # dict(
                    #        type= "scattermapbox",
                    #        lat= [destroyer2.loc[k, 'Latitude']], 
                    #        lon= [destroyer2.loc[k, 'Longitude']]),
                    # dict(
                    #        type= "scattermapbox",
                    #        lat= [heli_2.loc[k, 'Latitude']], 
                    #        lon= [heli_2.loc[k, 'Longitude']],
                    #        marker=dict( size = [heli_2.loc[k,'pxsize2']]),
                    #         customdata = np.stack((heli_2['altitude'].iloc[k:k+1], heli_2['sensor1'].iloc[k:k+1], heli_2['sensor2'].iloc[k:k+1], heli_2['velocity'].iloc[k:k+1], heli_2['stationtime'].iloc[k:k+1]), axis=-1),
                    #         hovertemplate = "<br>".join([
                    #                                         "Altitude (ft) : %{customdata[0]}",
                    #                                         "APS-147 Radar (km) : %{customdata[1]}",
                    #                                         "AAS-44 MS Targeting System (km) : %{customdata[2]}",
                    #                                         "Cruising Speed (km/hr) : %{customdata[3]}",
                    #                                         "Time Left on Station (hr) : %{customdata[4]}"
                    #                                         ])
                    #     #    marker=dict( symbol = [heli1.loc[k, 'symbol']])
                    #        ),

                    dict(
                           type= "scattermapbox",
                           lat= [p8flight_pac.loc[k, 'Latitude']], 
                           lon= [p8flight_pac.loc[k, 'Longitude']],
                           marker=dict(
                                        size = [p8flight_pac.loc[k, 'rangesize']], 
                                        # 'color': [rltracks3600.loc[0, 'rank']],
                                        # 'colorscale': 'reds',
                                        # 'cmin' : 0,
                                        # 'cmax' : 4200,
                                        # 'opacity' : 0.4
                          )
                           ),
                    dict(
                       type= "scattermapbox",
                       
                       lat=sd.loc[k, 'Latitude'].tolist(), 
                        lon=sd.loc[k, 'Longitude'].tolist(),
                        
                       ),
                    dict(
                       type= "scattermapbox",
                       
                       lat=sd_1.loc[k, 'Latitude'].tolist(), 
                        lon=sd_1.loc[k, 'Longitude'].tolist(),
                        
                       ),
                    dict(
                       type= "scattermapbox",
                       
                       lat=sd_2.loc[k, 'Latitude'].tolist(), 
                        lon=sd_2.loc[k, 'Longitude'].tolist(),
                        
                       ),

                    dict(
                       type= "scattermapbox",
                       
                       lat=df_rosa3.loc[k, 'Latitude'].tolist(), 
                        lon=df_rosa3.loc[k, 'Longitude'].tolist(),
                        marker={ 
                                        # 'symbol' : [ctrack0.loc[k, 'symbol']],
                                        'size': df_rosa3.loc[k, 'size'].tolist(),
                                        'color': df_rosa3.loc[k, 'color'].tolist(),
                                     
                           }
                        
                       ),

                    dict(
                           type= "scattermapbox",
                           lat= ctrack0.loc[k, 'Latitude'].tolist(), 
                           lon= ctrack0.loc[k, 'Longitude'].tolist(),
                           marker={ 
                                        # 'symbol' : [ctrack0.loc[k, 'symbol']],
                                        'size': ctrack0.loc[k, 'size'].tolist(), 
                                        'color': '#ff3030',
                                     
                           }
                           ),



                   ],
               traces=[0,1,2,3,4,5,6,7,8,9,10,11,12,13]) for k in range(N)]

dataSD = [

    trace_destroyer0,
    trace_heli00,
    trace_heli_1,
    trace_destroyer1,
    # trace_p8,
    # trace_p8_car,
    # trace_destroyer2,
    # trace_heli_2,
    trace_p8_pac,
    trace_sdcar,
    trace_sdpac1,
    trace_sdpac2,

    tracerosabase3,
    # tracerosa2,
    trace_ctrack0,

    waveschlor,
    cloud_ceiling_chlor,
    precipitation_chlor,

    originchlor,
    trace_airbases,
    trace_ptds

]

figSD = dict(
    layout = layout,
    data = dataSD
    )

figSD.update(frames=framesSD),
figSD['layout'].update(updatemenus=updatemenus,
          sliders=sliders)

fig6 = go.Figure(figSD)


## AIS Bounty
## Sail Drone Vignette
framesais = [dict(name=k,
               data=[


                    dict(
                           type= "scattermapbox",
                           lat= [destroyer0.loc[k, 'Latitude']], 
                           lon= [destroyer0.loc[k, 'Longitude']]),
                    dict(
                           type= "scattermapbox",
                           lat= [heli00.loc[k, 'Latitude']], 
                           lon= [heli00.loc[k, 'Longitude']],
                        #    marker=dict( symbol = [heli1.loc[k, 'symbol']])
                           ),

                    dict(
                           type= "scattermapbox",
                           lat= [heli_1.loc[k, 'Latitude']], 
                           lon= [heli_1.loc[k, 'Longitude']],
                           marker=dict( size = [heli_1.loc[k,'pxsize2']]),
                            customdata = np.stack((heli_1['altitude'].iloc[k:k+1], heli_1['sensor1'].iloc[k:k+1], heli_1['sensor2'].iloc[k:k+1], heli_1['velocity'].iloc[k:k+1], heli_1['stationtime'].iloc[k:k+1]), axis=-1),
                            hovertemplate = "<br>".join([
                                                            "Altitude (ft) : %{customdata[0]}",
                                                            "APS-147 Radar (km) : %{customdata[1]}",
                                                            "AAS-44 MS Targeting System (km) : %{customdata[2]}",
                                                            "Cruising Speed (km/hr) : %{customdata[3]}",
                                                            "Time Left on Station (hr) : %{customdata[4]}"
                                                            ])
                        #    marker=dict( symbol = [heli1.loc[k, 'symbol']])
                           ),
                    dict(
                           type= "scattermapbox",
                           lat= [destroyer1.loc[k, 'Latitude']], 
                           lon= [destroyer1.loc[k, 'Longitude']]),
                    


                    dict(
                           type= "scattermapbox",
                           lat= [p8flight_car.loc[k, 'Latitude']], 
                           lon= [p8flight_car.loc[k, 'Longitude']],
                           marker=dict(
                                        size = [p8flight_car.loc[k, 'rangesize']], 
                                        # 'color': [rltracks3600.loc[0, 'rank']],
                                        # 'colorscale': 'reds',
                                        # 'cmin' : 0,
                                        # 'cmax' : 4200,
                                        # 'opacity' : 0.4
                          )
                           ),

                    # dict(
                    #        type= "scattermapbox",
                    #        lat= [destroyer2.loc[k, 'Latitude']], 
                    #        lon= [destroyer2.loc[k, 'Longitude']]),
                    # dict(
                    #        type= "scattermapbox",
                    #        lat= [heli_2.loc[k, 'Latitude']], 
                    #        lon= [heli_2.loc[k, 'Longitude']],
                    #        marker=dict( size = [heli_2.loc[k,'pxsize2']]),
                    #         customdata = np.stack((heli_2['altitude'].iloc[k:k+1], heli_2['sensor1'].iloc[k:k+1], heli_2['sensor2'].iloc[k:k+1], heli_2['velocity'].iloc[k:k+1], heli_2['stationtime'].iloc[k:k+1]), axis=-1),
                    #         hovertemplate = "<br>".join([
                    #                                         "Altitude (ft) : %{customdata[0]}",
                    #                                         "APS-147 Radar (km) : %{customdata[1]}",
                    #                                         "AAS-44 MS Targeting System (km) : %{customdata[2]}",
                    #                                         "Cruising Speed (km/hr) : %{customdata[3]}",
                    #                                         "Time Left on Station (hr) : %{customdata[4]}"
                    #                                         ])
                    #     #    marker=dict( symbol = [heli1.loc[k, 'symbol']])
                    #        ),

                    dict(
                           type= "scattermapbox",
                           lat= [p8flight_pac.loc[k, 'Latitude']], 
                           lon= [p8flight_pac.loc[k, 'Longitude']],
                           marker=dict(
                                        size = [p8flight_pac.loc[k, 'rangesize']], 
                                        # 'color': [rltracks3600.loc[0, 'rank']],
                                        # 'colorscale': 'reds',
                                        # 'cmin' : 0,
                                        # 'cmax' : 4200,
                                        # 'opacity' : 0.4
                          )
                           ),
                    # dict(
                    #    type= "scattermapbox",
                       
                    #    lat=sd.loc[k, 'Latitude'].tolist(), 
                    #     lon=sd.loc[k, 'Longitude'].tolist(),
                        
                    #    ),
                    # dict(
                    #    type= "scattermapbox",
                       
                    #    lat=sd_1.loc[k, 'Latitude'].tolist(), 
                    #     lon=sd_1.loc[k, 'Longitude'].tolist(),
                        
                    #    ),
                    # dict(
                    #    type= "scattermapbox",
                       
                    #    lat=sd_2.loc[k, 'Latitude'].tolist(), 
                    #     lon=sd_2.loc[k, 'Longitude'].tolist(),
                        
                    #    ),
                    dict(
                       type= "scattermapbox",
                       
                       lat=ais_all.loc[k, 'Latitude'].tolist(), 
                        lon=ais_all.loc[k, 'Longitude'].tolist(),
                        
                       ),
                    dict(
                       type= "scattermapbox",
                       
                       lat=df_rosa3.loc[k, 'Latitude'].tolist(), 
                        lon=df_rosa3.loc[k, 'Longitude'].tolist(),
                        marker={ 
                                        # 'symbol' : [ctrack0.loc[k, 'symbol']],
                                        'size': df_rosa3.loc[k, 'size'].tolist(),
                                        'color': df_rosa3.loc[k, 'color'].tolist(),
                                     
                           }
                       ),

                    dict(
                           type= "scattermapbox",
                           lat= ctrack0.loc[k, 'Latitude'].tolist(), 
                           lon= ctrack0.loc[k, 'Longitude'].tolist(),
                           marker={ 
                                        # 'symbol' : [ctrack0.loc[k, 'symbol']],
                                        'size': ctrack0.loc[k, 'size'].tolist(), 
                                        'color': '#ff3030',
                                     
                           }
                           ),



                   ],
               traces=[0,1,2,3,4,5,6,7,8,9,10,11,12,13]) for k in range(220)]

dataais = [

    trace_destroyer0,
    trace_heli00,
    trace_heli_1,
    trace_destroyer1,
    # trace_p8,
    trace_p8_car,
    # trace_destroyer2,
    # trace_heli_2,
    trace_p8_pac,
    # trace_sdcar,
    # trace_sdpac1,
    # trace_sdpac2,
    trace_aism,

    tracerosabase3,
    # tracerosa2,
    trace_ctrack0,

    waveschlor,
    cloud_ceiling_chlor,
    precipitation_chlor,

    originchlor,
    trace_airbases,
    # trace_ptds

]

figAIS = dict(
    layout = layout,
    data = dataais
    )

figAIS.update(frames=framesais),
figAIS['layout'].update(updatemenus=updatemenus,
          sliders=sliders)

fig7 = go.Figure(figAIS)


###
number_input_dest = html.Div(
    [
        html.H4('Destroyer Radar Range'),
        html.P("Enter Radar Range in km"),
        dbc.Input(type="number", min=0, max=500, step=0.05),
    ],
    id="styled-numeric-input1",
)

number_input_p8 = html.Div(
    [
        html.H4('P8 Radar Range'),
        html.P("Enter Radar Range in km"),
        dbc.Input(type="number", min=0, max=600, step=0.05, value = 300.5),
    ],
    id="styled-numeric-input2",
)

number_input_heli = html.Div(
    [
        html.H4('SH-60 Radar Range'),
        html.P("Enter Radar Range in km"),
        dbc.Input(type="number", min = 0, max = 300, step=0.05),
    ],
    id="styled-numeric-input3",
)


## Build Layout

row = html.Div(
    [
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.Div( html.H5("Reinforcement Learning Environment"
                    , 
                    style={'color': '#d40000', 'fontSize': 18}
                    )
                    ),
                    
                    width={"size": 6
                    , 
                    "offset": 3
                    },
            
                ),

            ],

            ),

        dbc.Row(
            [

                dbc.Col(
                    [


                        dcc.Graph( 
                                    # id = 'graph-moving'

                                    figure = fig3
                                    ),


                    ],
                    width = 12
                ),
                # dbc.Col(
                #     number_input_p8,
                #     width = 4

                # ),
                # dbc.Col(
                #     number_input_dest,
                #     width = 4

                # ),
                # dbc.Col(
                #     number_input_heli,
                #     width = 4

                # ),
                dbc.Col(
                    [
                        

                        dcc.Graph( 

                                    figure = figzo),


                    ],
                    width = 12
                ),


            ]
            
        ),
        
        dbc.Row(
            [
                # dbc.Col(
                #     number_input,

                # ),

                dbc.Col(
                    html.Div( html.H5('Load'),
                     
                    style={'color': '#d40000', 'fontSize': 18}
                    )
                    ,
                    
                    width={"size": 6
                    , 
                    "offset": 3
                    },
            
                ),
                # dbc.Col(
                #     html.Div( html.H5("Raw Data"
                #     , 
                #     style={'color': '#339933', 'fontSize': 18}
                #     )
                #     ),
                    
                #     width={"size": 3, 
                #     "offset": 2},
                
                # )
            ],

            ),
        # dbc.Row([
            
        #     sliderin,
        #     html.Div( html.H6(id ='slider-output-container' ))
        # ]),


        # dbc.Row(
        #     html.Div([
        #         dcc.Markdown("""
        #             **Selection Data**

        #             Choose the lasso or rectangle tool in the graph's menu
        #             bar and then select points in the graph.

        #             Note that if `layout.clickmode = 'event+select'`, selection data also
        #             accumulates (or un-accumulates) selected data if you hold down the shift
        #             button while clicking.
        #         """),
        #         html.Pre(id='selected-data', style=styles['pre']),
        #         ])
            
        # )
       
    ],
    style={'backgroundColor': 'black'}
)

# controls
controls = dbc.Card(
      [dbc.FormGroup(
            [
                dbc.Label("Options"),
                                dcc.RadioItems(id="display_figure", 
                                options=[   {'label': 'Original', 'value': 'Nope'},
                                            {'label': 'Sensor Change', 'value': 'Figure1'},
                                            {'label': 'Crowdsource', 'value': 'Figure2'},
                                            {'label': 'Unmanned Surge', 'value': 'Figure3'}
                                ],
                                value='Nope',
                                labelStyle={'display': 'inline-block', 'width': '10em', 'line-height':'0.5em'}
                                ) 
            ], 
        ),
        dbc.FormGroup(
            [dbc.Label(""),]
        ),
    ],
    color="dark", inverse=True,
    body=True,
    style = {'font-size': 'large'})

# controls
slider_c = dbc.Card(
      [html.Div(
            [
                dbc.Label("Sensor Range Percentage Change", html_for="slider"),
                dcc.Slider(id="my-slider", min=0, max=200, step=1, value=100),
                html.Div(id='slider-output-container')
            ],
            className="mb-3",
                )
      ],
    color="dark", inverse=True,
    body=True,
    style = {'font-size': 'large'})

# controls
slider_end = dbc.Card(
      [html.Div(
            [
                dbc.Label("First Look Detections:", html_for="slider"),
                # dcc.Slider(id="my-slider-end", min=0, max=200, step=1, value=100),
                html.Div(id='slider-output-container-2'),

                dbc.Label("Number PID:", html_for="slider"),

                html.Div(id='slider-output-container-3')
            ],
            className="mb-3",
                )
      ],
    color="dark", inverse=True,
    body=True,
    style = {'font-size': 'large'})

# controls
opt_read = dbc.Card(
      [html.Div(
            [
                dbc.Button(
                        "Click me", id="example-button", className="me-2", n_clicks=0
                    ),

                html.Div(id='result'),


            ],
            className="mb-3",
                )
      ],
    color="dark", inverse=True,
    body=True,
    style = {'font-size': 'large'})





external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootswatch@5.1.0/dist/cerulean/bootstrap.min.css']
# https://cdn.jsdelivr.net/npm/bootswatch@5.1.0/dist/cerulean/bootstrap.min.css
##
app = dash.Dash(__name__,                  
                 title="Salacious Crumb RL Model!",
                 assets_folder ="static",
                 assets_url_path="static",
                 external_stylesheets=external_stylesheets)

application = app.server
# app.title='Hack the Machine Environment!'

app.layout =  html.Div([

    dbc.Container(
                [
        html.Div([

            dbc.Container(
                [
                    # html.A(
                        html.Br(),
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                # html.Br(),
                                # dbc.Col(html.Img(src= app.get_asset_url('CET-23.png'), height="40px")),
                                dbc.Col([html.Img(src= app.get_asset_url('spear3.png'), height="30px")], width = 1),
                                dbc.Col([html.Img(src= app.get_asset_url('CET-23.png'), height="30px")], width = 1),
                                dbc.Col([html.Img(src= app.get_asset_url('CurrentLab2.png'), height="30px")], width = 2),
                                dbc.Col([html.Img(src= app.get_asset_url('aws1.png'), height="30px")], width = 1),

                                # dbc.Col([dbc.NavbarBrand("Team Salacious Crumb"
                                # # , 
                                # # className="ms-2"
                                # )], width = 4),
                                
                                dbc.Col(
                                            html.Div("Team Salacious Crumb", style={'color': 'Black', 'fontSize': 26}),
                                            width={"size": 4, "offset": 0},
                                                ),
                                #     html.Div( html.H4("Team Salacious Crumb", style={'color': 'Black', 'fontSize': 26}))
                                #             width={"size": 6, "offset": 2}, 
                                # ),

                                dbc.Col([html.Img(src= app.get_asset_url('aws1.png'), height="30px")], width = 1),
                                dbc.Col([html.Img(src= app.get_asset_url('hack_the_machine.png'), height="30px")], width = 1),
                                dbc.Col([html.Img(src= app.get_asset_url('top_model.png'), height="30px")], width = 1),
                                # dbc.Col([html.Div( html.H4("Team Salacious Crumb", style={'color': 'Black', 'fontSize': 18}))], 
                                #             width=4),
                            ],
                            # color = '#f6f5f2'
                            # align="center",
                            # className="g-0",
                            # no_gutters=True,
                        ),
                        
                    # ),

                ],
                # color="#2b2b2b",
                fluid=True
                # dark=False,
            )
            # html.Img(src=app.get_asset_url('goetz2.png'))
        ],
        style={'backgroundColor': '#f6f5f2', 'height': 60}
        ),
        dbc.Row([
            dbc.Col([controls],xs = 4),
            dbc.Col([slider_c],xs = 4),
            dbc.Col([slider_end],xs = 4),

            dbc.Col([
                dbc.Row([
                    dbc.Col(dcc.Graph(id="predictions")),
                ])
            ]),
        ]),
        dbc.Row([
            html.Div(
                html.P('Hello heres the output')
            ),
            opt_read

        ]),
        # row,
        html.Div(html.Br(), style={'backgroundColor': '#f6f5f2', 'height': 60})
        ],
    fluid=True

    )
    ],
    style={'backgroundColor': '#2b2b2b'})



@app.callback(
    Output("predictions", "figure"),
    [Input("display_figure", "value"),

    ],
)
def make_graph(display_figure):

    # main trace

#     print(display_figure)
    if 'Nope' in display_figure:
        fig = go.Figure(fig1)

        return fig

    if 'Figure1' in display_figure:
        fig = go.Figure(figsens)
        

    # prediction trace
    if 'Figure2' in display_figure:
        fig = go.Figure(figAIS)


    if 'Figure3' in display_figure:
        fig = go.Figure(figSD)

    return(fig)


@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('my-slider', 'value')])
def update_output(value):
    return 'Sensor Range is at "{}" Percent'.format(value)

@app.callback(
    dash.dependencies.Output('slider-output-container-2', 'children'),
    [dash.dependencies.Input("display_figure", "value")])
def update_output(display_figure):

    if 'Nope' in display_figure:
        ## 52 p8 pac
        ## 35 car
        value = 87

    if 'Figure1' in display_figure:
        value = 89

        ## 36 car

    # prediction trace
    if 'Figure2' in display_figure:
        value = 82


    if 'Figure3' in display_figure:
        value = 89

    return ' {} Detections'.format(value)

@app.callback(
    dash.dependencies.Output('slider-output-container-3', 'children'),
    [dash.dependencies.Input("display_figure", "value")])
def update_output(display_figure):

    if 'Nope' in display_figure:
        
        value = 34

    if 'Figure1' in display_figure:
        value = 42

    # prediction trace
    if 'Figure2' in display_figure:
        #21 dest 0
        value = 27

    if 'Figure3' in display_figure:
        #21 dest 0
        value = 39

    return '{} Detections'.format(value)

# @app.callback(
#     Output('result', 'children'),
#     [Input("example-button", "n_clicks"),
#      ]
# )
# def on_button_click(n):
#     if n is None:
#         return "Not clicked."
#     else:
#         r = SearchForAllSolutionsSampleSat()
#         return '{}'.format(r)

########### Run the app
if __name__ == '__main__':
    application.run(debug=True, port=8080)

