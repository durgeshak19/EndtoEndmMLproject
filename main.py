import json
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from tqdm import tqdm_notebook

base_url = "https://trustpilot.com"

def get_soup(url):
    return BeautifulSoup(requests.get(url).content,'lxml')


data ={}

soup = get_soup(base_url+'/categories')

for category in soup.findAll('div',{'class' : 'category-object'}):
    name = category.find('h3',{'class' : 'sub-category_header'}).text
    name = name.strip()
    data[name]={}
    sub_categories = category.find('div',{'class': 'sub-category-list'})
    for sub_category in sub_categories.findAll('div',{'class': 'child-category'}):
        sub_category_name = sub_category.find('a', {'class': 'sub-category-item'}).text
        sub_category_uri = sub_category.find('a',{'class':'sub-category-item'})['href']
        data[name][sub_category_name] = sub_category_uri

def extract_company_urls_from_page():
    a_list =webdriver.driver.find_elements_by_xpath('//a[@class="category-business-card card"]')
    urls = [a.get_attribute('href') for a in a_list]
    dedup_urls = list(set(urls))
    return dedup_urls


def go_next_page():
    try:
        button = driver.find_element_by_xpath('//a[@class="button button--primary next-page"]')
        return True, button
    except NoSuchElementException:
        return False, None

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")

prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome('./driver/chromedriver', options=options)

timeout = 3