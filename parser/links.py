from bs4 import BeautifulSoup
from selenium import webdriver

with open('data/paths.txt') as file:
    paths = file.readlines()

hrefs = []


def parse_studios_links():
    with webdriver.Safari() as driver:
        for path in paths:
            driver.get(f'https://cmsmagazine.ru{path}')
            bs = BeautifulSoup(driver.page_source)

            div = bs.find('div', class_='_3LwepWoDjL')
            hrefs.append(div.find('a')['href'] + '\n')

    with open('data/links.txt', 'w') as links:
        links.writelines(map(str, hrefs))
