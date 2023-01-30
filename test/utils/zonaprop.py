from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from src.utils.zonaprop import PropertyArticle, PropertyCard

from src.utils.selenium import driver, wait_for_class, wait_for_new_window

URL = 'https://www.zonaprop.com.ar/terrenos-venta-santa-fe-mas-300-m2-menos-200000-dolar.html'

def test_property_card():
    
    driver.get(URL.format(1))
    wait_for_class(driver, PropertyCard.CLASS)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    cards_soups = soup.find_all("div", class_=PropertyCard.CLASS)

    attributes = property_card.get_attributes()
    print(attributes)

def test_property_article():
    driver.get(URL.format(1))
    wait_for_class(driver, PropertyCard.CLASS)
    cards = driver.find_elements(By.CLASS_NAME, PropertyCard.CLASS)
    card = cards[0]
    card.click()
    wait_for_new_window(driver)
    driver.switch_to.window(driver.window_handles[1])
    wait_for_class(driver, 'layout-container')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    property_article = PropertyArticle(soup)
    print(property_article.get_price_items())

def test_page_change():
    driver.get(URL)
    wait_for_class(driver, PropertyCard.CLASS)
    next_page = driver.find_element(By.CSS_SELECTOR, '.sc-n5babu-2.jRAhtM')
    next_page.click()
    wait_for_class(driver, PropertyCard.CLASS)
    cards = driver.find_elements(By.CLASS_NAME, PropertyCard.CLASS)
    card = cards[0]
    card.click()




if __name__ == '__main__':
    # test_property_article()
    test_page_change()