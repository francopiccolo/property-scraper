from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# options.add_argument('--disable-blink-features=AutomationControlled')

driver_path = '/Users/francopiccolo/Utils/chromedriver109'

def wait_for_class(driver, class_):
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, class_))
    )

def wait_for_new_window(driver, timeout=10):
    WebDriverWait(driver, timeout).until(
        lambda driver: len(driver.window_handles) == 2)

# driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
driver = uc.Chrome(executable_path=driver_path)