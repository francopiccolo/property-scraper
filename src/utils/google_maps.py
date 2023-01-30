import googlemaps

gmaps = googlemaps.Client(key='AIzaSyBMiiZxvInozU_0AhGKzuZRLuwCyCZfw5Y')


import re

addresses = df['address'] + ', ' + df['location']
for address in addresses:
    address = re.sub(r"[/|]", ' ', address)
    geocode_result = gmaps.geocode(address)
    with open('data/raw/maps/' + address + '.json', 'w') as f:
        json.dump(geocode_result, f)