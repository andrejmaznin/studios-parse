from bs4 import BeautifulSoup
from selenium import webdriver

with open('../data/urls.txt') as file:
    urls = file.readlines()

driver = webdriver.Safari()

with open('../data/links.txt', 'w') as links:
    hrefs = []
    for url in urls:
        driver.get(f'https://cmsmagazine.ru{url}')

        bs = BeautifulSoup(driver.page_source)
        div = bs.find('div', class_='_3LwepWoDjL')
        hrefs.append(div.find('a')['href'] + '\n')

    links.writelines(map(str, hrefs))

driver.close()
