import requests
import json
import pandas as pd
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

for key in orignal:
    r = requests.get('http://127.0.0.1:5000/search?q={}&faqs=yes'.format(key))
    data = json.loads(r.content)
    print(data)

