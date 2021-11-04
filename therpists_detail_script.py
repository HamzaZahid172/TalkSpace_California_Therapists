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

all_image_url1 = []
all_image_url2 = []
UPC = []
description = []
match_upc = []
complete_data = {}

file = pd.read_excel('/home/hamza/Desktop/selenium_project/Therapists_data_Project/Detail_url.xlsx',header=0, converters={
                     'attribution_link': str})

# print(file)

URL = []
therapist_name = []
licensing = []
specialties = []
years_in_practice = []
state = []
complete_data = {}

for x in range(len(file['attribution_link'])):  
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)  
    print(file['attribution_link'][x])
    driver.get(file['attribution_link'][x])
    time.sleep(5)     
    name = check_exists_by_css(driver,'h2[class="c-therapist__name profile"]')
    license = check_exists_by_css(driver,'div[id="credentials"]')
    special = check_exists_by_css(driver,'div[id="specialties"]')
    years = check_exists_by_css(driver,'div[id="years-practice"]')
    stat = check_exists_by_css(driver,'li[id="breadcrumbs-state"]>a')
    if '\n' in license:
        lic = re.findall("(.*)\n(.*)", license)
        license = ' | '.join(lic[0])
    years = re.findall("\d+", years)
    years = ''.join(years)
    
    URL.append(file['attribution_link'][x])
    therapist_name.append(name)
    licensing.append(license)
    specialties.append(special)
    years_in_practice.append(years)
    state.append(stat)
    
  
    driver.close()
    
    complete_data['URL'] = URL
    complete_data['Therapist Name'] = therapist_name
    complete_data['Licensing'] = licensing
    complete_data['Specialties'] = specialties
    complete_data['Years In Practice'] = years_in_practice
    complete_data['State'] = state
        
    print(complete_data)
    Data = pd.DataFrame(complete_data)
    Data.to_excel('Final_Output.xlsx' ,index=None)
    Data.to_csv('Final_Output.csv' ,index=None)
    print("Complete Now Thanks You")
    
    
    






