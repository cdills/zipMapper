import folium
import pandas as pd
import os

#init variablaes
geoDir =  './resources/geojson/'
geoDirSimple = './resources/simple/'
doSimple = True
csvZipsToDraw = './resources/zipsToDraw.csv'
#state_geo="./resources/geojson/nc.geojson"

df = pd.read_csv(csvZipsToDraw, na_values=[''])
df.set_index('index', inplace=True)
#m = folium.Map(location=[35.8, -78.64], tiles = 'Mapbox Bright', prefer_canvas=True, zoom_start=8)



def parseGeoJson(directory, map):
    files = os.listdir(directory)

    for file in files:
        geoJson = directory + file
        folium.GeoJson(
            geoJson,
            name='geojson',
            style_function=style_function
        ).add_to(map)


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

def drawMap():
    m = folium.Map(location=[35.8, -78.64], tiles='Mapbox Bright', prefer_canvas=True, zoom_start=8)
    parseGeoJson(geoDir, m)
    m.save('map.html')

    if doSimple:
        s = folium.Map(location=[35.8, -78.64], tiles='Mapbox Bright', prefer_canvas=True, zoom_start=8)
        parseGeoJson(geoDirSimple, s)
        s.save('mapSimple.html')

drawMap()