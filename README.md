#zipMapper

Easily plot and shade US Zip Code regions.

BUT WAIT

Now includes simplified zip regions and county mapping


### Prerequisites

pip install folium
pip install pandas


Download US Zip Code shape files from [US Census Site](https://www.census.gov/cgi-bin/geo/shapefiles/index.php) by selecting '2010' and 'Zip tabulation areas'
Convert .zip shapfile to geojson here: [MapShaper](http://mapshaper.org/)
Drop .json file into /resources/geojson


Place .csv list of zip codes you wish to import into root directory



### Using

 Run script after following prerequisites. Result is 'map.html' in root directory. 

## Built With

* [Folium](https://github.com/python-visualization/folium)
* [Pandas](http://pandas.pydata.org)


