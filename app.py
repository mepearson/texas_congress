# ----------------------------------------------------------------------------
# Python Libraries
# ----------------------------------------------------------------------------

import os
import pathlib
import json

import pandas as pd
import geopandas as gpd

import plotly.express as px

import dash_bootstrap_components as dbc
from dash import Dash, callback, clientside_callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate

# ----------------------------------------------------------------------------
# DATA Loading
# ----------------------------------------------------------------------------

data_filepath = pathlib.Path(__file__).parent.absolute()

## TEXAS CONGRESSIONAL DISTRICT MAP
texas_geojson_file = os.path.join(data_filepath,'data','texas_congress.geojson')
texas = gpd.read_file(texas_geojson_file)

# links to district Files
district_files_filepath = os.path.join(data_filepath,'data','district_files.csv')
district_files = pd.read_csv(district_files_filepath)
# add column with link formatted for markdown
district_files['File'] ='[' + district_files['description'] + '](' + district_files['district_map_url'] + ')'

## Create link to district map
district_map_link_prefix = 'https://wrm.capitol.texas.gov/fyiwebdocs/PDF/congress/dist' # replace {district_number} with selected district
district_map_link_suffix = '/m1.pdf'

# ----------------------------------------------------------------------------
# DATA Visualizations
# ----------------------------------------------------------------------------
texas_center_lat = 31.3 #31.9686
texas_center_lon = -99.9018

map_fig = px.choropleth_mapbox(
    texas,
    geojson = texas.geometry,
    locations = texas.index,
    custom_data = [texas['CD116FP'], texas['NAMELSAD']], # pull in additional columns to use in UI, ex: on Hover
    mapbox_style = "open-street-map",
    zoom = 5,
    center = {
        "lat" : texas_center_lat,
        "lon" : texas_center_lon
    },
    opacity = 0.8,
)

map_fig.update_layout(
    margin = {
        "r" : 0,
        "t" : 0,
        "l" : 0,
        "b" : 0
    },
    clickmode = 'event',
    height = 600,
    showlegend=False
)

map_fig.update_traces(
    hovertemplate="<br>".join([
        "%{customdata[1]}"
    ])
)

# ----------------------------------------------------------------------------
# APP Layout
# ----------------------------------------------------------------------------

external_stylesheets = [dbc.themes.LITERA]

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dbc.Row([
        html.H2('Texas Congressional District Information'),
        ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='graph-map',
                figure=map_fig,

            ),
        ],width=4),
        dbc.Col([
            html.Div(id='div-map-select'),
            html.Div('Maps from https://redistricting.capitol.texas.gov/')
        ],width=8),
    ]),
    dbc.Row([
        dbc.Col([            
            html.Div(id='div-files'),
        ])
    ])
])


# ----------------------------------------------------------------------------
# CALLBACKS
# ----------------------------------------------------------------------------

@callback(
    Output('div-map-select', 'children'),
    Output('div-files','children'),
    Input('graph-map', 'clickData'))
def update_figure(clickData):
    # Data for table of files
    table_data_cols = ['Congress','State','District', 'File']
    table_data = district_files[table_data_cols]

    if clickData is None:
        div_map = html.P('Select a Congressional district from the map at left to load the District Map')


    # If District selected in map, display specialty map and filter files list
    else:
        # get value of district selected
        cd = clickData['points'][0]['customdata'][0]
        if cd[0] == '0': # remove leading 0
            cd = cd[1:]
        # get link to District map for selected district
        cd_link = ''.join([district_map_link_prefix,cd,district_map_link_suffix])
        div_map = html.Embed(src=cd_link,width="600",height="600",type="application/pdf")
        # filter files table to district
        table_data = table_data[table_data['District']==int(cd)]

    div_files = dash_table.DataTable(
        id='table-files',
        style_data={'whiteSpace': 'normal',
                    'height':'auto'},
        style_table={'overflowX': 'scroll',
                     'textOverflow':'ellipsis',
                      'maxHeight': '800px',
                      'paddingTop': '2px'
                      },
        data=table_data.to_dict('records'),
        columns= [{'name':i, 'id':i,'type':'text','presentation':'markdown'} for i in table_data_cols],
        # filter_action = 'native',
        sort_action = 'native',
        sort_mode = 'multi',
        fixed_rows = {'headers':True}
    )


    return div_map, div_files

# ----------------------------------------------------------------------------
# RUN APP
# ----------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
else:
    server = app.server
