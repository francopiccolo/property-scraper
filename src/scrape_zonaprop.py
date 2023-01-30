import json
import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException

from src.utils.zonaprop import PropertyArticle, PropertyCard
from src.utils.selenium import driver, wait_for_class, wait_for_new_window

def process_card(driver, card, properties):
    card.click()        
    wait_for_new_window(driver)
    driver.switch_to.window(driver.window_handles[1])
    wait_for_class(driver, PropertyArticle.CLASS)
    property_url = driver.current_url
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    property_article = PropertyArticle(soup)
    attributes = property_article.get_attributes()
    attributes['url'] = property_url
    properties.append(attributes)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def process_cards(driver, cards):
    properties = []
    for card in cards[:num_cards_to_process]:
        process_card(driver, card, properties)
    return properties

num_cards_to_process = 20

def scrape():
    num_properties = 3600
    num_properties_per_page = 20
    num_pages = num_properties // num_properties_per_page + 1
    
    URL = 'https://www.zonaprop.com.ar/terrenos-venta-santa-fe-mas-400-m2-menos-200000-dolar.html'

    print('Processing page 1')
    driver.get(URL)
    wait_for_class(driver, PropertyCard.CLASS)
    cards = driver.find_elements(By.CLASS_NAME, PropertyCard.CLASS)
    properties = process_cards(driver, cards)

    with open('./data/raw/zonaprop/terrenos/1.json', 'w') as outfile:
        json.dump(properties, outfile)

    for page_num in range(2, num_pages + 1):
        print('Processing page ', page_num)    
        next_page = driver.find_element(By.CSS_SELECTOR, '.sc-n5babu-2.jRAhtM')
        next_page.click()
        cards = driver.find_elements(By.CLASS_NAME, PropertyCard.CLASS)
        while True:
            try:
                properties = process_cards(driver, cards)
                break
            except (StaleElementReferenceException, ElementClickInterceptedException):
                cards = driver.find_elements(By.CLASS_NAME, PropertyCard.CLASS)
                time.sleep(1)
        
        with open('./data/raw/zonaprop/terrenos/{}.json'.format(page_num), 'w') as outfile:
            json.dump(properties, outfile)


if __name__ == '__main__':
    scrape()