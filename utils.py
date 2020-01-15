class surfline_spot_scraper():
    
    def __init__(self, page_html, driver):
        self.page_html = page_html
        self.driver = driver
        
    def fetch(self, feature_name, content_idx=None):
        from bs4 import BeautifulSoup
        import re
        from datetime import datetime

        """Returns feature_name parameter's respective data using BeautifulSoup scraping package. Try/excepts statements 
        are used in case page html changes. If page html changes then None value is returned and diagnostic message is
        printed. 
        
        Keyword arguments:
        feaure_name -- feature value to be scraped type(str)
        content_idx -- optional integer value to pass if scraping command requires an idx
        """

        if feature_name=='report update time':
            try:
                update_time = self.page_html.find('span', class_='quiver-forecaster-profile__update-container__last-update').contents[3]
            except AttributeError:
                print('Update html: ', feature_name)
                return None
            else:
                return datetime.strptime(re.findall(r'\d+:\d+[pa]m', update_time)[0], '%I:%M%p')

        elif feature_name=='condition':
            try:
                return self.page_html.find('div', class_='quiver-spot-report').contents[0].text
            except AttributeError:
                print('Update html: ', feature_name)
                return None

        elif feature_name=='surf height':
            try:
                raw_surf_height = self.page_html.find('div', 'quiver-spot-forecast-summary__stat-container quiver-spot-forecast-summary__stat-container--surf-height').find(class_='quiver-surf-height').contents[0]
            except AttributeError:
                try:
                    flat_surf = self.page_html.find('div', class_='quiver-spot-forecast-summary__stat-container quiver-spot-forecast-summary__stat-container--surf-height quiver-spot-forecast-summary__stat-container--surf-height--expired').find('span', class_='quiver-surf-height quiver-surf-height--flat').text
                except AttributeError:
                    print('Update html: ', feature_name)
                    return None
                else:
                    return 0.0
            else:
                if raw_surf_height == 'Flat':
                    return 0.0
                else:
                    surf_height_range = list(map(float, re.findall(r'\d+', raw_surf_height)))
                    return sum(surf_height_range) / len(surf_height_range)

        elif feature_name=='swell':
            try:
                raw_swell = self.page_html.find('div', class_='quiver-condition-stats__swells').contents[content_idx].text
            except AttributeError:
                swell_ft = None
                swell_secs = None
                swell_degrees = None
                print('Update html: ', feature_name)
            except IndexError:
                swell_ft = 0
                swell_secs = 0
                swell_degrees = 0
            else:
                swell = list(map(float, re.findall(r'\d+\.\d+|\d+', raw_swell)))
                swell_ft = swell[0]
                swell_secs = swell[1]
                swell_degrees = swell[2]
            return swell_ft, swell_secs, swell_degrees

        elif feature_name=='current tide':
            try:
                tide = self.page_html.find('span', class_='quiver-reading').text
            except (AttributeError, IndexError):
                print('Update html: ', feature_name)
                return None
            else:
                return float(re.findall(r'\d+', tide)[0])

        elif feature_name=='local extrema tide':
            try:
                local_extrema_tide = self.page_html.find_all('span', class_='quiver-reading-description')[1].text
            except AttributeError:
                local_extrema_tide_ft = None
                local_extrema_tide_time = None
                print('Update html: ', feature_name)
            else:
                local_extrema_tide_ft = float(re.findall(r'-?\d+\.\d+(?=\s?ft)|-?\d+(?=\s?ft)', local_extrema_tide)[0])
                local_extrema_tide_time = datetime.strptime(re.findall(r'\d+:\d+[pa]m', local_extrema_tide)[0], '%I:%M%p')
            return local_extrema_tide_ft, local_extrema_tide_time
       
        elif feature_name=='wind mph':
            try:
                raw_wind_mph = self.page_html.find_all('span', class_='quiver-reading')[1].text
            except (AttributeError, IndexError):
                print('Update html: ', feature_name)
                return None
            else:
                return float(re.findall(r'\d+', raw_wind_mph)[0])
            
        elif feature_name=='wind degrees':
            try:
                raw_wind_degrees = self.page_html.find_all('span', class_='quiver-reading-description')[2].text
            except (AttributeError, IndexError):
                print('Update html: ', feature_name)
                return None
            else:
                return float(re.findall(r'\d+', raw_wind_degrees)[0])

        elif feature_name=='air temperature':
            try:
                air_temp = self.page_html.find('div', class_='quiver-weather-stats').find('div').contents[1]
            except (AttributeError, IndexError):
                print('Update html: ', feature_name)
                return None
            else:
                return float(air_temp)
            
        elif feature_name=='ocean temperature':
            try:
                water_temp_range = self.page_html.find('div', class_='quiver-water-temp').find('div')
            except AttributeError:
                print('Update html: ', feature_name)
                return None
            else:
                return (float(water_temp_range.contents[1]) + int(water_temp_range.contents[5])) / 2

        elif feature_name=='daylight':
            try:
                daylight = self.page_html.find('table', class_='quiver-forecast-graphs__table quiver-forecast-graphs__table--sunlight-times').find_all('td')
            except AttributeError:
                first_light = 'update html'
                sunrise = 'update html'
                sunset = 'update html'
                last_light = 'update html'
            else:
                first_light = datetime.strptime(daylight[1].text, '%I:%M%p')
                sunrise = datetime.strptime(daylight[3].text, '%I:%M%p')
                sunset = datetime.strptime(daylight[5].text, '%I:%M%p')
                last_light = datetime.strptime(daylight[7].text, '%I:%M%p')
            return first_light, sunrise, sunset, last_light

        elif feature_name=='description':
            try:
                description = self.page_html.find('div', class_='quiver-spot-report__report-text').find_all('p')[:-1]
            except AttributeError:
                print('Update html: ', feature_name)
                return None
            else:
                return ''.join(p.get_text() for p in description).replace('\n', '').replace('\xa0', '')
        else:
            return 'feature_name options: '

    def spot_dict(self):
        from datetime import datetime
        import time
        """Returns surf spot dictionary"""

        swell_one_ft, swell_one_secs, swell_one_degrees = self.fetch('swell', content_idx=0)
        swell_two_ft, swell_two_secs, swell_two_degrees = self.fetch('swell', content_idx=1)
        swell_three_ft, swell_three_secs, swell_three_degrees = self.fetch('swell', content_idx=2)
        
        local_extrema_tide_ft, local_extrema_tide_time = self.fetch('local extrema tide')

        first_light, sunrise, sunset, last_light = self.fetch('daylight')
        
        spot_dict = {
            'scraped_time': datetime.now(),
            'report_update_time': self.fetch('report update time'),
            'condition': self.fetch('condition'),
            'surf_height': self.fetch('surf height'),
            'swell_one_ft': swell_one_ft,
            'swell_one_secs': swell_one_secs,
            'swell_one_degrees': swell_one_degrees,
            'swell_two_ft': swell_two_ft,
            'swell_two_secs': swell_two_secs,
            'swell_two_degrees': swell_two_degrees,
            'swell_three_ft': swell_three_ft,
            'swell_three_secs': swell_three_secs,
            'swell_three_degrees': swell_three_degrees,
            'current_tide': self.fetch('current tide'),
            'local_extrema_tide_ft': local_extrema_tide_ft,
            'local_extrema_tide_time': local_extrema_tide_time,
            'wind_mph': self.fetch('wind mph'),
            'wind_degrees': self.fetch('wind degrees'),
            'air_temp_f': self.fetch('air temperature'),
            'ocean_temp_f': self.fetch('ocean temperature'),
            'first_light': first_light,
            'sunrise': sunrise,
            'sunset': sunset,
            'last_light': last_light,
            'description': self.fetch('description')
            }
        return spot_dict

    def cam_screenshot(self, surf_spot):
        from selenium import webdriver
        import time
        from datetime import datetime
        from bs4 import BeautifulSoup
        
        #init cursor location on chart header above surf cam video
        element = self.driver.find_elements_by_xpath('//div[@class="sl-forecast-header__nav__page-level__link__text"]')[2]
        action = webdriver.common.action_chains.ActionChains(self.driver)

        #move cursor to surf cam block
        action.move_to_element_with_offset(element, 5, 200)

        #start surf cam video
        action.click()
        action.perform()
        #play/pause/stop button on the botton right corner of surf cam
        ad_button = self.page_html.find('div', class_="jw-icon jw-icon-inline jw-button-color jw-reset jw-icon-playback")['aria-label']

        #Check for when the advertisement stops
        while ad_button != 'Stop':
            time.sleep(10)
            ad_button = BeautifulSoup(self.driver.page_source, 'html.parser').find('div', class_="jw-icon jw-icon-inline jw-button-color jw-reset jw-icon-playback")['aria-label']
        
        #full screen the surf cam
        action.double_click()
        action.perform()
        
        #reinitiate ad button variable
        ad_button = BeautifulSoup(self.driver.page_source, 'html.parser').find('div', class_="jw-icon jw-icon-inline jw-button-color jw-reset jw-icon-playback")['aria-label']
        
        #Check for when the advertisement #2 stops
        while ad_button != 'Stop':
            time.sleep(10)
            ad_button = BeautifulSoup(self.driver.page_source, 'html.parser').find('div', class_="jw-icon jw-icon-inline jw-button-color jw-reset jw-icon-playback")['aria-label']
        time.sleep(4)
        
        #get datetime used for labeling screenshot filename
        screenshot_datetime = datetime.now()

        #save surf cam screen shot to respective surf spot screenshot dir
        self.driver.save_screenshot('screenshots/{}/{}{}{}_{}_{}.png'.format(surf_spot, screenshot_datetime.year, screenshot_datetime.month, 
                                                        screenshot_datetime.day, screenshot_datetime.hour, 
                                                        screenshot_datetime.minute))
