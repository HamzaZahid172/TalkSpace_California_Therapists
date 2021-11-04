import warnings
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException 
import base64
import re



chromedriver_path = r'/home/hamza/Desktop/selenium_project/chromedriver_linux64/chromedriver'
warnings.filterwarnings("ignore")
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
wait = WebDriverWait(driver, 10)
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

def check_exists_by_css(driver,css_selector):
    try:
        output = driver.find_element_by_css_selector(css_selector)
        return output.text
    except NoSuchElementException:
        return " "


def check_exists_by_css_click(driver,css_selector):
    try:
        output = driver.find_element_by_css_selector(css_selector)
        return output
    except NoSuchElementException:
        return "0"
def check_exists_by_css_selector(driver,css_selector):
    try:
        output = driver.find_element_by_css_selector(css_selector)
        return css_selector
    except NoSuchElementException:
        return "0"

def check_exists_by_css_selector_link(driver,css_selector):
    try:
        output = driver.find_element_by_css_selector(css_selector).get_attribute('href')
        return output
    except NoSuchElementException:
        return "0"

def correct_image_url(image):

    my_image = image.split('data:image/jpeg;base64,')
    if(len(my_image) >1):  
        image_url = base64.b64decode(my_image[1])
        print(image_url)
        return image_url



file = pd.read_csv('/home/hamza/Desktop/selenium_project/Therapists_data_Project/Therapists_data_Google_url.csv',header=0, converters={
                     'Google_url': str})

# print(file)

attribution_link = []
complete_data = {}

for x in range(len(file['Google_url'])):  
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)  
    print(file['Google_url'][x])
    driver.get(file['Google_url'][x])
    time.sleep(10) 
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(10)
    # print(soup)
    search_result = soup.findAll('div', {'class': 'g'})
    print(len(search_result))
    for y in range(len(search_result)+3):

        title_link = check_exists_by_css_selector_link(driver,'div[id="search"]>div>div>div:nth-child(' + str(y+1) + ') div>a')        
        attribution_link.append(title_link)
    
  
    driver.close()
    
    complete_data['attribution_link'] = attribution_link
        
    print(complete_data)
    Data = pd.DataFrame(complete_data)
    Data.to_excel('Final_Output.xlsx' ,index=None)
    Data.to_csv('Final_Output.csv' ,index=None)
    print("Complete Now Thanks You")
    
    






