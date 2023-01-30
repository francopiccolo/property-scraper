import json
import re
import pandas as pd
from pathlib import Path

class Property:
    def __init__(self, property_dict):
        self.dict = property_dict
        self.set_age()
        self.set_area_total()
        self.set_location()        
        self.set_price()
        self.set_title()
        self.set_url()        
        
        # self.set_address()        
        # self.set_covered_area()
        # self.set_rooms()
        # self.set_bathrooms()
        # self.set_environments()
        # self.set_garages()

        

    def set_title(self):
        title = self.dict['title']
        if title:
            title = title.strip()
        self.title = title
    
    def set_price(self):
        # price_gap = self.dict['price_gap']
        price = self.dict['price'].strip()

        self.currency = None
        self.low_price = None
        self.high_price = None
        self.price = None
        # if price_gap:
        #     price = price_gap
        print(price)
        if price:
            if price.startswith('C'):
                return
            elif price.startswith('D'):
                price = price.split('a')            
                low_price = price[0].replace('De', '').strip()
                high_price = price[1].strip()
                self.low_price, self.currency = self.get_price_currency(low_price)
                self.high_price, self.currency = self.get_price_currency(high_price)                
            else:
                self.price, self.currency = self.get_price_currency(price)
    
    @staticmethod
    def get_price_currency(price):
        currency = None
        if 'USD' in price:
            currency = 'USD'
        elif '$' in price:
            currency = 'ARS'
        price = price.replace('USD', '').replace('$', '').replace('.', '')
        price = int(price.strip())
        return price, currency
      
    def set_location(self):
        location = self.dict.get('location')
        self.location = None
        if location:
            location = location.replace('Ver en mapa', '')
            self.location = location.strip()
            self.location = re.sub(r"[/|°]", ' ', self.location)
        

    def set_address(self):
        address = self.dict['address']
        address = address.replace('al', '')
        self.address = address.strip()
        
    def preprocess_feature(self, feature, string):
        feature = self.dict[feature]
        if feature:
            feature = int(feature.replace(string, '').strip())
        return feature
    
    @staticmethod
    def get_area_unit(area):        
        unit = None
        if 'm²' in area:
            unit = 'm²'
        elif 'ha' in area:
            unit = 'ha'
        
        area = int(area.replace('m²', '').replace('ha', '').replace('Total', '').strip())
        return area, unit
    
    def set_area_total(self):
        area = self.dict['area_total']
        self.total_area = None
        self.area_unit = None
        if area:
            self.total_area, self.area_unit = self.get_area_unit(area)
        
    
    def set_covered_area(self):
        area = self.dict['covered_area']
        self.covered_area = None
        self.area_unit = None
        if area:
            area = area.replace('Cubierta', '')
            self.covered_area, self.area_unit = self.get_area_unit(area)

    def set_rooms(self):
        self.rooms = self.preprocess_feature('rooms', 'dorm.')
    
    def set_bathrooms(self):
        bathrooms = self.dict['bathrooms']
        if bathrooms:
            bathrooms = re.sub(r'baño(s)?', '', bathrooms)
            bathrooms = int(bathrooms.strip())
        self.bathrooms = bathrooms

    def set_environments(self):
        self.environments = self.preprocess_feature('environments', 'amb.')

    def set_garages(self):
        self.garages = self.preprocess_feature('garages', 'coch.')
    
    def set_age(self):
        age = self.dict['age']
        if age:
            age = age.replace('Antigüedad', '')
            age = age.replace('En construcción', '-1')
            age = age.replace('A estrenar', '0')            
            age = int(age.strip())

        self.age = age
    
    def set_url(self):
        url = self.dict['url']
        if url:
            url = url.strip()
        self.url = url
        
    def get_attributes(self):
        return {
            'currency': self.currency,
            'location':  self.location,
            'price':  self.price,
            'title': self.title,
            'area_total':  self.total_area,
            'age':  self.age,
            'url':  self.url,
            
            # 'low_price':  self.low_price,
            # 'high_price':  self.high_price,                        
            # 'address':  self.address,                
            # 'covered_area':  self.covered_area,
            # 'rooms':  self.rooms,
            # 'bathrooms':  self.bathrooms,
            # 'environments':  self.environments,
            # 'garages':  self.garages,
}


def preprocess():
    df = pd.DataFrame(columns=['age', 'area_unit', 'area_total', 'location', 'price', 'url'])
    # 'title', 'currency', 'low_price', 'high_price',  'address',  'covered_area', 'rooms', 'bathrooms', 'environments', 'garages',  'file', 'locality', 'neighborhood', 'route', 'street_number', 'lat', 'long'
    for i in range(1, 13):
        with open('./data/raw/zonaprop/terrenos/{}.json'.format(i), 'rb') as f:
            properties = json.load(f)

        for property in properties:
            property = Property(property)        
            # address = Address(property.address, property.location)
            data = property.get_attributes()
            # data.update(address.get_attributes())            
            data['file'] = i
            df = df.append(data, ignore_index=True)

    df['location'] = df['location'].astype(str)
    df['price_per_square_meter'] = df['price'] / df['area_total']
    df.drop_duplicates(subset=['url'], inplace=True)
    df.to_csv('./data/preprocessed/terrenos/df.csv', index=False)

if __name__ == '__main__':
    preprocess()