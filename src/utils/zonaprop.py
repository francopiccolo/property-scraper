

class PropertyCard:
    CLASS = 'sc-n2cjqs-0' # Posting card gallery class
    CLASS = 'sc-i1odl-2' # Posting card text class
    
    def __init__(self, soup):
        self.soup = soup
        main_features = {}
        for main_feature in self.soup.find("ul", class_="postingCardMainFeatures").find_all("li"):
            i = main_feature.find("i")
            if i:
                classes = i['class']
                feature = [class_ for class_ in classes if class_ != 'postingCardIconsFeatures']
                main_features[feature[0]] = main_feature.text            
        self.main_features = main_features
    
    def get_price_gap(self):
        div_price_gap = self.soup.find("div", class_="priceGap")
        if div_price_gap:
            return div_price_gap.text.strip()
    
    def get_price_na(self):
        span_price_gap = self.soup.find("span", class_="priceGap")
        if span_price_gap:
            return span_price_gap.text
    
    def get_fixed_price(self):
        span_first_price = self.soup.find("span", class_="firstPrice")
        if span_first_price:
            return span_first_price.text.strip()
    
    def get_location(self):
        span_posting_card_location = self.soup.find("span", class_="postingCardLocation")
        if span_posting_card_location:
            location = span_posting_card_location
        div_location = self.soup.find("div", class_="location")
        if div_location:
            location = div_location.span
        return location.text
    
    def get_address(self):
        span_posting_card_location_title = self.soup.find("span", class_="postingCardLocationTitle")
        if span_posting_card_location_title:
            address = span_posting_card_location_title
        div_address = self.soup.find("div", class_="address")
        if div_address:
            address = div_address.span
        return address.text
    
    def get_area(self):
        return self.main_features.get('iconArea')
    
    def get_rooms(self):
        return self.main_features.get('iconBedrooms')
    
    def get_bathrooms(self):
        return self.main_features.get('iconBathrooms')
    
    def get_environments(self):
        return self.main_features.get('iconEnvironments')
    
    def get_garages(self):
        return self.main_features.get('iconGarage')
    
    def get_attributes(self):
        return {'price': self.get_fixed_price(),
                'price_na': self.get_price_na(),
                'price_gap': self.get_price_gap(),
                'location': self.get_location(),
                'address': self.get_address(),
                'area': self.get_area(),
                'rooms': self.get_rooms(),
                'bathrooms': self.get_bathrooms(),
                'environments': self.get_environments(),
                'garages': self.get_garages()}


class PropertyArticle:
    CLASS = 'layout-container'
    def __init__(self, soup):
        self.soup = soup
        icon_features = {}
        for icon_feature in self.soup.find_all("li", class_="icon-feature"):
            i = icon_feature.find("i")
            if i:
                class_ = i['class'][0]
                icon_features[class_] = icon_feature.text           
        self.icon_features = icon_features

    def get_age(self):
        return self.icon_features.get('icon-antiguedad')

    def get_area_covered(self):
        return self.icon_features.get('icon-scubierta')
    
    def get_area_total(self):
        return self.icon_features.get('icon-stotal')
    
    def get_location(self):
        try:
            location = self.soup.find('h2', class_='title-location').text
        except AttributeError:
            location = None
        return location
    
    def get_price_operation(self):
        return self.soup.find("div", class_="price-operation")

    def get_price_items(self):
        return self.soup.find("div", class_="price-items").text

    def get_title(self):
        return self.soup.find("div", class_="section-title").text      
    
    def get_attributes(self):
        return {'age': self.get_age(),
                'area_total': self.get_area_total(),
                'location': self.get_location(),
                'price': self.get_price_items(),
                'title': self.get_title()
                }