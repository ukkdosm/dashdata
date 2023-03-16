# To update, run: python.exe -m pip install --upgrade pip
# !pip install streamlit geopandas pandas_geojson folium numpy panel pandas matplotlib jupyter_bokeh==3.0.5
# pip install bokeh==2.4.0
# Compress function
/home/appuser/venv/bin/python -m pip install --upgrade pip
import folium as fm
from folium import plugins
from pandas_geojson import read_geojson, filter_geojson
import numpy as np
import panel as pn
pn.extension(sizing_mode="stretch_width")
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import json
import urllib.request

def create_app2(sociodemo, geo_json, select):
    selectv = select.value
    filter = [selectv]
    selectgeo = filter_geojson(geo_json=geo_json, filter_list=filter, property_key='dun')

    # create map object
    map = fm.Map(location=[5.016806622688496, 107.9456777002687], tiles='cartodbpositron', zoom_start=6)

    # add tool measure to the top right
    # from folium.plugins import MeasureControl
    # map.add_child(MeasureControl())

    # add geojson to map
    fm.GeoJson(selectgeo, name='DUN boundary', tooltip=fm.GeoJsonTooltip(fields=['dun', 'parlimen'])).add_to(map)
    map.fit_bounds(map.get_bounds(), padding=(30, 30))
    folium_map = pn.panel(map, height=400)

    # select data based on selected value
    select_sociodemo = sociodemo[sociodemo['dun'] == selectv]

    # round watercover to 3 decimal places
    select_sociodemo['watercover'] = np.round(select_sociodemo.watercover, decimals=3)

    # get max_elevation, watercover and population_total
    max_elev = select_sociodemo['max_elevation'].iloc[0]
    water = select_sociodemo['watercover'].iloc[0]
    pop = select_sociodemo['population_total'].iloc[0]

    # create indicators
    number = pn.indicators.Number(format='{value}')

    indicator = pn.Row(
        number.clone(name='Population', value=pop, colors=[(33, 'black')]),
        number.clone(name='Maximum Elevation', value=max_elev, colors=[(66, 'blue')]),
        number.clone(name='Surface covered in water', value=water, colors=[(100, 'red')]),
        sizing_mode='stretch_width')

    # create description
    description = select_sociodemo['dun'].iloc[0]
    str_pane = pn.indicators.Number(name=str(description))

    # create panel object
    app2 = pn.Column(
        pn.Column(
            str_pane,
            indicator,
            folium_map,
            sizing_mode='scale_both'
        ),
        sizing_mode='scale_both'
    )

    return app2

'''Select option'''
url = 'https://raw.githubusercontent.com/dosm-malaysia/data-open/main/datasets/geodata/electoral_1_dun.geojson'

geo_json = json.load(urllib.request.urlopen(url))

duns = gpd.read_file(url)

sociodemo = pd.read_csv('https://github.com/booluckgmie/podac/raw/main/sociodemo.csv')

#READ DATAFRAME
from pandas_geojson import read_geojson, filter_geojson
filter = ['Pulau Pinang']
select = filter_geojson(geo_json=geo_json, filter_list=filter, property_key='state')
duns_pp = duns[duns['state'].isin(filter)].reset_index(drop=True)
select_options = duns_pp['dun'].values.tolist()

#CREATE SELECTION
select = pn.widgets.Select(name='Select DUN', options=select_options)
select

'''Run apps deploy'''
app2 = create_app2(sociodemo, geo_json, select)
app2
