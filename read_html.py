from bs4 import BeautifulSoup

with open('catalog.html') as page:
    text = page.read()
    bs = BeautifulSoup(text)

links = bs.findAll("a", class_='_1gIygNGZAI')
hrefs = []

for link in links:
    hrefs.append(link["href"])

hrefs = [i + '\n' for i in filter(lambda a: not a.startswith('http'), hrefs)]

with open('urls.txt', 'w') as file:
    file.writelines(hrefs)
