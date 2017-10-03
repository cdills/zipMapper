import folium
import pandas as pd


state_geo="./resources/geojson/nc.geojson"
m = folium.Map(location=[35.7, -81.21])


df = pd.read_csv("./resources/zipsToDraw.csv", na_values=[''])
df.set_index('index', inplace=True)

def style_function(feature):
    properties = feature['properties']
    featureZip= properties['ZCTA5CE10']
    zip = df.values

    if str(featureZip) in str(zip):
      return {
        'fillOpacity': 1.00,
           'weight': 1,
          'fillColor': '#black'
      }
    else:
        return {
        'fillOpacity': 0.0,
        'weight': 0,
        'fillColor': '#red'
        }

folium.GeoJson(
    state_geo,
    name='geojson',
    style_function=style_function
).add_to(m)

m.save('map.html')