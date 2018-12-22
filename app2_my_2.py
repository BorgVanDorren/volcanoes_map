import folium as fl
import pandas as pd

# Initialization - data import and initial map creation
my_map = fl.Map(location=[65.089959, 134.153830], zoom_start=4)
vol_df = pd.read_csv('volcanoes_rus_clear.csv')

# World active volcanoes list import and data prep to same format
# NB: All records with errors were dropped
vol_df_a = pd.read_csv('volcanoes_world_active.csv')
vol_df_a = vol_df_a.drop(['Country', 'Type'], 1)
vol_df_a.columns = ['name', 'lat', 'lon', 'height']
vol_df_a['lat'] = pd.to_numeric(vol_df_a['lat'], errors = 'coerse')
vol_df_a['lon'] = pd.to_numeric(vol_df_a['lon'], errors = 'coerse')
vol_df_a = vol_df_a.dropna()

# Replaced by interrows iteration over DataFrame
# lat = list(vol_df['lat'])
# lon = list(vol_df['lon'])
# name = list(vol_df['name'])
# elev = list(vol_df['height'])

html = """<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""


def color_selector(el):

    """ Select color of the marker depending on height"""

    if el < 1000:
        return 'green'
    elif 1000 < el < 2500:
        return 'orange'
    else:
        return 'red'

# Forming group of markers
fgv = fl.FeatureGroup(name='Volcanoes')
fga = fl.FeatureGroup(name='Active')

for i, row in vol_df.iterrows():

    iframe = fl.IFrame(html=html % (row['name'], row['name'], row['height']), width=150, height=80)
    fgv.add_child(fl.CircleMarker(location=[row['lat'], row['lon']], popup=fl.Popup(iframe),
                                  color=color_selector(row['height']), radius=6, weight=1,
                                  fill=True, fill_opacity=0.8))

for i, row in vol_df_a.iterrows():

    iframe = fl.IFrame(html=html % (row['name'], row['name'], row['height']), width=150, height=80)
    fga.add_child(fl.Marker(location=[row['lat'], row['lon']], popup=fl.Popup(iframe), icon=fl.Icon(color=color_selector(row['height']))))


# Adding group to the map and saving the map
my_map.add_child(fgv)
my_map.add_child(fga)
my_map.save('Map4.html')
