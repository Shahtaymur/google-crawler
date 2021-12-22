import requests
import json
import pandas as pd
import config
from random import choice
from requests_html import HTMLSession



keyword = [
    'apple','samsung','motorola','sony','top sights in ireland','how to cook buckwheat','define love','imaran khan','what is node js','node js','how to run python code','best games in 2021','upcoming movies','how many ounces in a gallon',
'LED Submersible Lights',
'Portable Projector',
'Bluetooth Speaker',
'Smart Watch',
'Temporary Tattoos',
'Bookends',
'Neck Massager',
'Facial Cleanser',
'Vegetable Chopper',
'Back Cushion',
'Portable Blender',
'Nail Polish',
'Wireless Phone Chargers',
'Phone Lenses',
'Shapewear',
'Strapless Backless Bra',
'Doormats',
'Car Phone Holder',
'Home Security IP Camera',
'Wifi Repeater',
'Laptop Accessories',
'Posture Corrector',
'Electric Soldering Iron Gun',
'Manicure Milling Drill Bit',
'Flexible Garden Hose',
'One Piece Swimsuit',
'Waterproof Eyebrow Liner',
'Cat Massage Comb',
'Breathable Mesh Running Shoes – Summer Product',
'Portable Electric Ionic Hairbrush – Summer Product',
'Beach Towels – Summer Product',
'Baby Kids Water Play Mat – Summer Product',
'Plush Blankets – Winter Product',
'Winter Coats – Winter Product',
'Shoe Dryer – Winter Product',
'Touchscreen Gloves – Winter Product',
'Waterproof Pants – Winter Product',
'Bear Claws – Spring Products',
'Hiking Backpacks – Spring Products',
'Minimalist Wallets – Spring Products',
'Waterproof Shoe Cover – Autumn (Fall) Product',
'Hooded Raincoats – Autumn (Fall) Product',
'Laser Hair Removal Machines',
'Portable Car Vacuum',
'Baby Swings',
'Matcha Tea',
'Eyebrow Razor',
'Seat Cushions',
'Phone Tripod',
'Portable Solar Panels',
'Automobiles Accessories',
'Baby Care Products',
'Beauty & Healthcare Products',
'Computer & Office Products',
'Home & Gardening',
'Kitchen & Dining Items',
'Mother & Kids',
'Pet Products',
'Wearable Devices',
'Security & Protection',
'Hair accessories',
'Beauty and healthcare products',
'Pet products',
'Hi-tech products & accessories',
'Fashion items',
'Sport & traveling products',
'Car products',
'Fine jewelry'
 'Hair Wig',
 'Headscarf',
 'Magnetic eyelashes',
 'Nail extensions',
 'Green Powder',
 'Car phone holder',
 'Wireless charger',
 'Phone cases',
 'Wearable devices',
 'Pet food',
 'Pet bathing tool',
 'Pet carrier',
 'Neon clothes',
 'Collared clothes',
 'Bra-top craze',
 'Shapewear',
 'Sport bottle',
 'Luggage suitcase',
 'Mesh shoes',
'Rear cameras',
'Car led light',
'Car covers',
'Second-hand jewelry',
'Layering',
'Stackable rings']


df_list = pd.read_html('list.html')

for i, df in enumerate(df_list):
    for game in df.Game:
        keyword.append(game)
        print(game)
    for genere in df.Genre:
        keyword.append(genere)
        print(genere)
    for publisher in df.Publisher:
        keyword.append(publisher)
        print(publisher)

orignal = []
for key in keyword:
    if not key in orignal:
        orignal.append(key)

# for key in orignal:
#     count = 1
#     # try:
#     #     r = requests.get('http://127.0.0.1:5000/search?q=')
#     #     count = count + 1
#     # except requests.exceptions.RequestException as e:
#     #     print (e.args[0].reason)
#     #     print(e.request.headers)
#     r = requests.get('http://127.0.0.1:5000/search?q={}'.format(key))
#     data = json.loads(r.content)
#     data = r.content
#     print(data)
#     print(key)

from bs4 import BeautifulSoup
import requests, lxml
import re

headers = {
    'User-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
}

params = {
  'q': 'how to code',
  'gl': 'us',
  'hl': 'en',
}

html = requests.get('https://www.google.com/search', headers=headers, params=params)
soup = BeautifulSoup(html.text, 'lxml')
try:
    with open(f"html/{re.sub('[^A-Za-z0-9]+', '', params['q'])}.html", "w") as file:
        file.write(html.text)
except:
    pass
results = soup.find_all('div','tF2Cxc')
for result in soup.select('.tF2Cxc'):
  title = result.select_one('.DKV0Md').text
  link = result.select_one('.yuRUbf a')['href']
  print(title, link, sep='\n')

#Street Fighter IV
#Gears of War 2
#Rock Band
#Halo 3
#Overwatch
#The Legend of Zelda: Breath of the Wild
#Inside
#Destiny
#The Last of Us
#Grand Theft Auto V
#Dota 2
#Hotline Miami
#Journey
#Dishonored
#Super Mario Galaxy 2
#Action
#Apogee Software
#Automobiles Accessories
#Baby Care Products
#Space Invaders
#Zork
#Galaga
#Tempest
#Frogger
#Mike Tyson's Punch-Out!!
#Double Dragon
#Mega Man 2
#Prince of Persia
#SimCity
#Wolfenstein 3D
#Myst
#NBA Jam
#SimCity 2000
#X-COM: UFO Defense
#Wipeout
#Tekken 3
#Star Wars Jedi Knight: Dark Forces II
#Rock Band
#Halo 3
#Gears of War 2
#Turn-based strategy
#Civilization
#NBA Jam