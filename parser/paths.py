import random
import time
from parser.consts import BASE_CATALOG_URL

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def parse_studios_paths(clicks) -> None:
    with webdriver.Safari() as driver:
        driver.get(BASE_CATALOG_URL + '/creators')

        for i in range(clicks):
            driver.find_element(
                value='button._1SzHD9UZti',
                by=By.CLASS_NAME
            ).click()

            time.sleep(random.randint(1, 3))

        source = driver.page_source

    bs = BeautifulSoup(source)
    names_with_hrefs = bs.find_all('a', class_='_1gIygNGZAI')

    with open('data/paths.txt', 'w') as file:
        file.writelines([i['href'] + '\n' for i in names_with_hrefs])
