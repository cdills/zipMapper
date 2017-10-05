import folium
import pandas as pd
import os

doCounty = True
doSimple = True
doZip = True


geoDir =  './resources/geojson/'
geoDirSimple = './resources/simple/'
geoDirCounty = './resources/county/'
csvZipsToDraw = './resources/zipsToDraw.csv'
countiesToDraw = './resources/countiesToDraw.csv'


df = pd.read_csv(csvZipsToDraw, na_values=[''])
df.set_index('index', inplace=True)
dfC = pd.read_csv(countiesToDraw, na_values=[''])




def parseGeoJson(directory, map, style):
    global file, stateTag
    files = os.listdir(directory)

    if style == "county":
        for file in files:
            geoJson = directory + file
            folium.GeoJson(
                geoJson,
                name='geojson',
                style_function=style_functionCounty
            ).add_to(map)

    if (style == "zip" ) or (style == "simple"):
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

def style_functionCounty(feature):
    counties = dfC['County'].tolist()
    properties = feature['properties']
    featureCounty= properties['NAME10']
    stateFP= properties['STATEFP10']

    def iterateCSV():
        for item in counties:

            if str(checkFeature) == item:

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

    if stateFP == "51":
        stateTag = "VA"
        checkFeature = str(featureCounty) + ' ' + stateTag
        style = iterateCSV()
        return style
    if stateFP == "45":
        stateTag = "SC"
        checkFeature = str(featureCounty) + ' ' + stateTag
        style = iterateCSV()
        return style
    if stateFP == "37":
        stateTag = "NC"
        checkFeature = str(featureCounty) + ' ' + stateTag
        style = iterateCSV()
        return style

def drawMap():
    if doZip:
        m = folium.Map(location=[35.8, -78.64], tiles='Mapbox Bright', prefer_canvas=True, zoom_start=8)
        parseGeoJson(geoDir, m, 'zip')
        m.save('map.html')

    if doSimple:
        s = folium.Map(location=[35.8, -78.64], tiles='Mapbox Bright', prefer_canvas=True, zoom_start=8)
        parseGeoJson(geoDirSimple, s, 'simple')
        s.save('mapSimple.html')

    if doCounty:
        c = folium.Map(location=[35.8, -78.64], tiles='Mapbox Bright', prefer_canvas=True, zoom_start=8)
        parseGeoJson(geoDirCounty, c, 'county')
        c.save('mapCounty.html')


drawMap()