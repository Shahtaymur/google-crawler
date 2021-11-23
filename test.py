import requests
import json
import pandas as pd
import config
from random import choice



keyword = [
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
'apple','samsung','motorola','sony','love','imaran khan','what is node js','node js','how to run python code','best games in 2021','upcoming movies',
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

DEFAULT_HEADERS = {}

for key in orignal:
    proxy = {"http":"http://{}:{}@{}".format(config.PROXY_USER, config.PROXY_PASS, choice(config.GEONODS))
    ,"https":"http://{}:{}@{}".format(config.PROXY_USER, config.PROXY_PASS, choice(config.GEONODS))}
    url = "https://www.google.com/complete/search?q={}&cp=0&client=desktop-gws-wiz-on-focus-serp&xssi=t&hl=en&authuser=0&pq={}&psi=EOObYbuVBv7RwbkPp5GjuA8.1637606159767&ofp=GKba186mw7Wf4AEYr73hkcP9xNiaARi5ioGOrJy9sJsBGL62qeeTiouCIBjgzqntjrXy4-MBEAEy2wEKEgoQaG90IHdhdGVyIGhlYXRlcgoUChJob3Qgd2F0ZXIgYmVuZWZpdHMKFAoSZHJpbmtpbmcgaG90IHdhdGVyChMKEWhvdCB3YXRlciBmYXN0aW5nChsKGWhvdCB3YXRlciBmb3Igd2VpZ2h0IGxvc3MKJAoic2lkZSBlZmZlY3RzIG9mIGRyaW5raW5nIGhvdCB3YXRlcgoYChZob3Qgd2F0ZXIgY29uc3RpcGF0aW9uCiUKI2VmZmVjdHMgb2YgZHJpbmtpbmcgaG90IHdhdGVyIGRhaWx5EEc&dpr=1".format(key,key)
    DEFAULT_HEADERS['user-agent'] = choice(config.USER_AGENTS)
    #DEFAULT_HEADERS['cookies'] = "SEARCH_SAMESITE=CgQI25MB; OGPC=19026101-2:; SID=EAgP3tEXOtOaSeoXycdVMciv9FUqlYdgXPWz0qqxK4MWvmR8PPiLW389m26SadHo7_HZEQ.; _Secure-1PSID=EAgP3tEXOtOaSeoXycdVMciv9FUqlYdgXPWz0qqxK4MWvmR8xJxM-bDwdr26-EzseXxqLA.; _Secure-3PSID=EAgP3tEXOtOaSeoXycdVMciv9FUqlYdgXPWz0qqxK4MWvmR8tj08c5OAaN-HNwszNKcFMQ.; HSID=AxKzEQFz-nv91SdE6; SSID=An5q4xrrnwrr3g2Yw; APISID=o8ebvsowWXWjMA2S/AmU4U2f3nhy8CBGio; SAPISID=HCq4QTkD5PKznhJU/AVtTPSW71KXxzQMOD; _Secure-1PAPISID=HCq4QTkD5PKznhJU/AVtTPSW71KXxzQMOD; _Secure-3PAPISID=HCq4QTkD5PKznhJU/AVtTPSW71KXxzQMOD; 1P_JAR=2021-11-22-17; NID=511=kY3depByVCOb_F1STvyVAsFXGjar4LKinDfspwcWQ-AHQzCsq1L6syDoWAzcugLMQutNvZBU7yhw08H067Mrqb9JPfkvjZMx6m7fPU3XZZd7zNmuFzSKyX9Elv58Dc0rFdR0fG-1_pWDZ5IhzARhz3-LXG0vO0iHZzn-UdnGvohUYx5ijm5Gf5THAWb-Jx24kmuv5ilCAhGX-UP6Chqsx8PzBYETobuMFQZt9QnQPlmFJsBhBZRmNt4; SIDCC=AJi4QfH6_DusZbre6f67hmJ04dzCuiqIn08cGsZa4jZkSGcqIx-iVVRwP2rYhPU_u2iRF4vIZg; __Secure-3PSIDCC=AJi4QfEvx0s6YqroYvZX0hYGdBoCouIYb3ByPPM8tLInSv5WlBnYWefvFKdwYWQKkhnsRd23Qg"
    DEFAULT_HEADERS = {
                'authority': 'www.google.com',
                'method': 'GET',
                'scheme': 'https',
                'accept': "*/*",
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'cookie': '1P_JAR=2021-11-22-18; NID=511=XSpyrgXsHOdVvDPitq4Y-BfGRvjphhn6ivwvTkG0xupUavPq7Im4zM0uiaiquzrvebCfN1lZbOmnOZR4J2Ylmyl7gTMF5iOdIjy4psSx9nJuelw3mJHznoEcEr8IMy7zt6TkR6UUnpj64yhEmZ5wwsC8kH44yF9BrbzLI-FXmWI; DV=g689A68X8EsooLzqnEwKQNAxiOeO1FegFLPp11GAngAAAAA',
                'referer': 'https://www.google.com/',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
                'sec-ch-ua-mobile': "?0",
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent':choice(config.USER_AGENTS)
            }
    print(key)
    count = 1
    while True:
        try:
            # r = requests.get('http://ip-api.com/json',proxies=proxy,headers=DEFAULT_HEADERS)
            # print(r.text)
            # r = requests.get('https://ipinfo.io/ip',proxies=proxy,headers=DEFAULT_HEADERS)
            # print(r.text)
            # googleTrendsUrl = 'https://google.com'
            # response = requests.get(googleTrendsUrl,headers=DEFAULT_HEADERS)
            # if response.status_code == 200:
            #     g_cookies = response.cookies.get_dict()
            
            r = requests.get(url,proxies=proxy, headers=DEFAULT_HEADERS)
            #r = requests.get('https://www.google.com/search',proxies=proxy,headers=DEFAULT_HEADERS,params=params)
            print(count)
            count = count + 1
            if r.status_code == 200:
                break
            elif r.status_code == 466:
                print(r.reason)
            elif r.status_code == 429:
                print(r.status_code)
                print(r.text)
                print(r.request.headers)
        except requests.exceptions.RequestException as e:
            print (e.args[0].reason)
            print(e.request.headers)
    #r = requests.get('http://127.0.0.1:5000/search?q={}&faqs=yes'.format(key))
    #data = json.loads(r.content)
    data = r.content
    print(data)
    print(key)

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