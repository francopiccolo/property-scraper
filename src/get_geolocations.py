import json
import re
from pathlib import Path

import googlemaps
import pandas as pd

from config import GMAPS_API_KEY

class Location:
    def __init__(self, location): # address
        # self.address = address
        self.location = location
        self.locality = None
        self.neighborhood = None
        self.route = None
        self.street_number = None
        self.lat = None
        self.long = None
        
        file = Path('data/raw/maps/terrenos/' + location + '.json')
        
        if file.is_file():
            with open(file, 'r') as f:
                self.geocode = json.load(f)

            if self.geocode:
                for component in self.geocode[0]['address_components']:
                    if 'street_number' in component['types']:
                        self.street_number = component['long_name']
                    elif 'route' in component['types']:
                        self.route = component['long_name']
                    elif 'neighborhood' in component['types']:
                        self.neighborhood = component['long_name']
                    elif 'locality' in component['types']:
                        self.locality = component['long_name']
                self.lat = self.geocode[0]['geometry']['location']['lat']
                self.long = self.geocode[0]['geometry']['location']['lng']
                self.types = self.geocode[0]['types']
    
    def get_attributes(self):
        return {
            'lat': self.lat,
            'locality': self.locality,
            'location': self.location,
            'long': self.long,
            'neighborhood': self.neighborhood,
            'route': self.route,
            'street_number': self.street_number,                
        }

def get_geolocations():
    google_maps_client = googlemaps.Client(key=GMAPS_API_KEY)

    df = pd.read_csv('./data/preprocessed/terrenos/df.csv')

    for property in df.itertuples():
        maps_file = Path('./data/raw/maps/terrenos/' + property.location + '.json')
        if maps_file.is_file():
            continue    
        geocode_result = google_maps_client.geocode(property.location)
        with open(maps_file, 'w') as f:
            json.dump(geocode_result, f)

def enrich_properties():
    df_locations = pd.DataFrame()
    df_properties = pd.read_csv('./data/preprocessed/terrenos/df.csv')
    for property in df_properties.itertuples():
        location = Location(property.location)        
        data = location.get_attributes()
        df_locations = df_locations.append(data, ignore_index=True)

    new_df = df_properties.merge(df_locations, on='location')
    new_df.dropna(subset=['lat', 'long'], inplace=True)
    new_df.to_csv('./data/preprocessed/terrenos/df2.csv', index=False)

if __name__ == '__main__':
    enrich_properties()