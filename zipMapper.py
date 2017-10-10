import folium
import pandas as pd
import os
import pyodbc
import configparser


Config = configparser.ConfigParser()
Config.read(".\config.ini")

dbMode = Config.getboolean('mode', 'dbmode')


if dbMode:
    dbCounties = []
    dbZip = []
    driver = Config.get('db', 'driver')
    server = Config.get('db', 'server')
    database = Config.get('db', 'database')
    uid = Config.get('db', 'uid')
    pwd = Config.get('db', 'pwd')
    con = pyodbc.connect(driver=driver, server=server, database=database, uid=uid, pwd=pwd)
    cur = con.cursor()
    db_cmd = Config.get('db', 'cmd')
    cur = cur.execute(db_cmd)

    for r in cur:
        dbCounties.append(r[1])
        dbZip.append(r[2])
else:
    csvZipsToDraw = Config.get('files', 'csvZipsToDraw')
    countiesToDraw = Config.get('files', 'countiesToDraw')

    df = pd.read_csv(csvZipsToDraw, na_values=[''])
    df.set_index('index', inplace=True)
    dfC = pd.read_csv(countiesToDraw, na_values=[''])

doCounty = Config.getboolean('styles', 'doCounty')
doSimple = Config.getboolean('styles', 'doSimple')
doZip = Config.getboolean('styles', 'doZip')

if doCounty:
    geoDirCounty = Config.get('files', 'geoDirCounty')
if doSimple:
    geoDirSimple = Config.get('files', 'geoDirSimple')
if doZip:
    geoDir = Config.get('files', 'geoDir')
if not doCounty and not doSimple and not doZip:
    exit("no style selected")



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
    if dbMode:
        zip = dbZip
    else:
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
    if dbMode:
        counties = dbCounties
    else:
        counties = dfC['County'].tolist()

    properties = feature['properties']
    featureCounty= properties['NAME10']
    stateFP= properties['STATEFP10']

    checkFeature = str(featureCounty) + ' ' + stateFP


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