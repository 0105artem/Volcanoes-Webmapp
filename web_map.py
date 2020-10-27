#! python3
# web_map.py - is a web map made with pandas and folium. It has 3 layers. 
# First one is a simple map. The second represents volcanoes of USA.
# And third is a polygon layer which represents the population of the countries.
  
import folium
import pandas


df = pandas.read_csv('Volcanoes.txt')
lat = df['LAT']
lon = df['LON']
location = df['LOCATION']
elev = list(df['ELEV'])

def color_producer(elevation):
    if elevation <= 1000:
        return 'green'
    elif elevation < 2500:
        return 'orange'
    else:
        return 'red'

map = folium.Map(location=[35.369999, -111.501000], zoom_start=6, tiles="Stamen Terrain")

fgv = folium.FeatureGroup(name="Volcanoes")
fgp = folium.FeatureGroup(name="Population")

for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=str(el)+' m', 
    radius=8, fill_opacity=0.6, fill_color=color_producer(el), color='grey'))

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), 
style_function=lambda x: {'fillColor':'yellow' if x['properties']['POP2005'] < 10000000 
else 'orange' if x['properties']['POP2005'] < 100000000 else 'red' }))

map.add_child(fgv)
map.add_child(fgp)

map.add_child(folium.LayerControl())

map.save('main.html')