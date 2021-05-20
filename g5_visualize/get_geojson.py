import pandas as pd
import folium
import coordTransform
from folium.plugins import Search
# import geopandas
from folium.map import FeatureGroup
import json

bank=pd.read_excel('广州分行网点清单.xlsx')
bank=bank[['Name','lon','lat','Place']]
xls = pd.ExcelFile('g5canteen.xlsx')
df1 = pd.read_excel(xls, '有饭票')
df2 = pd.read_excel(xls, '无饭票')

df =pd.concat([bank,df1,df2])

def df_to_geojson(df,name='网点名称'):
    geojson = {'type':'FeatureCollection', 'features':[]}

    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'properties':{'name':row[name]},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}
        lon, lat = coordTransform.bd09_to_gcj02(row['lon'], row['lat'])
        feature['geometry']['coordinates'] = [lon,lat]
        # for prop in properties:
        #     feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson

geojson = df_to_geojson(df,'Name')
output_filename = 'all.json'
with open(output_filename, 'w') as output_file:
    # output_file.write('var dataset = ')
    json.dump(geojson, output_file, indent=2)

# banks = geopandas.read_file(
#     'bank.json',
#     driver='GeoJSON'
# )