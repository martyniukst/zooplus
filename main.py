import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import csv

chrome_options = Options()
options = selenium.webdriver.ChromeOptions()
driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)

def scraping():
    driver.get('https://www.zooplus.de/tierarzt/results')
    time.sleep(3)
    btn = driver.find_element_by_id('onetrust-reject-all-handler')
    btn.click()
    data = [['Title', 'Subtitle', 'Hours', 'Address', 'Empfehlungen', 'Rating']]
    for i in range (1,6):
        url = 'https://www.zooplus.de/tierarzt/results?animal_99=true&page='+str(i)
        driver.get(url)
        time.sleep(2)
        ones = driver.find_elements_by_class_name('result-intro__link')
        for item in ones:
            res = item.get_attribute('outerHTML')
            soup = BeautifulSoup(res, 'html.parser')
            title = soup.find(class_='result-intro__title').text
            try:
                subtitle = soup.find(class_='result-intro__subtitle').text
            except:
                subtitle = 'no subtitle'
            hours = soup.find(class_='result-intro__hours').text
            address = soup.find(class_='result-intro__address').text
            empfehlungen = soup.find(class_='result-intro__rating__note').text
            rating = item.get_attribute('outerHTML').count('<span aria-hidden="true" class="fa fa-star">')
            locallist = [title, subtitle, hours, address, empfehlungen, rating]
            data.append(locallist)
    driver.close()
    return write_csv(data)
def write_csv(data):
    file = open('done.csv', 'w+')
    with file:
        writer = csv.writer(file)
        writer.writerows(data)

if __name__ == "__main__":
    scraping()
