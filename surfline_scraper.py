from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import time
from utils import surfline_spot_scraper
import os.path

def surfline_scraper(*args, **kwargs):
    #spot names and page urls to be scraped
    spot_url_dict = {
        'malibu_close': 'https://www.surfline.com/surf-report/malibu-close-up/5cbde6df477f8600012f498d',
        'hbpier_ss': 'https://www.surfline.com/surf-report/hb-pier-southside/5977abb3b38c2300127471ec',
        'hbpier_ns': 'https://www.surfline.com/surf-report/hb-pier-northside/5842041f4e65fad6a7708827',
        'salt_creek': 'https://www.surfline.com/surf-report/salt-creek/5842041f4e65fad6a770882e'
        }
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    scraping_start_time = time.time()
    for spot, url in spot_url_dict.items():
        print('Scraping {} ... In Progress'.format(spot))
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        #init scraper with page html and chrome driver (see utils.py)
        scraper = surfline_spot_scraper(soup, driver)
        
        #returns scraped data
        print('Scraping Numerical Data ... In Progress')
        scraper.spot_dict(spot)
        print('Scraping Numerical Data ... Done')
        
        #screenshots cam footage and places png file to screenshot/{spot}/.png
        print('Scraping Screenshot ... In Progress')
        scraper.cam_screenshot(spot)
        print('Scraping Screenshot ... Done')
        
        
        print('Scraping {} ... Done'.format(spot))
        scraping_end_time = time.time()
        runtime = scraping_end_time - scraping_start_time
        print('Approx. Scraping Runtime (secs): ', round(runtime, 2))
        print()

        driver.close()
        driver.quit()
    
surfline_scraper()