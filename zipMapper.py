import folium
import pandas as pd

state_geo="./resources/geojson/nc.geojson"
m = folium.Map(location=[35.8, -78.64], tiles = 'Mapbox Bright', prefer_canvas=True, zoom_start=8)

df = pd.read_csv("./resources/zipsToDraw.csv", na_values=[''])
df.set_index('index', inplace=True)

def style_function(feature):
    properties = feature['properties']
    featureZip= properties['ZCTA5CE10']
    zip = df.values

    if str(featureZip) in str(zip):
      return {
        'fillOpacity': .5,
           'weight': 0.4,
          'fillColor': 'red'
      }
    else:
        return {
        'fillOpacity': 0.0,
        'weight': 0,
        'fillColor': ''
        }

folium.GeoJson(
    state_geo,
    name='geojson',
    style_function=style_function
).add_to(m)

m.save('map.html')