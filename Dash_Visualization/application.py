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



mintime = df_Blackroute['Secondsr'].min()
maxtime = df_Blackroute['Secondsr'].max()

#Load 12 mile territorial line

# f = open(r'C:\Users\tjack\Documents\HackTheMachine\12milefileid.json',)
 
# returns JSON object as
# a dictionary
# jdata = json.load(f)

urljson1 = "https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Grids/12milefile.json"
  
# store the response of URL
response1 = urlopen(urljson1)
  
# storing the JSON response 
# from url in data
jdata = json.loads(response1.read())

# values
jdatadf = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/Grids/12milefileid.csv')

## read in 8 by 8 grid
# Opening JSON file
# f1 = open(r'C:\Users\tjack\Documents\HackTheMachine\8by8.json',)
 
# returns JSON object as
# a dictionary
# griddf = json.load(f1)

# for k in range(len(griddf['features'])):
#     griddf['features'][k]['id'] = k

# ids = [features['id'] for features in griddf["features"]]

# dfn = pd.DataFrame()
# dfn['ids'] = (ids)
# dfn['value'] = 5
# dfn['text'] =  dfn.apply(lambda x: "Gameboard Index:" + str(x.ids), axis=1)

# ## read in 16 by 16 grid
# # Opening JSON file
# f16 = open(r'C:\Users\tjack\Documents\HackTheMachine\16by16.json',)
# f16new = open(r'C:\Users\tjack\Documents\HackTheMachine\16by16new.json',)
 
# # returns JSON object as
# # a dictionary
# grid16df = json.load(f16)

# grid16dfnew= json.load(f16new)

# for k in range(len(grid16df['features'])):
#     grid16df['features'][k]['id'] = k

# ids16 = [features['id'] for features in grid16df["features"]]

# dfn16 = pd.DataFrame()
# dfn16['ids'] = (ids16)
# dfn16['value'] = 2
# dfn16['text'] =  dfn16.apply(lambda x: "Gameboard Index:" + str(x.ids), axis=1)

# #For new json

# for k in range(len(grid16dfnew['features'])):
#     grid16dfnew['features'][k]['id'] = k

# ids16new = [features['id'] for features in grid16dfnew["features"]]

# dfn16new = pd.DataFrame()
# dfn16new['ids'] = (ids16new)
# dfn16new['value'] = 3
# dfn16new['text'] =  dfn16new.apply(lambda x: "Gameboard Index:" + str(x.ids), axis=1)

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


#For new json

for k in range(len(grid20df['features'])):
    grid20df['features'][k]['id'] = k

ids20 = [features['id'] for features in grid20df["features"]]

df_griddata = pd.DataFrame()
df_griddata['ids'] = (ids20)
df_griddata['value'] = 3
df_griddata['text'] =  df_griddata.apply(lambda x: "Gameboard Index:" + str(x.ids), axis=1)

# df_griddatain = pd.read_csv(r'C:\Users\tjack\Documents\HackTheMachine\synthetic_data\grid_data_20x20.csv')
df_griddatain = pd.read_csv('https://raw.githubusercontent.com/spear-ai/hackthemachine-unmanned-track-3/dash_visual/Dash_Visualization/synthetic_data/grid_data_20x20.csv')

df_griddata['AIS'] = df_griddatain['AIS']
df_griddata['Navigation'] = df_griddatain['Navigation']
# Navigation Binary
df_griddata['Navigation'].values[df_griddata['Navigation'].values > 1] = 1
## Initiate Plot with Target Data
df_griddata['Fog'] = df_griddatain['Fog']
df_griddata['Origin'] = df_griddatain['Origin']
df_griddata['Destination'] = df_griddatain['Destination']
df_griddata['Historical Trafficking Routes'] = df_griddatain['Historical Trafficking Routes']
df_griddata['High Elevation Clouds'] = df_griddatain['High Elevation Clouds']

fig = go.Figure(go.Scattermapbox(
        name= 'Targets', 
        lat= df_Blackroute['Latitude'],
        lon= df_Blackroute['Longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            #cmax= 12, 
            #cmin= 2, 

            cauto= False, 


            color= df_Blackroute['Secondsr'],
            colorscale = 'viridis',
            opacity = 0.5,
            showscale=False,

            
        ),

        text= df_Blackroute['Secondsr'],
    ))

fig.add_trace(go.Choroplethmapbox(
                            name = 'Gameboard 20 by 20',
                            z= df_griddata['value'],
                            locations=df_griddata['ids'],
                            colorscale='tealgrn',
                            colorbar=dict(thickness=20, ticklen=3),
                            geojson= grid20df,
                            showlegend=True,
                            showscale=False,
                            text = df_griddata['text'],
#                           visible =  "legendonly",
                            hoverinfo='all',
                            marker_line_width=1, 
                            marker_opacity=0.3)) 

## Add AIS Data to Plot

fig.add_trace(go.Scattermapbox(
    name= 'Passenger Vessel - AIS', 

    lat= df_ais_blue['Latitude'],
    lon= df_ais_blue['Longitude'],
    mode='markers',
    marker=go.scattermapbox.Marker(

        cauto= False, 

        size=3,
        color= '#0000FF',
        opacity = 0.8,

        
    ),
    # texttemplate = "%{df1['Latitude']}: %{df1['Latitude']:$,s} <br>(%{df1['Latitude']})",
    # text= df1_s11['Time'],
))

fig.add_trace(go.Scattermapbox(
    name= 'Tanker - AIS', 

    lat= df_ais_red['Latitude'],
    lon= df_ais_red['Longitude'],
    mode='markers',
    marker=go.scattermapbox.Marker(

        cauto= False, 

        size=3,
        color= '#FF0000',
        opacity = 0.8,

        
    ),

))

fig.add_trace(go.Scattermapbox(
    name= 'Cargo Vessel  - AIS', 

    lat= df_ais_green['Latitude'],
    lon= df_ais_green['Longitude'],
    mode='markers',
    marker=go.scattermapbox.Marker(

        cauto= False, 
        size=3,

        color= '#7CFC00',
        opacity = 0.8,

        
    ),

))

## Add Historical Routes Heatmap

fig.add_trace(go.Densitymapbox(
    name = 'Heatmap Historical Routes',
    lat=df_histroutes['Latitude'], 
    lon=df_histroutes['Longitude'], 
    #z=quakes.Magnitude,
    showlegend=True,
    visible =  "legendonly",
    showscale=False,
    radius=3))

# Add Weather Data

fig.add_trace(go.Densitymapbox(
    name = 'Fog',
    lat=df_fog['Latitude'], 
    lon=df_fog['Longitude'], 
    colorscale='greys',
    showlegend=True,
    visible =  "legendonly",
    showscale=False,
    radius=7))

fig.add_trace(go.Densitymapbox(
    name = 'Mid Altitude Clouds',
    lat=df_mediumclouds['Latitude'], 
    lon=df_mediumclouds['Longitude'], 
    colorscale='mint',
    showlegend=True,
    visible =  "legendonly",
    showscale=False,
    radius=7))

fig.add_trace(go.Densitymapbox(
    name = 'High Altititude Clouds',
    lat=df_highclouds['Latitude'], 
    lon=df_highclouds['Longitude'], 
    colorscale='darkmint',
    showlegend=True,
    visible =  "legendonly",
    showscale=False,
    radius=7))

fig.add_trace(go.Densitymapbox(
    name = 'Highest Altitude Clouds',
    lat=df_highestclouds['Latitude'], 
    lon=df_highestclouds['Longitude'], 
    colorscale='pubu',
    showlegend=True,
    visible =  "legendonly",
    showscale=False,
    radius=7))


## Add 12 Mile Territorial Waters

fig.add_trace(go.Choroplethmapbox(
                            name = 'Territorial Waters 12 Miles',
                            z=jdatadf['value'],
                            locations=jdatadf['ids'],
                            colorscale='purp',
                            # colorbar=dict(thickness=20, ticklen=3),
                            geojson=jdata,
                            showlegend=True,
                            showscale=False,
#                             text=text,
                            hoverinfo='all',
                            marker_line_width=1, marker_opacity=0.4))

# fig.add_trace(go.Choroplethmapbox(
#                             name = 'Gameboard 8 x 8',
#                             z=dfn['value'],
#                             locations=dfn['ids'],
#                             colorscale='hot',
#                             colorbar=dict(thickness=20, ticklen=3),
#                             geojson=griddf,
#                             showlegend=True,
#                             showscale=False,
#                             text = dfn['text'],
# #                             text=text,
#                             hoverinfo='all',
#                             marker_line_width=1, 
#                             marker_opacity=0.3)) 
                    
# fig.add_trace(go.Choroplethmapbox(
#                             name = 'Gameboard 16 x 16',
#                             z=dfn16['value'],
#                             locations=dfn16['ids'],
#                             colorscale='tealgrn',
#                             colorbar=dict(thickness=20, ticklen=3),
#                             geojson=grid16df,
#                             showlegend=True,
#                             showscale=False,
#                             text = dfn16['text'],
# #                             text=text,
#                             hoverinfo='all',
#                             marker_line_width=1, 
#                             marker_opacity=0.3)) 



fig.update_layout(
    # title = 'Raw Data',
    template= "plotly_dark",
    height=600,
    # autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style= "satellite",
        bearing=0,
        center=dict(
            # lat=latm,
            # lon=lonm
            lat=3.5,
            lon=-83
        ),
        pitch=0,
        zoom=3.7
        # zoom=13.529401748965746
    ),
    legend=dict(
            yanchor="bottom",
            y=0.05,
            xanchor="left",
            x=0.65
        ),
        margin= {
                "b": 5, 
                "l": 5, 
                "r": 20, 
                "t": 5
            }, 
)


# figGameboard = go.Figure(go.Choroplethmapbox(
#                             name = 'Gameboard 20 by 20',
#                             z= df_griddata['value'],
#                             locations=df_griddata['ids'],
#                             colorscale='tealgrn',
#                             colorbar=dict(thickness=20, ticklen=3),
#                             geojson= grid20df,
#                             showlegend=True,
#                             showscale=False,
#                             text = df_griddata['text'],
# #                           visible =  "legendonly",
#                             hoverinfo='all',
#                             marker_line_width=1, 
#                             marker_opacity=0.3)) 

figGameboard = go.Figure(go.Choroplethmapbox(
                            name = 'Navigable Waters',
                            z= df_griddata['Navigation'],
                            locations=df_griddata['ids'],
                            colorscale= [[0, 'rgba(0, 0, 255, 0.0)'], [1.0, 'rgba(0, 107, 7, 0.8)']],
                            # colorscale='purp',
                            colorbar=dict(thickness=20, ticklen=3),
                            geojson= grid20df,
                            # legendgroup="Navigation",  # this can be any string, not just "group"
                            # legendgrouptitle_text="Navigation",
                            showlegend=True,
                            showscale=False,
                            text = df_griddata['Navigation'],
#                             text=text,
                            hoverinfo='all',
                            marker_line_width=1, 
                            # marker_opacity=0.5
                            )) 

# figGameboard.add_trace(go.Choroplethmapbox(
#                             name = 'Navigable Waters',
#                             z= df_griddata['Navigation'],
#                             locations=df_griddata['ids'],
#                             colorscale= [[0, 'rgba(0, 0, 255, 0.0)'], [1.0, 'rgba(0, 107, 7, 0.8)']],
#                             # colorscale='purp',
#                             colorbar=dict(thickness=20, ticklen=3),
#                             geojson= grid20df,
#                             # legendgroup="Navigation",  # this can be any string, not just "group"
#                             # legendgrouptitle_text="Navigation",
#                             showlegend=True,
#                             showscale=False,
#                             text = df_griddata['Navigation'],
# #                             text=text,
#                             hoverinfo='all',
#                             marker_line_width=1, 
#                             # marker_opacity=0.5
#                             )) 

figGameboard.add_trace(go.Choroplethmapbox(
                            name = 'Origins',
                            z= df_griddata['Origin'],
                            locations=df_griddata['ids'],
                            colorscale= [[0, 'rgba(168, 192, 247, 0.0)'], [1.0, 'rgba(0, 255, 0, 0.9)']],
                            # colorscale='purp',
                            colorbar=dict(thickness=20, ticklen=3),
                            geojson= grid20df,
                            showlegend=True,
                            showscale=False,
                            # legendgroup="Navigation",
                            text = df_griddata['Origin'],
                            # visible =  "legendonly",
                            hoverinfo='all',
                            marker_line_width=1, 
                            # marker_opacity=0.5
                            ))

figGameboard.add_trace(go.Choroplethmapbox(
                            name = 'Destinations',
                            z= df_griddata['Destination'],
                            locations=df_griddata['ids'],
                            colorscale= [[0, 'rgba(168, 192, 247, 0.0)'], [1.0, 'rgba(110, 1, 1, 0.8)']],
                            # colorscale='purp',
                            colorbar=dict(thickness=20, ticklen=3),
                            geojson= grid20df,
                            showlegend=True,
                            showscale=False,
                            # legendgroup="Navigation",
                            text = df_griddata['Destination'],
                            # visible =  "legendonly",
                            hoverinfo='all',
                            marker_line_width=1, 
                            # marker_opacity=0.5
                            ))

figGameboard.add_trace(go.Choroplethmapbox(
                            name = 'Fog',
                            z= df_griddata['Fog'],
                            locations=df_griddata['ids'],
                            colorscale= [[0, 'rgba(2, 71, 156, 0.0)'], [1.0, 'rgba(250, 250, 250, 0.8)']],
                            # colorscale='purp',
                            colorbar=dict(thickness=20, ticklen=3),
                            geojson= grid20df,
                            # legendgroup="Weather",  # this can be any string, not just "group"
                            # legendgrouptitlet="Weather",
                            showlegend=True,
                            showscale=False,
                            text = df_griddata['Fog'],
                            visible =  "legendonly",
                            hoverinfo='all',
                            marker_line_width=1, 
                            # marker_opacity=0.5
                            )) 

# figGameboard.add_trace(go.Choroplethmapbox(
#                             name = 'Navigability Binary',
#                             z= df_griddata['Navigation Binary'],
#                             locations=df_griddata['ids'],
#                             colorscale= [[0, 'rgb(0, 0, 255)'], [1.0, 'red']],
#                             # colorscale='purp',
#                             colorbar=dict(thickness=20, ticklen=3),
#                             geojson= grid20df,
#                             showlegend=True,
#                             showscale=False,
#                             text = df_griddata['Navigation'],
# #                             text=text,
#                             hoverinfo='all',
#                             marker_line_width=1, 
#                             marker_opacity=0.5)) 

figGameboard.add_trace(go.Choroplethmapbox(
                            name = 'Historical Trafficking Routes',
                            z= df_griddata['Historical Trafficking Routes'],
                            locations=df_griddata['ids'],
                            colorscale=[[0, 'rgba(70,3,159,0.2)'], [0.5, 'rgba(219,92,104,0.5)'], [1.0, 'rgba(241,244,33,0.8)']],
                            colorbar=dict(thickness=20, ticklen=3),
                            geojson= grid20df,
                            # legendgroup="Supplemental Data",  # this can be any string, not just "group"
                            # legendgrouptitle="Supplemental Data",
                            showlegend=True,
                            showscale=False,
                            text = df_griddata['Historical Trafficking Routes'],
                            visible =  "legendonly",
#                             text=text,
                            hoverinfo='all',
                            marker_line_width=1, 
                            # marker_opacity=0.5
                            )) 

figGameboard.add_trace(go.Choroplethmapbox(
                            name = 'AIS',
                            z= df_griddata['AIS'],
                            locations=df_griddata['ids'],
                            colorscale=[[0, 'rgba(192, 131, 252, 0.1)'], [1.0, 'rgba(255, 153, 0, 0.8)']],
                            colorbar=dict(thickness=20, ticklen=3),
                            geojson= grid20df,
                            # legendgroup="Supplemental Data",  # this can be any string, not just "group"
                            # legendgrouptitle="Supplemental Data",
                            showlegend=True,
                            showscale=False,
                            text = df_griddata['AIS'],
                            visible =  "legendonly",
#                             text=text,
                            hoverinfo='all',
                            marker_line_width=1, 
                            # marker_opacity=0.5
                            )) 

# figGameboard.add_trace(go.Scattermapbox(
#     name= 'Nav', 

#     lat= navigation['Latitude'],
#     lon= navigation['Longitude'],
#     mode='markers',
#     marker=go.scattermapbox.Marker(

#         cauto= False, 
#         size=3,

#         color= 'yellow',
#         opacity = 0.8,

        
#     ),

# ))

figGameboard.update_layout(
        # title = 'Gameboard',
    
        template= "plotly_dark",
        height=625,
        # autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            style= "satellite",
            bearing=0,
            center=dict(
                # lat=latm,
                # lon=lonm
                lat=3.5,
                lon=-95
            ),
            pitch=0,
            zoom=3.7
            # zoom=13.529401748965746
        ),
        legend=dict(
            yanchor="bottom",
            y=0.05,
            xanchor="left",
            x=0.01
        ),
            margin= {
                    "b": 5, 
                    "l": 5, 
                    "r": 5, 
                    "t": 5
                }, 
    )

    
# fig2dhist = go.Figure(go.Choroplethmapbox(z=jdatadf['value'],
#                             locations=jdatadf['ids'],
#                             colorscale='reds',
#                             colorbar=dict(thickness=20, ticklen=3),
#                             geojson=jdata,
# #                             text=text,
#                             hoverinfo='all',
#                             marker_line_width=1, marker_opacity=0.75))

                            

# fig2dhist.add_trace(go.Choroplethmapbox(z=dfn['value'],
#                             locations=dfn['ids'],
#                             colorscale='reds',
#                             colorbar=dict(thickness=20, ticklen=3),
#                             geojson=griddf,
# #                             text=text,
#                             hoverinfo='all',
#                             marker_line_width=1, marker_opacity=0.75))       

# fig2dhist.update_layout(title_text= '12mileinfo',
#                   title_x=0.5, width = 700,# height=700,
#                   mapbox = dict(center= dict(lat=8,  lon=-90),
#                                  accesstoken= mapbox_access_token,
#                                  style='basic',
#                                  zoom=2.35,
#                                ))

sliderin = dcc.Slider(
    id='my-range-slider2',
    min=mintime,
    max=maxtime,
    # min=0,
    # max=1765361,
    # step=None,
    # marks={
    #     0: '0',
    #     2000: '2000',
    #     4000: '4000',
    #     6000: '6000',
    #     8000: '8000',
    #     10000: '10000'
    # },
    value=900
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
                    
                    width={"size": 5
                    , 
                    "offset": 1
                    },
            
                ),
                dbc.Col(
                    html.Div( html.H5("Raw Data"
                    , 
                    style={'color': '#339933', 'fontSize': 18}
                    )
                    ),
                    
                    width={"size": 3, 
                    "offset": 2},
                
                )
            ],

            ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        # dcc.Graph( figure= fig ),

                        dcc.Graph( figure = figGameboard),
                        # dbc.Row(
                        #     [
                        #         html.Div([select], style={"width": "50%"}),
                        #         popover,
                        #         html.Div(id='dataselected')
                        #     ]
                        # )

                    ],
                    width = 6
                ),

                dbc.Col(
                    [
                        # html.Div( sliderin ),
                        dcc.Graph( figure= fig ),
                        # dcc.Graph( figure = figGameboard),
                        # dcc.Graph(id='graph-with-slider'),
                        # dbc.Row(
                        #     [
                        #         html.Div([select], style={"width": "50%"}),
                        #         popover,
                        #         html.Div(id='dataselected')
                        #     ]
                        # )

                    ],
                    width = 6
                ),
            ]
            
        ),

        dbc.Row(
            html.Br()
        )
       
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
                                dbc.Col([html.Img(src= app.get_asset_url('CurrentLab2.png'), height="30px")], width = 1),

                                # dbc.Col([dbc.NavbarBrand("Team Salacious Crumb"
                                # # , 
                                # # className="ms-2"
                                # )], width = 4),
                                
                                dbc.Col(
                                            html.Div("Team Salacious Crumb", style={'color': 'Black', 'fontSize': 26}),
                                            width={"size": 4, "offset": 2},
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
                        html.Br(),
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
        # html.Div(id='intermediate-value', style={'display': 'none'})
        ],
    fluid=True

    )
    ],
    style={'backgroundColor': '#2b2b2b'})





########### Run the app
if __name__ == '__main__':
    application.run(debug=True, port=8080)


# if __name__ == '__main__':
#     application.run(debug=True, port=8080)
