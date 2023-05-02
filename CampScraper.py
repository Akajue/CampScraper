import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

class CampScraper:

    def __init__(self):
        self.base_url = 'https://www.camptocamp.org/waypoints?wtyp=summit&offset={}&limit=100'
        self.data = []

    def writeCsv(self, data):
        with open('site.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['titre', 'localisation', 'altitude', 'lien'])
            writer.writeheader()
            for row in data:
                writer.writerow(row)

    def scrap_page(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run Chrome in headless mode
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)  # Wait for up to 10 seconds for an element to load

        try:
            page = 0
            while page < 1000:
                url = self.base_url.format(page)
                driver.get(url)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'document-card')))
                html = driver.page_source
                if html:
                    soup = BeautifulSoup(html, 'html.parser')
                    for mountain in soup.find_all('div', {'class': 'document-card'}):
                        try:
                            title = mountain.find('span', {'class': None}).text.strip()
                            location = mountain.find('span', {'class': 'is-ellipsed'}).text.strip()
                            altitude = mountain.find('span', {'class': 'is-nowrap'}).text.strip().replace("m", "")
                            link = mountain.find('a', ).get('href')
                            altitude = int(altitude)
                            if altitude > 2000:
                                self.data.append({'titre': title, 'localisation': location, 'altitude': altitude, 'lien': link})
                        except:
                            continue
                    page += 100
                else: 
                    break
        finally:
            driver.quit()

        self.writeCsv(self.data)
scraper = CampScraper()
scraper.scrap_page()
