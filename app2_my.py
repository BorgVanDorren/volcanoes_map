import folium as fl
import pandas as pd

# Initialization - data import and initial map creation
my_map = fl.Map(location=[65.089959, 134.153830], zoom_start=4)
vol_df = pd.read_csv('volcanoes_rus_clear.csv')

lat = list(vol_df['lat'])
lon = list(vol_df['lon'])
name = list(vol_df['name'])
elev = list(vol_df['height'])

html = """<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def color_selector (el):
    """ Select color of the marker depending on height"""

    if el < 1000:
        return 'green'
    elif 1000 < el < 2500:
        return 'orange'
    else:
        return 'red'

# Forming group of markers
fgv = fl.FeatureGroup(name="Volcanoes")

for n, lt, ln, el in zip(name, lat, lon, elev):

    iframe = fl.IFrame(html=html % (n, n, el), width=150, height=80)
    fgv.add_child(fl.Marker(location=[lt, ln], popup=fl.Popup(iframe), icon=fl.Icon(color=color_selector(el))))

# Adding group to the map and saving the map
my_map.add_child(fgv)
my_map.save('Map1.html')
