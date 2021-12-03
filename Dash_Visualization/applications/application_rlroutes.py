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




mapbox_access_token = "pk.eyJ1IjoiamtvZWhsZXIxMSIsImEiOiJja2d2MmMyYWswNDlzMnNtdW9jbDU0NXhmIn0.5Ynkm6tAvtl18Q5QBQT_7g"

#AIS DAta
url = 'https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/AIS/PassengerVessel.csv'
df_ais_blue = pd.read_csv(url)
df_ais_red = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/AIS/Tanker.csv')
df_ais_green = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/AIS/Cargo.csv')

df_histroutes = pd.read_csv ('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Routes/HistoricalTraffickingRoutePoints.csv')

##Weather Data
df_fog = pd.read_csv('https://github.com/spear-ai/hackthemachine-unmanned-track-3/blob/dash_visual/Dash_Visualization/synthetic_data/Weather/Visibility/fog3.csv?raw=true')
df_mediumclouds = pd.read_csv ('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Weather/Visibility/medium_clouds.csv')
df_highclouds = pd.read_csv ('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Weather/Visibility/higher.csv')
df_highestclouds = pd.read_csv ('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Weather/Visibility/highest.csv')

## Read in trafficking data
df_Blackroute = pd.read_csv ('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Targets/Blackroute.csv')

##Navigation
navigation = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Navigability/NoNavigationPoints2.csv')



#Load 12 mile territorial line

f = open(r'C:\Users\tjack\Documents\HackTheMachine\12milefileid.json',)
 
# returns JSON object as
# a dictionary
jdata = json.load(f)

urljson1 = "https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Grids/12milefile.json"
  
# store the response of URL
# response1 = urlopen(urljson1)
  
# storing the JSON response 
# from url in data
# jdata = json.loads(response1.read())

# values
jdatadf = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Grids/12milefileid.csv')



## Read in 20 x 20 grid and Data
# Opening JSON file
# parameter for urlopen
urljson = "https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Grids/20by20.json"
  
# store the response of URL
response = urlopen(urljson)
  
# storing the JSON response 
# from url in data
data_json = json.loads(response.read())
# f20 = open('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Grids/20by20.json',)
 
# returns JSON object as
# a dictionary
grid20df = data_json

#Load 24 x 24 data

f24 = open(r'C:\Users\tjack\Documents\HackTheMachine\24by24.json',)
 
# returns JSON object as
# a dictionary
data1 = json.load(f24)

grid24df = data1




#For new json

for k in range(len(grid24df['features'])):
    grid24df['features'][k]['id'] = k

ids24 = [features['id'] for features in grid24df["features"]]

df_griddata = pd.DataFrame()
df_griddata['ids'] = (ids24)
df_griddata['value'] = 3
df_griddata['text'] =  df_griddata.apply(lambda x: "Gameboard Index:" + str(x.ids), axis=1)

# df_griddatain = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\grid_data_20x20.csv')
# df_griddatain = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/grid_data_20x20.csv')
df_griddatain = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\grid_data_24x24.csv')

## Edit navigation
tozero = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Grids\24tozero.csv')
toone = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Grids\24toone.csv')

df_griddatain.loc[df_griddatain['ids'].isin(tozero['tozero']), 'Navigation'] = 0
df_griddatain.loc[df_griddatain['ids'].isin(toone['toone']), 'Navigation'] = 1


df_griddata['AIS'] = df_griddatain['AIS']
df_griddata['Navigation'] = df_griddatain['Navigation']
# Navigation Binary
df_griddata['Navigation'].values[df_griddata['Navigation'].values > 1] = 1
## Initiate Plot with Target Data
df_griddata['Fog'] = df_griddatain['Fog']
df_griddata['Origin'] = df_griddatain['origins']
df_griddata['Destination'] = df_griddatain['destinations']
df_griddata['Historical Trafficking Routes'] = df_griddatain['Historical Trafficking Routes']
df_griddata['High Elevation Clouds'] = df_griddatain['High Elevation Clouds']

df_griddata.loc[(df_griddata['ids']==189), 'Destination'] = 0
df_griddata.loc[(df_griddata['ids']==236), 'Destination'] = 1
df_griddata.loc[(df_griddata['ids']==165), 'Destination'] = 1

## New fog
df_fogarray = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Weather\Visibility\fogtime.csv')

## New Ceiling
df_ceilingarray = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Weather\Visibility\ceilingtime.csv')

# df_fogarray = df_fogarray[df_fogarray['time']==11]

## Track from Amy
patha = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\amypath.csv')

# pathb = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\t8000.csv')
pathb = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\t0.csv')
path50 = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\track_50.csv')
path100 = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\track_100.csv')
path300 = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\track_300.csv')
path500 = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\track_500.csv')
path1000 = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\track_1000.csv')
path2000 = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\track_2000.csv')

## From Amy RL Tracks
rltracks = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\rltracks1.csv')
rltracks0 = rltracks[rltracks['Iteration']== 'track_0']

rltracks400 = rltracks[rltracks['Iteration']== 'track_400']
rltracks400 = rltracks400.reset_index()
rltracks400['Latitude'] = rltracks400['Latitude'] - 0.05
rltracks400['Longitude'] = rltracks400['Longitude'] + -0.05

rltracks800 = rltracks[rltracks['Iteration']== 'track_800']
rltracks800 = rltracks800.reset_index()
rltracks800['Latitude'] = rltracks800['Latitude'] - 0.1
rltracks800['Longitude'] = rltracks800['Longitude'] - 0.1

rltracks1200 = rltracks[rltracks['Iteration']== 'track_1200']
rltracks1200 = rltracks1200.reset_index()

rltracks1600 = rltracks[rltracks['Iteration']== 'track_1600']
rltracks1600 = rltracks1600.reset_index()
rltracks1600['Latitude'] = rltracks1600['Latitude'] + 0.05
rltracks1600['Longitude'] = rltracks1600['Longitude'] + 0.05

rltracks2000 = rltracks[rltracks['Iteration']== 'track_2000']
rltracks2000 = rltracks2000.reset_index()
rltracks2000['Latitude'] = rltracks2000['Latitude'] + 0.1
rltracks2000['Longitude'] = rltracks2000['Longitude'] + 0.1

rltracks2800 = rltracks[rltracks['Iteration']== 'track_2800']
rltracks2800 = rltracks2800.reset_index()
rltracks2800['Latitude'] = rltracks2800['Latitude'] + 0.15
rltracks2800['Longitude'] = rltracks2800['Longitude'] + 0.15

rltracks3600 = rltracks[rltracks['Iteration']== 'track_3600']
rltracks3600 = rltracks3600.reset_index()
rltracks3600['Latitude'] = rltracks3600['Latitude'] + 0.2
rltracks3600['Longitude'] = rltracks3600['Longitude'] + 0.2

rltracks3999 = rltracks[rltracks['Iteration']== 'track_3999']
rltracks3999 = rltracks3999.reset_index()
rltracks3999['Latitude'] = rltracks3999['Latitude'] + 0.25
rltracks3999['Longitude'] = rltracks3999['Longitude'] + 0.25
rltracks3999['symbol'] = 'heliport'

## My Fake
pathfake = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\Route_test.csv')

## Nueral MMO
nmmo1 = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Grids\nmmo1.csv')

## Nueral MMO 26
nmmo26 = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Grids\26nmo.csv')


## Waves
waves = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Grids\waves.csv')



df = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\route_full.csv')

df = pathfake
N = 43

## Add velocity and weight
df['velocity'] = 49
df['heading'] = 270
df['freeboard'] = '3200 kg'

#Kevins Path
df_rosa = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Routes\rosa3.csv')


## Daylight Data

df_daylight = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\Navigability\twilights.csv')

#Load 26 x 26 data

f26 = open(r'C:\Users\tjack\Documents\HackTheMachine\26by26.json',)
 
# returns JSON object as
# a dictionary
grid26 = json.load(f26)

#For new json

for k in range(len(grid26['features'])):
    grid26['features'][k]['id'] = k

ids26 = [features['id'] for features in grid26["features"]]

df_griddata26 = pd.DataFrame()
df_griddata26['ids'] = (ids26)



# df_daylight = df_daylight[df_daylight['time']==11]

trace1path = {

                "name": "Track", 
                "mode": "markers",
                "type": "scattermapbox",
                # "xsrc": "jacksonk:59:eefdd4", 
                "lat": [df_Blackroute['Latitude']], 
                # "ysrc": "jacksonk:59:de0e34", 
                "lon": [df_Blackroute['Longitude']], 
                "marker": {
                    "size": 12, 
                    "color": "rgb(255, 215, 0)" 
                    # "symbol": "asterisk-open"
                }, 
                "showlegend": True, 
                # "stackgroup": None
                }

trace2path = {

                "name": "Track_0", 
                "mode": "markers",
                "type": "scattermapbox",
                # "xsrc": "jacksonk:59:eefdd4", 
                "lat": pathb['Latitude'], 
                # "ysrc": "jacksonk:59:de0e34", 
                "lon": pathb['Longitude'], 
                "marker": {
                    "size": 5, 
                    "color": pathb['time'],
                    'showscale':True,
                    # "rgb(255, 215, 0)" 
                    # "symbol": "asterisk-open"
                }, 
                'text' : pathb['time'],
                "showlegend": True,
                'legendgroup':"rltracks",
                'legendgrouptitle' : dict( text = "RL Iterations"), 
                # "stackgroup": None
                }

trace50path = {

                "name": "Track_50", 
                "mode": "markers",
                "type": "scattermapbox",
                # "xsrc": "jacksonk:59:eefdd4", 
                "lat": path50['Latitude'], 
                # "ysrc": "jacksonk:59:de0e34", 
                "lon": path50['Longitude'], 
                "marker": {
                    "size": 5, 
                    "color": path50['time'],
                    'showscale':True,
                    # "rgb(255, 215, 0)" 
                    # "symbol": "asterisk-open"
                }, 
                'text' : path50['time'],
                "showlegend": True,
                'legendgroup':"rltracks",
                'legendgrouptitle' : dict( text = "RL Iterations"), 
                # "stackgroup": None
                }

trace300path = {

                "name": "Track_300", 
                "mode": "markers",
                "type": "scattermapbox",
                # "xsrc": "jacksonk:59:eefdd4", 
                "lat": path300['Latitude'], 
                # "ysrc": "jacksonk:59:de0e34", 
                "lon": path300['Longitude'], 
                "marker": {
                    "size": 5, 
                    "color": path300['time'],
                    'showscale':True,
                    # "rgb(255, 215, 0)" 
                    # "symbol": "asterisk-open"
                }, 
                'text' : path300['time'],
                "showlegend": True,
                'legendgroup':"rltracks",
                'legendgrouptitle' : dict( text = "RL Iterations"), 
                # "stackgroup": None
                }

trace500path = {

                "name": "Track_500", 
                "mode": "markers",
                "type": "scattermapbox",
                # "xsrc": "jacksonk:59:eefdd4", 
                "lat": path500['Latitude'], 
                # "ysrc": "jacksonk:59:de0e34", 
                "lon": path500['Longitude'], 
                "marker": {
                    "size": 5, 
                    "color": path500['time'],
                    'showscale':True,
                    # "rgb(255, 215, 0)" 
                    # "symbol": "asterisk-open"
                }, 
                'text' : path500['time'],
                "showlegend": True,
                'legendgroup':"rltracks",
                'legendgrouptitle' : dict( text = "RL Iterations"), 
                # "stackgroup": None
                }

trace1000path = {

                "name": "Track_1000", 
                "mode": "markers",
                "type": "scattermapbox",
                # "xsrc": "jacksonk:59:eefdd4", 
                "lat": path1000['Latitude'], 
                # "ysrc": "jacksonk:59:de0e34", 
                "lon": path1000['Longitude'], 
                "marker": {
                    "size": 5, 
                    "color": path1000['time'],
                    'showscale':True,
                    # "rgb(255, 215, 0)" 
                    # "symbol": "asterisk-open"
                }, 
                'text' : path1000['time'],
                "showlegend": True,
                'legendgroup':"rltracks",
                'legendgrouptitle' : dict( text = "RL Iterations"), 
                # "stackgroup": None
                }


trace2000path = {

                "name": "Track_2000", 
                "mode": "markers",
                "type": "scattermapbox",
                # "xsrc": "jacksonk:59:eefdd4", 
                "lat": path2000['Latitude'], 
                # "ysrc": "jacksonk:59:de0e34", 
                "lon": path2000['Longitude'], 
                "marker": {
                    "size": 5, 
                    "color": path2000['time'],
                    'showscale':True,
                    # "rgb(255, 215, 0)" 
                    # "symbol": "asterisk-open"
                }, 
                'text' : path2000['time'],
                "showlegend": True,
                'legendgroup':"rltracks",
                'legendgrouptitle' : dict( text = "RL Iterations"), 
                # "stackgroup": None
                }

trace3chlor = {
                'type': 'choroplethmapbox',
                'name' : 'Gameboard 24 by 24',
                'z': df_griddata['value'],
                'locations':df_griddata['ids'],
                'colorscale':'tealgrn',
                'colorbar':dict(thickness=20, ticklen=3),
                'geojson': grid24df,
                'showlegend':True,
                'showscale':False,
                'text' : df_griddata['text'],
#                           visible :  "legendonly",
                'hoverinfo':'all',
                'marker_line_width':1, 
                'marker_opacity':0.3 
}



trace4scatt = {
        "type": "scattermapbox",
        'name': 'Target Path', 
        'lat': df_Blackroute['Latitude'],
        'lon': df_Blackroute['Longitude'],
        'mode':'markers',
        'marker': {
            #cmax: 12, 
            #cmin: 2, 

            'cauto': False, 


            'color': df_Blackroute['Secondsr'],
            'colorscale' : 'viridis',
            'opacity' : 0.5,
            'showscale':False,
        },

        'text': df_Blackroute['Secondsr'],
}

## Add AIS Data to Plot

trace5scatt = {
        "type": "scattermapbox",
        'name': 'Passenger Vessel - AIS', 

        'lat': df_ais_blue['Latitude'],
        'lon': df_ais_blue['Longitude'],
        'mode':'markers',
        'marker':{

            'cauto': False, 

            'size':3,
            'color': '#0000FF',
            'opacity' : 0.8,
    }}

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
                            'z': df_fogarray['fog'][df_fogarray['time'] == 0],
                            'locations':df_fogarray['ids'][df_fogarray['time'] == 0],
                            'colorscale': [[0, 'rgba(2, 71, 156, 0.0)'], [1.0, 'rgba(250, 250, 250, 0.8)']],
                            # 'colorscale':'purp',
                            # 'colorbar':dict(thickness:20, ticklen:3),
                            'geojson': grid24df,
                            'legendgroup' : "Dynamic Scenario Elements",  # this can be any string, not just "group"
                            # legendgrouptitle :"Weather",
                            'showlegend':True,
                            'showscale':False,
                            'text' : df_fogarray['fog'][df_fogarray['time'] == 0],
                            'visible' :  "legendonly",
                            'hovertemplate': "Visibility Rating (fog/rain) : %{z}",
                            'marker_line_width':1, 
                            # marker_opacity:0.5
}

ceilingchlor = {
                            'type' : 'choroplethmapbox',
                            'name' : 'Cloud Ceiling',
                            'z': df_ceilingarray['ceiling'][df_ceilingarray['time'] == 0],
                            'locations':df_ceilingarray['ids'][df_ceilingarray['time'] == 0],
                            'colorscale': [[0, 'rgba(255,255,255, 0.0)'], [0.05, 'rgba(227,238,245, 0.4)'], [0.5, 'rgba(157,186,217, 0.5)'], [1.0, 'rgba(113,25,117, 0.6)']],
                            # 'colorscale':'purp',
                            # 'colorbar':dict(thickness:20, ticklen:3),
                            'geojson': grid24df,
                            'legendgroup' : "Dynamic Scenario Elements",  # this can be any string, not just "group"
                            # legendgrouptitle :"Weather",
                            'showlegend':True,
                            'showscale':False,
                            'text' : df_ceilingarray['ceiling'][df_ceilingarray['time'] == 0],
                            'visible' :  "legendonly",
                            'hovertemplate': "Ceiling Altitude (ft) : %{z}",
                            'marker_line_width':1, 
                            # marker_opacity:0.5
}

navchlor = {
                            'type' : 'choroplethmapbox',
                            'name' : 'Navigable Waters',
                            'z' : df_griddata['Navigation'],
                            'locations' : df_griddata['ids'],
                            'colorscale' : [[0, 'rgba(0, 0, 255, 0.0)'], [1.0, 'rgba(0, 107, 7, 0.8)']],
                            # 'colorscale':'purp',
                            'colorbar':dict(thickness=20, ticklen=3),
                            'geojson': grid24df,
                            # legendgroup:"Navigation",  # this can be any string, not just "group"
                            # legendgrouptitle_text:"Navigation",
                            'showlegend':True,
                            'showscale':False,
                            'text' : df_griddata['Navigation'],
#                             'text':'text',
                            'hoverinfo':'all',
                            'marker_line_width':1, 
                            # marker_opacity:0.5
}


originchlor = {
                            'type' : 'choroplethmapbox',
                            'name' : 'Origins',
                            'z': df_griddata['Origin'],
                            'locations':df_griddata['ids'],
                            'colorscale': [[0, 'rgba(168, 192, 247, 0.0)'], [1.0, 'rgba(0, 255, 0, 0.9)']],
                            # 'colorscale':'purp',
                            'colorbar':dict(thickness=20, ticklen=3),
                            'geojson': grid24df,
                            'showlegend':True,
                            'showscale':False,
                            'legendgroup':"Navigation",
                            'text' : df_griddata['Origin'],
                            # visible :  "legendonly",
                            'hoverinfo':'skip',
                            'marker_line_width':1, 
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
                            'geojson': grid24df,
                            'showlegend':True,
                            'showscale':False,
                            'legendgroup':"Navigation",
                            'text' : df_griddata['Destination'],
                            # visible :  "legendonly",
                            'hoverinfo':'skip',
                            'marker_line_width':1, 
                            # marker_opacity:0.5
}


historicalchlor = {
                            'type' : 'choroplethmapbox',
                            'name' : 'Historical Trafficking Routes',
                            'z': df_griddata['Historical Trafficking Routes'],
                            'locations':df_griddata['ids'],
                            'colorscale':[[0, 'rgba(70,3,159,0.2)'], [0.5, 'rgba(219,92,104,0.5)'], [1.0, 'rgba(241,244,33,0.8)']],
                            # 'colorbar':dict(thickness:20, ticklen:3),
                            'geojson': grid24df,
                            'legendgroup':"Creative Insights",
                            'legendgrouptitle' : dict( text = "Creative Insights"),  # this can be any string, not just "group"
                            # legendgrouptitle:"Supplemental Data",
                            'showlegend':True,
                            'showscale':False,
                            'text' : df_griddata['Historical Trafficking Routes'],
                            'visible' :  "legendonly",
#                             'text':'text',
                            'hoverinfo':'skip',
                            'marker_line_width':1, 
                            # marker_opacity:0.5
}

aischlor = {
                            'type' : 'choroplethmapbox',
                            'name' : 'AIS Aggregation',
                            'z': df_griddata['AIS'],
                            'locations':df_griddata['ids'],
                            'colorscale':[[0, 'rgba(192, 131, 252, 0.1)'], [1.0, 'rgba(255, 153, 0, 0.8)']],
                            # 'colorbar':dict(thickness:20, ticklen:3),
                            'geojson': grid24df,
                            'legendgroup':"Creative Insights",  # this can be any string, not just "group"
                            # legendgrouptitle:"Supplemental Data",
                            'showlegend':True,
                            'showscale':False,
                            'text' : df_griddata['AIS'],
                            'visible' :  "legendonly",
#                             'text':'text',
                            'hoverinfo':'all',
                            'hovertemplate': "Maritime Activity (# AIS Vessels in region) : %{z}",
                            'marker_line_width':1, 
                            # marker_opacity:0.5
}

waveschlor = {
                            'type' : 'choroplethmapbox',
                            'name' : 'Sea State',
                            'z': waves['Wave Height'],
                            'locations': waves['ids'],
                            # 'colorscale':'jet',
                            'colorscale':[[0, 'rgba(4,115,255, 0.1)'], [1.0, 'rgba(254,41,147, 0.9)']],
                            # 'colorscale':[[0, 'rgba(4,115,255,0.1)'], [0.6, 'rgba(147,7,0,0.7)'], [0.7, 'rgba(118,0,60,0.8)'], [1.0, 'rgba(254,41,147,0.8)']],
                            # 'colorbar':dict(thickness:20, ticklen:3),
                            'geojson': grid24df,
                            'legendgroup':"Dynamic Scenario Elements",  # this can be any string, not just "group"
                            # legendgrouptitle:"Supplemental Data",
                            'showlegend':True,
                            'showscale':False,
                            # 'text' : waves['text'],
                            'visible' :  "legendonly",
                            'hovertemplate': "Wave Height (ft) : %{z}",
                            # 'hoverinfo':'all',
                            'marker_line_width':1, 
                            # marker_opacity:0.5
}

tracetargetbase = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Target X', 
         'lon': [df.loc[0, 'Longitude']], 
         'lat': [df.loc[0, 'Latitude']], 
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 10, 'color':'#ff3030'},
         'mode': 'markers', 
         'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'targets',
         'legendgrouptitle' : dict( text = "Target Characteristics"),
         'showlegend': True, 
        #  'customdata' : [df['heading'], df['heading'], df['freeboard']],
         'customdata' : np.stack((df['velocity'], df['heading'], df['freeboard']), axis=-1),
         'hovertemplate': "<br>".join([
                            "Velocity (km/hr) : %{customdata[0]}",
                            "Heading (degrees) : %{customdata[1]}",
                            "Freeboard (kgs load) : %{customdata[2]}",
         ])
}

trace_0 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Target RL routes', 
         'lon': [rltracks0.loc[0, 'Longitude']], 
         'lat': [rltracks0.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 8, 
                    'color': [rltracks0.loc[0, 'rank']],
                    'colorscale': 'reds',
                    'cmin' : 0,
                    'cmax' : 2000,
                    },
         'mode': 'markers+lines', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'targets',
         'legendgrouptitle' : dict( text = "Target Characteristics"),
         'showlegend': True, 
}

trace_400 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'RL route_400', 
         'lon': [rltracks400.loc[0, 'Longitude']], 
         'lat': [rltracks400.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 8, 
                    'color': [rltracks400.loc[0, 'rank']],
                    'colorscale': 'reds',
                    'cmin' : 0,
                    'cmax' : 2000,
                    },
         'mode': 'markers+lines', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'targets',
         'legendgrouptitle' : dict( text = "Target Characteristics"),
         'showlegend': True, 
}

trace_800 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'RL route_800', 
         'lon': [rltracks800.loc[0, 'Longitude']], 
         'lat': [rltracks800.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 8, 
                    'color': [rltracks800.loc[0, 'rank']],
                    'colorscale': 'reds',
                    'cmin' : 0,
                    'cmax' : 2000,
                    },
         'mode': 'markers+lines', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'targets',
         'legendgrouptitle' : dict( text = "Target Characteristics"),
         'showlegend': True, 
}

trace_1200 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'RL route_1200', 
         'lon': [rltracks1200.loc[0, 'Longitude']], 
         'lat': [rltracks1200.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 8, 
                    'color': [rltracks1200.loc[0, 'rank']],
                    'colorscale': 'reds',
                    'cmin' : 0,
                    'cmax' : 2000,
                    # 'color': [rltracks1200.loc[rltracks1200['time'] == 0, 'rank']]
                    },
         'mode': 'markers+lines', 
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'targets',
         'legendgrouptitle' : dict( text = "Target Characteristics"),
         'showlegend': True, 
}

trace_1600 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'RL route_1600', 
         'lon': [rltracks1600.loc[0, 'Longitude']], 
         'lat': [rltracks1600.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 6, 
                    'color': [rltracks1600.loc[0, 'rank']],
                    'colorscale': 'reds',
                    'cmin' : 0,
                    'cmax' : 2000,
                    # 'color': [rltracks1200.loc[rltracks1200['time'] == 0, 'rank']]
                    },
         'mode': "markers+lines",
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'targets',
         'legendgrouptitle' : dict( text = "Target Characteristics"),
         'showlegend': True, 
}

trace_2000 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'RL route_2000', 
         'lon': [rltracks2000.loc[0, 'Longitude']], 
         'lat': [rltracks2000.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 6, 
                    'color': [rltracks2000.loc[0, 'rank']],
                    'colorscale': 'reds',
                    'cmin' : 0,
                    'cmax' : 2800,
                    # 'color': [rltracks1200.loc[rltracks1200['time'] == 0, 'rank']]
                    },
         'mode': "markers+lines",
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'targets',
         'legendgrouptitle' : dict( text = "Target Characteristics"),
         'showlegend': True, 
}

trace_2800 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'RL route_2800', 
         'lon': [rltracks2800.loc[0, 'Longitude']], 
         'lat': [rltracks2800.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 6, 
                    'color': [rltracks2800.loc[0, 'rank']],
                    'colorscale': 'reds',
                    'cmin' : 0,
                    'cmax' : 2800,
                    # 'color': [rltracks1200.loc[rltracks1200['time'] == 0, 'rank']]
                    },
         'mode': "markers+lines",
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'targets',
         'legendgrouptitle' : dict( text = "Target Characteristics"),
         'showlegend': True, 
}

trace_3600 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'RL route_3600', 
         'lon': [rltracks3600.loc[0, 'Longitude']], 
         'lat': [rltracks3600.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 20, 
                    'color': [rltracks3600.loc[0, 'rank']],
                    'colorscale': 'reds',
                    'cmin' : 0,
                    'cmax' : 4200,
                    # 'color': [rltracks1200.loc[rltracks1200['time'] == 0, 'rank']]
                    },
         'mode': "markers+lines",
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'targets',
         'legendgrouptitle' : dict( text = "Target Characteristics"),
         'showlegend': True, 
}

trace_3999 = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'RL route_3999', 
         'lon': [rltracks3999.loc[0, 'Longitude']], 
         'lat': [rltracks3999.loc[0, 'Latitude']], 
        #  'fillcolor' : [rltracks.loc[0, 'rank']],
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 6, 
                    # 'color': [rltracks3999.loc[0, 'rank']],
                    # 'colorscale': 'reds',
                    # 'cmin' : 0,
                    # 'cmax' : 4200,
                    'symbol' : [rltracks3999.loc[0, 'symbol']]
                    # 'color': [rltracks1200.loc[rltracks1200['time'] == 0, 'rank']]
                    },
         'mode': "markers+lines",
        #  'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'targets',
         'legendgrouptitle' : dict( text = "Target Characteristics"),
         'showlegend': True, 
}

tracerosabase = {
        'type': "scattermapbox", # This trace is identified inside frames as trace 0
         'name': 'Target Y', 
         'lon': [df_rosa.loc[0, 'Longitude']], 
         'lat': [df_rosa.loc[0, 'Latitude']], 
        #  'hoverinfo': 'name+text', 
         'marker': {'size': 10, 'color':'#cc0000'},
         'mode': 'markers', 
         'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'targets',
         'legendgrouptitle' : dict( text = "Target Characteristics"),
         'showlegend': True, 
        #  'customdata' : [df['heading'], df['heading'], df['freeboard']],
         'customdata' : np.stack((df_rosa['velocity'], df_rosa['heading'], df_rosa['freeboard']), axis=-1),
         'hovertemplate': "<br>".join([
                            "Velocity (km/hr) : %{customdata[0]}",
                            "Heading (degrees) : %{customdata[1]}",
                            "Freeboard (kgs load) : %{customdata[2]}",
         ])
}

# traceBlackbase = {
#         'type': 'scattermapbox', # This trace is identified inside frames as trace 1
#         'name': 'Replace Target', 
#         'lon': [df_Blackroute.loc[0, 'Longitude']],
#         'lat': [df_Blackroute.loc[0, 'Latitude']],
#         'mode': 'markers',
#         'legendgroup': 'targets',
#         'marker': {'size': 10, 'color':'#fc5603'},
#         }

tracegridbase={
        'type': 'choroplethmapbox', # This trace is identified inside frames as trace 2
        'name': 'Navigable Waters', 
        'z': df_griddata['Navigation'],
        'locations': df_griddata['ids'],
         'colorscale': [[0, 'rgba(0, 0, 255, 0.0)'], [1.0, 'rgba(0, 107, 7, 0.8)']],
        'geojson': grid24df,
         'showlegend' :True,
        'showscale':False,
        'legendgroup': 'targets',
        'text' : df_griddata['Navigation'],
#                             text=text,
        'hoverinfo':'all',
        'marker_line_width':1, 
        }

traceneuralmap={
        'type': 'choroplethmapbox',
        'name' : 'RL Gameboard 24 x 24',
        'z': nmmo1['Land'],
        'locations':nmmo1['ids'],
        'colorscale': [[0, 'rgba(255, 255, 255, 0.45)'], [0.5, 'rgba(82, 109, 242, 0.1)'], [1.0, 'rgba(0, 107, 7, 0.6)']],
        # 'colorscale'='purp',
        'colorbar':dict(thickness=20, ticklen=3),
        'geojson': grid24df,
        'legendgroup' : "Navigation", 
        'legendgrouptitle' : dict( text = "Geographic Factors"), 
        # legendgrouptitle_'text'="Navigation",
        'showlegend':True,
        'showscale':False,
        'text' : nmmo1['map_tiles'],
        'legendrank': 1,
        # 'hoverinfo':'all',
#                             'text'='text',
        'hoverinfo':'skip',
        'marker_line_width':1, 
        # marker_opacity=0.5
} 

trac26nmmap={
        'type': 'choroplethmapbox',
        'name' : 'Neural MMO Map 26',
        'z': nmmo26['Land'],
        'locations':nmmo26['ids'],
        'colorscale': [[0, 'rgba(190, 191, 196, 0.4)'], [0.5, 'rgba(82, 109, 242, 0.4)'], [1.0, 'rgba(0, 107, 7, 0.4)']],
        # 'colorscale'='purp',
        'colorbar':dict(thickness=20, ticklen=3),
        'geojson': grid26,
        # legendgroup="Navigation",  # this can be any string, not just "group"
        'legendgrouptitle' : dict( text = "Geographic Factors"), 
        'showlegend':True,
        'showscale':False,
        'text' : nmmo26['map_tiles'],
#                             'text'='text',
        'hoverinfo':'all',
        'marker_line_width':1, 
        # marker_opacity=0.5
} 

layout = dict(
            template= "plotly_dark",
            height=600,
    
            mapbox=dict(accesstoken=mapbox_access_token,
                              bearing=0,
                              center=dict(lat=3.5,
                              lon=-95),
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


                   dict(
                           type= "scattermapbox",
                           lat=rltracks0.loc[:k+1, 'Latitude'].tolist(), 
                          lon=rltracks0.loc[:k+1, 'Longitude'].tolist()),

                    dict(
                           type= "scattermapbox",
                           lat=rltracks400.loc[:k+1, 'Latitude'].tolist(), 
                          lon=rltracks400.loc[:k+1, 'Longitude'].tolist()),
                    dict(
                           type= "scattermapbox",
                           lat=rltracks800.loc[:k+1, 'Latitude'].tolist(), 
                          lon=rltracks800.loc[:k+1, 'Longitude'].tolist()),
                    dict(
                           type= "scattermapbox",
                           lat=rltracks1200.loc[:k+1, 'Latitude'].tolist(), 
                          lon=rltracks1200.loc[:k+1, 'Longitude'].tolist()),
                    dict(
                           type= "scattermapbox",
                           lat=rltracks1600.loc[:k+1, 'Latitude'].tolist(), 
                          lon=rltracks1600.loc[:k+1, 'Longitude'].tolist()),
                    dict(
                           type= "scattermapbox",
                           lat=rltracks2000.loc[:k+1, 'Latitude'].tolist(), 
                          lon=rltracks2000.loc[:k+1, 'Longitude'].tolist()),
                    dict(
                           type= "scattermapbox",
                           lat=rltracks2800.loc[:k+1, 'Latitude'].tolist(), 
                          lon=rltracks2800.loc[:k+1, 'Longitude'].tolist()),
                    dict(
                           type= "scattermapbox",
                           lat=rltracks3600.loc[:k+1, 'Latitude'].tolist(), 
                          lon=rltracks3600.loc[:k+1, 'Longitude'].tolist()),
                    dict(
                           type= "scattermapbox",
                           lat=rltracks3999.loc[:k+1, 'Latitude'].tolist(), 
                           lon=rltracks3999.loc[:k+1, 'Longitude'].tolist(),
                           marker=dict( symbol = rltracks3999.loc[:k+1, 'symbol'].tolist())
                           ),
                    # dict(
                    #    type= "scattermapbox",
                       
                    #    lat=[df_rosa.loc[k, 'Latitude']], 
                    #     lon=[df_rosa.loc[k, 'Longitude']],
                        
                    #    ),
                    dict(
                       type= "choroplethmapbox",
                       
                        z = df_daylight['Daylight2'][df_daylight['time']==k],
                        locations = df_daylight['ids'][df_daylight['time']==k],
                        geojson = grid24df,
                        
                       ),
                    dict(
                       type= "choroplethmapbox",
                       
                       z = df_fogarray['fog'][df_fogarray['time'] == k],
                        locations = df_fogarray['ids'][df_fogarray['time'] == k],
                        geojson = grid24df,
                        
                       ),
                    dict(
                       type= "choroplethmapbox",
                       
                        z = df_ceilingarray['ceiling'][df_ceilingarray['time'] == k],
                        locations = df_ceilingarray['ids'][df_ceilingarray['time'] == k],
                        geojson = grid24df,
                        
                       )

                   ],
               traces=[0,1,2,3,4,5,6,7,8]) for k in range(N)]

updatemenus=[dict(type='buttons', showactive=False,
                                y=0,
                                x=1.05,
                                xanchor='right',
                                yanchor='top',
                                pad=dict(t=0, r=10),
                                buttons=[dict(label='Play',
                                              method='animate',
                                              args=[None, 
                                                    dict(frame=dict(duration=500, 
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

# sliders = [dict(steps= [dict(method= 'animate',
#                            args= [[ f'frame{k}'],
#                                   dict(mode= 'immediate',
#                                   frame= dict(duration=200, redraw= False ),
#                                               transition=dict( duration= 0))
#                                  ],
#                             label='{:d}'.format(k)
#                              ) for k in range(N)], 
#                 transition= dict(duration= 0 ),
#                 x=0,#slider starting position  
#                 y=0, 
#                 currentvalue=dict(font=dict(size=12), 
#                                   prefix='Point: ', 
#                                   visible=True, 
#                                   xanchor= 'center'),  
#                 len=1.0)
#            ]

sliders = [dict(steps= [dict(method= 'animate',
                           args= [[k],
                                  dict(mode= 'immediate',
                                  frame= dict(duration=500, redraw= True ),
                                              transition=dict( duration= 0))
                                 ],
                            label=k
                             ) for k in range(N)], 
                transition= dict(duration= 0 ),
                x=0,#slider starting position  
                y=0, 
                currentvalue=dict(font=dict(size=12), 
                                  prefix='Hour: ', 
                                  visible=True, 
                                  xanchor= 'center'),  
                len=1.0)
           ]



# data = [
#         {'type': "scattermapbox", # This trace is identified inside frames as trace 0
#          'name': 'f1', 
#          'lon': [df.loc[0, 'Longitude']], 
#          'lat': [df.loc[0, 'Latitude']], 
#          'hoverinfo': 'name+text', 
#          'marker': {'size': 10, 'color':'blue'},
#          'mode': 'markers', 
#          'fillcolor': 'rgba(255,79,38,0.600000)', 
#          'legendgroup': 'f1',
#          'showlegend': True, 
#          },
#         {'type': 'scattermapbox', # This trace is identified inside frames as trace 1
#         'name': 'f12', 
#         'lon': [df_Blackroute.loc[0, 'Longitude']],
#         'lat': [df_Blackroute.loc[0, 'Latitude']],
#         'mode': 'markers',
#         'marker': {'size': 10, 'color':'blue'},
#         },
    
#     ## Not Animated
    
#         {'type': 'choroplethmapbox', # This trace is identified inside frames as trace 2
#         'name': 'Navigable Waters', 
#         'z': df_griddata['Navigation'],
#         'locations': df_griddata['ids'],
#          'colorscale': [[0, 'rgba(0, 0, 255, 0.0)'], [1.0, 'rgba(0, 107, 7, 0.8)']],
#         'geojson': grid24df,
#          'showlegend' :True,
#         'showscale':False,
#         'text' : df_griddata['Navigation'],
# #                             text=text,
#         'hoverinfo':'all',
#         'marker_line_width':1, 
#         },

#     ]

data = [
    trace_0,
    trace_400,
    trace_800,
    trace_1200,
    trace_1600,
    trace_2000,
    trace_2800,
    trace_3600,
    trace_3999,
    # tracetargetbase,
    # tracerosabase,
    # traceBlackbase,
    daylightchlor,
    fogchlor,
    ceilingchlor,
    waveschlor,
    traceneuralmap,
    # trac26nmmap,
    # tracegridbase,
    # trace2path,
    # trace50path,
    # trace300path,
    # trace500path,
    # trace1000path,
    historicalchlor,
    # aischlor,
    destinationchlor,
    originchlor,
    # trace2path,
    # trace50path,
    # trace300path,
    # trace500path,
    # trace1000path,
    # trace2000path
]

fig = dict(
    layout = layout,
    data = data
    )

fig.update(frames=frames),
fig['layout'].update(updatemenus=updatemenus,
          sliders=sliders)

fig3 = go.Figure(fig)



number_input = html.Div(
    [
        html.H4('Intel Report'),
        html.P("Enter Departure Location"),
        dbc.Input(type="number", min=0, max=180, step=0.05),
    ],
    id="styled-numeric-input",
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

        dbc.Row(
            [
                dbc.Col(
                    [
                        # dcc.Graph( figure= fig ),

                        dcc.Graph( 
                            # figure = figGameboard,
                                    figure = fig3),
                        # dbc.Row(
                        #     [
                        #         html.Div([select], style={"width": "50%"}),
                        #         popover,
                        #         html.Div(id='dataselected')
                        #     ]
                        # )

                    ],
                    width = 12
                ),

                # dbc.Col(
                #     [
                #         # html.Div( sliderin ),
                #         # dcc.Graph( figure= fig ),
                #         # dcc.Graph( figure = figGameboard),
                #         dcc.Graph(id='graph-moving'),
                #         # dbc.Row(
                #         #     [
                #         #         html.Div([select], style={"width": "50%"}),
                #         #         popover,
                #         #         html.Div(id='dataselected')
                #         #     ]
                #         # )

                #     ],
                #     width = 6
                # ),
            ]
            
        ),
        
        dbc.Row(
            [
                dbc.Col(
                    number_input,

                ),

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
                        html.Div(id='intermediate-value', style={'display': 'none'}),
                        html.Div(id='intermediate-value2', style={'display': 'none'}),
                        html.Div(id='intermediate-value3', style={'display': 'none'}),
                        
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
        # navbar,
        row,
        html.Div(html.Br(), style={'backgroundColor': '#f6f5f2', 'height': 60})
        ],
    fluid=True

    )
    ],
    style={'backgroundColor': '#2b2b2b'})





# @app.callback(
#     Output('graph-moving', 'figure'),
#     [Input('intermediate-value', 'children'),
#     Input('intermediate-value2', 'children'),
#     Input('intermediate-value3', 'children')
#     ])
# def update_figure(filta, filtpath, fake):

#     dfin = pd.read_json(filta, orient='split')

#     dfpath = pd.read_json(filtpath, orient='split')

#     dfpathfake = pd.read_json(fake, orient='split')



    
    

#     figanimate = go.Figure(go.Choroplethmapbox(
#                             name = 'Day or Night',
#                             z= dfin['Daylight2'],
#                             'locations'=dfin['ids'],
#                             zmin= 0,
#                             zmax = 2,
#                             'colorscale'= [[0, 'rgba(0, 0, 0, 0.2)'], [1.0, 'rgba(236, 245, 66, 0.2)']],
#                             # 'colorscale'='purp',
#                             'colorbar'=dict(thickness=20, ticklen=3),
#                             'geojson'= grid24df,
#                             # legendgroup="Weather",  # this can be any string, not just "group"
#                             # legendgrouptitlet="Weather",
#                             'showlegend'=True,
#                             'showscale'=False,
#                             'text' = dfin['Daylight2'],
#                             # 'visible' =  "legendonly",
#                             'hoverinfo'='all',
#                             'marker_line_width'=1, 
#                             # marker_opacity=0.5
#                             )) 
    
#     figanimate.add_trace(go.Scattermapbox(
#             name= 'Target Path - Temporal Difference', 

#             lat= dfpath['Latitude'],
#             lon= dfpath['Longitude'],
#             mode='markers',
#             marker=go.scattermapbox.Marker(

#                 cauto= False, 

#                 size=10,
#                 color= '#FF0000',
#                 opacity = 0.8,

                
#             ),

#         ))
    
#     figanimate.add_trace(go.Scattermapbox(
#             name= 'Target X', 

#             lat= dfpathfake['Latitude'],
#             lon= dfpathfake['Longitude'],
#             mode='markers',
#             marker=go.scattermapbox.Marker(

#                 cauto= False, 

#                 size=10,
#                 color= '#FF0000',
#                 opacity = 0.8,

                
#             ),

#         ))

#     figanimate.add_trace(go.Choroplethmapbox(
#                                     name = 'Navigable Waters',
#                                     z= df_griddata['Navigation'],
#                                     'locations'=df_griddata['ids'],
#                                     'colorscale'= [[0, 'rgba(0, 0, 255, 0.0)'], [1.0, 'rgba(0, 107, 7, 0.8)']],
#                                     # 'colorscale'='purp',
#                                     'colorbar'=dict(thickness=20, ticklen=3),
#                                     'geojson'= grid24df,
#                                     # legendgroup="Navigation",  # this can be any string, not just "group"
#                                     # legendgrouptitle_'text'="Navigation",
#                                     'showlegend'=True,
#                                     'showscale'=False,
#                                     'text' = df_griddata['Navigation'],
#         #                             'text'='text',
#                                     'hoverinfo'='all',
#                                     'marker_line_width'=1, 
#                                     # marker_opacity=0.5
#                                     )) 

#     figanimate.add_trace(go.Choroplethmapbox(
#                                     name = 'Neural MMO Map1',
#                                     z= nmmo1['Land'],
#                                     'locations'=nmmo1['ids'],
#                                     'colorscale'= [[0, 'rgba(190, 191, 196, 0.4)'], [0.5, 'rgba(82, 109, 242, 0.4)'], [1.0, 'rgba(0, 107, 7, 0.4)']],
#                                     # 'colorscale'='purp',
#                                     'colorbar'=dict(thickness=20, ticklen=3),
#                                     'geojson'= grid24df,
#                                     # legendgroup="Navigation",  # this can be any string, not just "group"
#                                     # legendgrouptitle_'text'="Navigation",
#                                     'showlegend'=True,
#                                     'showscale'=False,
#                                     'text' = nmmo1['map_tiles'],
#         #                             'text'='text',
#                                     'hoverinfo'='all',
#                                     'marker_line_width'=1, 
#                                     # marker_opacity=0.5
#                                     )) 



#     figanimate.add_trace(go.Choroplethmapbox(
#                                     name = 'Origins',
#                                     z= df_griddata['Origin'],
#                                     'locations'=df_griddata['ids'],
#                                     'colorscale'= [[0, 'rgba(168, 192, 247, 0.0)'], [1.0, 'rgba(0, 255, 0, 0.9)']],
#                                     # 'colorscale'='purp',
#                                     'colorbar'=dict(thickness=20, ticklen=3),
#                                     'geojson'= grid24df,
#                                     'showlegend'=True,
#                                     'showscale'=False,
#                                     # legendgroup="Navigation",
#                                     'text' = df_griddata['Origin'],
#                                     # visible =  "legendonly",
#                                     'hoverinfo'='all',
#                                     'marker_line_width'=1, 
#                                     # marker_opacity=0.5
#                                     ))

#     figanimate.add_trace(go.Choroplethmapbox(
#                                     name = 'Destinations',
#                                     z= df_griddata['Destination'],
#                                     'locations'=df_griddata['ids'],
#                                     'colorscale'= [[0, 'rgba(168, 192, 247, 0.0)'], [1.0, 'rgba(110, 1, 1, 0.8)']],
#                                     # 'colorscale'='purp',
#                                     'colorbar'=dict(thickness=20, ticklen=3),
#                                     'geojson'= grid24df,
#                                     'showlegend'=True,
#                                     'showscale'=False,
#                                     # legendgroup="Navigation",
#                                     'text' = df_griddata['Destination'],
#                                     # visible =  "legendonly",
#                                     'hoverinfo'='all',
#                                     'marker_line_width'=1, 
#                                     # marker_opacity=0.5
#                                     ))


#     figanimate.add_trace(go.Choroplethmapbox(
#                                     name = 'Fog',
#                                     z= df_griddata['Fog'],
#                                     'locations'=df_griddata['ids'],
#                                     'colorscale'= [[0, 'rgba(2, 71, 156, 0.0)'], [1.0, 'rgba(250, 250, 250, 0.8)']],
#                                     # 'colorscale'='purp',
#                                     'colorbar'=dict(thickness=20, ticklen=3),
#                                     'geojson'= grid24df,
#                                     # legendgroup="Weather",  # this can be any string, not just "group"
#                                     # legendgrouptitlet="Weather",
#                                     'showlegend'=True,
#                                     'showscale'=False,
#                                     'text' = df_griddata['Fog'],
#                                     'visible' =  "legendonly",
#                                     'hoverinfo'='all',
#                                     'marker_line_width'=1, 
#                                     # marker_opacity=0.5
#                                     )) 



#     figanimate.add_trace(go.Choroplethmapbox(
#                                     name = 'Historical Trafficking Routes',
#                                     z= df_griddata['Historical Trafficking Routes'],
#                                     'locations'=df_griddata['ids'],
#                                     'colorscale'=[[0, 'rgba(70,3,159,0.2)'], [0.5, 'rgba(219,92,104,0.5)'], [1.0, 'rgba(241,244,33,0.8)']],
#                                     'colorbar'=dict(thickness=20, ticklen=3),
#                                     'geojson'= grid24df,
#                                     # legendgroup="Supplemental Data",  # this can be any string, not just "group"
#                                     # legendgrouptitle="Supplemental Data",
#                                     'showlegend'=True,
#                                     'showscale'=False,
#                                     'text' = df_griddata['Historical Trafficking Routes'],
#                                     'visible' =  "legendonly",
#         #                             'text'='text',
#                                     'hoverinfo'='all',
#                                     'marker_line_width'=1, 
#                                     # marker_opacity=0.5
#                                     )) 

#     figanimate.add_trace(go.Choroplethmapbox(
#                                     name = 'AIS',
#                                     z= df_griddata['AIS'],
#                                     'locations'=df_griddata['ids'],
#                                     'colorscale'=[[0, 'rgba(192, 131, 252, 0.1)'], [1.0, 'rgba(255, 153, 0, 0.8)']],
#                                     'colorbar'=dict(thickness=20, ticklen=3),
#                                     'geojson'= grid24df,
#                                     # legendgroup="Supplemental Data",  # this can be any string, not just "group"
#                                     # legendgrouptitle="Supplemental Data",
#                                     'showlegend'=True,
#                                     'showscale'=False,
#                                     'text' = df_griddata['AIS'],
#                                     'visible' =  "legendonly",
#         #                             'text'='text',
#                                     'hoverinfo'='all',
#                                     'marker_line_width'=1, 
#                                     # marker_opacity=0.5
#                                     )) 

#         # figanimate.add_trace(go.Scattermapbox(
#         #     name= 'Nav', 

#         #     lat= navigation['Latitude'],
#         #     lon= navigation['Longitude'],
#         #     mode='markers',
#         #     marker=go.scattermapbox.Marker(

#         #         cauto= False, 
#         #         size=3,

#         #         color= 'yellow',
#         #         opacity = 0.8,

                
#         #     ),

#         # ))

#     figanimate.update_layout(
#                 # title = 'Gameboard',
            
#                 template= "plotly_dark",
#                 height=575,
#                 # autosize=True,
#                 hovermode='closest',
#                 mapbox=dict(
#                     accesstoken=mapbox_access_token,
#                     style= "satellite",
#                     bearing=0,
#                     center=dict(
#                         # lat=latm,
#                         # lon=lonm
#                         lat=3.5,
#                         lon=-95
#                     ),
#                     pitch=0,
#                     zoom=3.7
#                     # zoom=13.529401748965746
#                 ),
#                 legend=dict(
#                     yanchor="bottom",
#                     y=0.05,
#                     xanchor="left",
#                     x=0.01
#                 ),
#                     margin= {
#                             "b": 5, 
#                             "l": 5, 
#                             "r": 5, 
#                             "t": 5
#                         }, 
#             )

#     return figanimate

########### Run the app
if __name__ == '__main__':
    application.run(debug=True, port=8080)


# if __name__ == '__main__':
#     application.run(debug=True, port=8080)
