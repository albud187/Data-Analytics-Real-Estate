import requests
from bs4 import BeautifulSoup
import pandas
from geopy.geocoders import Nominatim
import random

def address_fix1(address):

    if 'UNIT' in address: 
        street=''
        for i in range(len(address)):
            street += address[i]
            if address[i:i+4] == 'UNIT':
                break 
    
        return(street[0:i-1])
    else:
        return(address.replace("#",' ').replace("|"," "))
    
def province(address):
    if 'ONTARIO' in address:
        return('ONTARIO')
    elif 'QUEBEC' in address:
        return('QUEBEC')

def address_fix2(address):
    if 'UNIT' in address:
        return(address_fix1(address)+', ' +province(address))
    else:
        return(address_fix1(address))

def rand_user_agent():
    agents = ['Del Lor', 'Kary Ayars', 'Harriette Schluter', 'Cassondra Carley', 'Hyman Bulkley', 'Noe Lorence', 'Janie Jernigan', 'Margaretta Janson', 'Petrina Utter', 'Barney Beckwith', 'Casandra Weyandt', 'Arleen Sneed', 'Joye Pfeifer', 'Charles Keplin', 'Isabelle Perla', 'Tarah Bradstreet', 'Kerstin Stocks', 'Tarra Wiren', 'Nena Pergande', 'Merry Dionisio', 'Bernetta Hallberg', 'Amina Babb', 'Ernesto Foster', 'Jolene Melgarejo', 'Peggie Lanham', 'Vallie Balsamo', 'Barbera Berlanga', 'Siobhan Hasbrouck', 'Eleonore Wisener', 'Ellen Scoggins', 'Deja Deloney', 'Cristina Poulin', 'Delicia Creasman', 'Tamiko Dam', 'Ryan Poffenberger', 'Tonia Simmerman', 'Jannie Ver', 'Genie Goodsell', 'Rachal Riddell', 'Gilda Pemberton', 'Analisa Temples', 'Melisa Windham', 'Roseanne Fallis', 'Olive Vanalstyne', 'Nia Hipsher', 'Michaela Chuang', 'Antonina Trees', 'Librada Vogus', 'Shantay Burts', 'Vern Cann']
    return agents[random.randint(0,len(agents))]

def address_lat(address):
    geolocator = Nominatim(user_agent = rand_user_agent())
    location = geolocator.geocode(address)
    return(location.latitude)

def address_long(address):
    geolocator = Nominatim(user_agent = rand_user_agent())
    location = geolocator.geocode(address)
    return(location.longitude)

base_url1 = "https://www.kijiji.ca/b-for-sale/ottawa/mls/page-"
base_url2 = "/k0c30353001l1700185r20.0?price=75000__200000"
last_page = 5

list =[]
print('URLs scraped:')
for pg in range(1,last_page):
    url = base_url1 + str(pg)+base_url2
    print(url)
    r = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/2010001 Firefox/61.0'})
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    all = soup.find_all("div", {"class":"info-container"})

 
    for item in all:
        d={}
        d["Raw Address"] = item.find("div",{"class":"title"}).text.replace("\n","").replace("   ","").upper()
        d["Address"] = address_fix2(item.find("div",{"class":"title"}).text.replace("\n","").replace("   ","").upper())
        try:
            d["Latitude"] = address_lat(address_fix2(item.find("div",{"class":"title"}).text.replace("\n","").replace("   ","").upper()))
        except:
            d["Latitude"] =1.1111
        try:
            d["Longitude"] = address_long(address_fix2(item.find("div",{"class":"title"}).text.replace("\n","").replace("   ","").upper()))
        except:
            d["Longitude"] = 1.1111
        d["Price"] = item.find("div",{"class":"price"}).text.replace("\n","").replace(" ","")
        d["MLS #"] = item.find("div",{"class":"description"}).text.replace("\n","").replace("    ","")[5:14]
        list.append(d)


    df = pandas.DataFrame(list)
    
    print('Done Scraping')

# turns the df into a .csv file
df.to_csv(r'E:\python\_projects\kijiji real estate webscraper\output4.csv')
