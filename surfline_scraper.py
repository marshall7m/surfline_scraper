from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import time
import re
import csv
from utils import surfline_spot_scraper
import os.path

def surfline_scraper(*args, **kwargs):
    #spot names and page urls to be scraped
    spot_url_dict = {
        'malibu_close': 'https://www.surfline.com/surf-report/malibu-close-up/5cbde6df477f8600012f498d',
        'hbpier_ss': 'https://www.surfline.com/surf-report/hb-pier-southside/5977abb3b38c2300127471ec',
        #multi-cams spots
        'hbpier_ns': 'https://www.surfline.com/surf-report/hb-pier-northside/5842041f4e65fad6a7708827',
        'salt_creek': 'https://www.surfline.com/surf-report/salt-creek/5842041f4e65fad6a770882e'
        }
    
    for spot, url in spot_url_dict.items():
        driver = webdriver.Chrome()
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        #init scraper with page html and chrome driver (see utils.py)
        scraper = surfline_spot_scraper(soup, driver)
        #returns scraped data
        spot_dict = scraper.spot_dict()
        #screenshots cam footage and places png file to screenshot/{spot}/.png
        scraper.cam_screenshot(spot)

        driver.close()

        #filename for csv file
        spot_dir = 'data/'+spot+'.csv'

        #append dictionary to respective spot csv file
        if os.path.isfile(spot_dir):
            with open(spot_dir, 'a') as f:
                w = csv.DictWriter(f, spot_dict.keys())
                w.writerow(spot_dict)
        else:
            #init csv file with column header
            with open(spot_dir, 'a') as f:
                w = csv.DictWriter(f, spot_dict.keys())
                w.writeheader()
                w.writerow(spot_dict)
            

surfline_scraper()