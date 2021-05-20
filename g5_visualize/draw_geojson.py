import pandas as pd
import folium
import coordTransform
from folium.plugins import Search
from folium.map import FeatureGroup
import geopandas

alljs = geopandas.read_file(
    'all.json',
    driver='GeoJSON'
)


map_f = folium.Map(location=[23.118766, 113.332907],
                  zoom_start=12,
                  control_scale=True,tiles="http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}",attr='default')

style_function = lambda x: {'Opacity': 1 }

groupA = folium.FeatureGroup(name='有饭票', control=True)
all = folium.FeatureGroup(name='all',show=False,control=False).add_to(map_f)
groupB = folium.FeatureGroup(name='无饭票', control=True)
bankgroup = folium.FeatureGroup(name='网点', control=True)

geo = folium.GeoJson(
    alljs,
    name='All',style_function=style_function,
    # tooltip=folium.GeoJsonTooltip(
    #     fields=['name'],
    #     localize=True,
    # ),
    overlay=True,
    show=False,
    # control=False
).add_to(all)


bank=pd.read_excel('广州分行网点清单.xlsx')
xls = pd.ExcelFile('g5canteen.xlsx')
df1 = pd.read_excel(xls, '有饭票')
df2 = pd.read_excel(xls, '无饭票')



for i,r in bank.iterrows():
    lon,lat= coordTransform.bd09_to_gcj02(r['lon'], r['lat'])
    folium.Marker([lat, lon], tooltip=r['Name'], icon=folium.DivIcon(icon_size=(80, 72), icon_anchor=(0, 0),
                                                                            html='<div style="font-size: 12px;color: blue; background: white;">' + f"{r['Name']}" + '</div>')
                  ).add_to(bankgroup)
    folium.Marker([lat,lon ],tooltip=r['Name'], icon=folium.Icon( icon='credit-card', prefix='fa')).add_to(bankgroup)


for i,r in df1.iterrows():
    lon, lat = coordTransform.bd09_to_gcj02(r['lon'], r['lat'])
    folium.Marker([lat,lon ], tooltip=r['Name'],icon=folium.DivIcon(icon_size=(100,72),icon_anchor=(0,0),html='<div style="font-size: 12px;color: red; background: white;">'+f"{r['Name']}"+'</div>')
).add_to(groupA) #,icon=folium.Icon(color='red', icon='cutlery')icon=folium.Icon(color='red', icon='cutlery'),icon=DivIcon(icon_size=(150,36),icon_anchor=(0,0),html='<div style="font-size: 24pt">Test</div>')
    folium.Marker([lat, lon], tooltip=r['Name'], icon=folium.Icon(color='red', icon='cutlery')
                  ).add_to(groupA)

for i,r in df2.iterrows():
    lon, lat = coordTransform.bd09_to_gcj02(r['lon'], r['lat'])
    folium.Marker([lat,lon ], tooltip=r['Name'],icon=folium.DivIcon(icon_size=(100,72),icon_anchor=(0,0),html='<div style="font-size: 12px;color: organe; background: white;">'+f"{r['Name']}"+'</div>')
).add_to(groupB) #,icon=folium.Icon(color='red', icon='cutlery')icon=folium.Icon(color='red', icon='cutlery'),icon=DivIcon(icon_size=(150,36),icon_anchor=(0,0),html='<div style="font-size: 24pt">Test</div>')
    folium.Marker([lat, lon], tooltip=r['Name'], icon=folium.Icon(color='gray', icon='cutlery')
                  ).add_to(groupB)


citysearch = Search(
    layer=geo,
    geom_type='Point',
    placeholder='Search',
    search_zoom=16,
    collapsed=True,
    search_label='name'
).add_to(map_f)
#
map_f.add_child(groupA)
map_f.add_child(groupB)
map_f.add_child(bankgroup)
# map_f.add_child(all)
folium.LayerControl().add_to(map_f)
map_f.save('bank_g5_with_search.html')