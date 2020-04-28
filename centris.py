from django.core.management.base import BaseCommand, CommandError
import requests
from django.db import IntegrityError
from bs4 import BeautifulSoup as bs
import shutil
import re
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv


def get_driver():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 1,
             "profile.default_content_setting_values.notifications": 2,
             "profile.managed_default_content_settings.stylesheets": 2,
             "profile.managed_default_content_settings.javascript": 1,
             "profile.managed_default_content_settings.plugins": 1,
             "profile.managed_default_content_settings.popups": 2,
             "profile.managed_default_content_settings.geolocation": 2,

    }
    chrome_options.add_experimental_option("prefs", prefs)
    capabilites = chrome_options.to_capabilities()
    driver = webdriver.Remote(
        desired_capabilities=capabilites,
        command_executor='http://selenium-hub:4444/wd/hub'
    )
    return driver


def download_image(url, directory='/images'):
    response = requests.get(
        url, stream=True
    )
    image_name = url.split('/')[-1].split('?')[0]

    image_path = '{}/{}'.format(directory, image_name)

    with open(image_path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

    return image_path


def write_to_csv(list_of_dict, output_file):
    keys = list_of_dict[0].keys()
    with open(f'{output_file}.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dict)


def get_information(driver):
    details = {}
    try:
        details['centris_no'] = driver.find_element_by_xpath(
            '//*[@id="ListingDisplayId"]'
        ).text
    except Exception:
        details['centris_no'] = ''
        pass
    try:
        details['property_type'] = driver.find_element_by_xpath(
            '//*[@data-id="PageTitle"]'
        ).text
    except Exception:
        details['property_type'] = ''
        pass
    try:
        details['price'] = driver.find_element_by_xpath(
            '//*[@id="BuyPrice"]'
        ).text
    except Exception:
        details['price'] = ''
        pass
    try:
        details['address'] = driver.find_element_by_xpath(
            '//*[@itemprop="address"]'
        ).text.split(',')[0]
    except Exception:
        details['address'] = ''
        pass
    try:
        details['municipality'] = driver.find_element_by_xpath(
            '//*[@itemprop="address"]'
        ).text.split(',')[1]
    except Exception:
        details['municipality'] = ''
        pass
    try:
        latitude = driver.find_element_by_xpath(
            '//*[@itemprop="latitude"]'
        ).get_attribute('content')
    except Exception:
        pass
    try:
        longitude = driver.find_element_by_xpath(
            '//*[@itemprop="longitude"]'
        ).get_attribute('content')
    except Exception:
        pass
    try:
        details['coordinates'] = f'Lat:{latitude}, Lon:{longitude}'
    except Exception:
        details['coordinates'] = ''
        pass
    try:
        details['bedrooms'] = driver.find_element_by_xpath(
            '//div[@class="row teaser"]//*[contains(text(),"bedrooms")]'
        ).text
    except Exception:
        details['bedrooms'] = ''
        pass
    try:
        details['bathrooms'] = driver.find_element_by_xpath(
            '//div[@class="row teaser"]//*[contains(text(),"bathroom")]'
        ).text
    except Exception:
        details['bathrooms'] = ''
        pass
    try:
        details['powder_rooms'] = driver.find_element_by_xpath(
            '//div[@class="row teaser"]//*[contains(text(),"powder room")]'
        ).text
    except Exception:
        details['powder_rooms'] = ''
        pass
    try:
        details['building_style'] = driver.find_element_by_xpath(
            '//*[contains(text(),"Building style")]/../div[@class="carac-value"]'
        ).text
    except Exception:
        details['building_style'] = ''
        pass
    try:
        details['year_built'] = driver.find_element_by_xpath(
            '//*[contains(text(),"Year built")]/../div[@class="carac-value"]'
        ).text
    except Exception:
        details['year_built'] = ''
        pass
    try:
        details['lot_area'] = driver.find_element_by_xpath(
            '//*[contains(text(),"Lot area")]/../div[@class="carac-value"]'
        ).text
    except Exception:
        details['lot_area'] = ''
        pass
    try:
        details['net_area'] = driver.find_element_by_xpath(
            '//*[contains(text(),"Net area")]/../div[@class="carac-value"]'
        ).text
    except Exception:
        details['net_area'] = ''
        pass
    try:
        details['listing_hyperlink'] = driver.current_url
    except Exception:
        details['listing_hyperlink'] = ''
        pass
    return details
    

driver = get_driver()
url = "https://www.centris.ca/en"
driver.get(url)
time.sleep(5)
try:
    driver.find_element_by_xpath(
        '//a/*[contains(text(),"Search")]'
    ).click()
except Exception:
    pass
try:
    driver.find_element_by_xpath(
        '//a[contains(text(),"Summary")]'
    ).click()
except Exception:
    pass

try:
    page_number = int(
        driver.find_element_by_xpath(
            '//*[@class="pager-current"]'
        ).text.split[' / '][1]
    )
except Exception:
    pass

post_list = []
post_list.append(get_information(driver))

for i in range(5):
    try:
        driver.find_element_by_xpath(
            '//*[@class="next"]/a'
        ).click()
        time.sleep(5)
        post_list.append(get_information(driver))
    except Exception:
        continue

write_to_csv(post_list, 'output_file')
print("the posts have been written to output_file.csv")
