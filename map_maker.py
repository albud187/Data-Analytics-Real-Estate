import folium
import pandas

data = pandas.read_csv(r'E:\python\_projects\kijiji real estate webscraper\output3.csv')
lat = list(data["Latitude"])
long = list(data["Longitude"])
price = list(data["Price"])
address = list(data["Raw Address"])
MLS = list(data["MLS #"])

map = folium.Map(location = [45.3, -75.7], zoom_start=10, titles = "Mapbox Bright")

fg = folium.FeatureGroup(name = "My Map")



for lt, ln, pr, ad, ML in zip(lat, long, price, address, MLS):
    fg.add_child(folium.CircleMarker(location=[lt, ln], popup=str(pr)+', '+str(ad)+', '+str(ML),
            fill_color = 'green', color = 'grey', fill_opacity = 0.7)) 




map.add_child(fg)
map.save(r'E:\python\_projects\kijiji real estate webscraper\realmap3.html')
