import time

from selenium import webdriver

driver = webdriver.Safari()
driver.get("https://cmsmagazine.ru/creators/")

for i in range(10):
    driver.find_element_by_class_name('button._1SzHD9UZti').click()
    time.sleep(0.5)

with open('catalog.html', 'w') as file:
    file.write(driver.page_source)

driver.close()
