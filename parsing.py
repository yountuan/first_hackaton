import csv
import requests
from bs4 import BeautifulSoup as BS

def get_html(url):
    response = requests.get(url)
    soup = BS(response.text, 'html.parser')
    return soup

def get_total_pages(html):
    pages_ul = html.find('div', {'class': 'listing search-page x-3'}).find('ul')
    last_page = pages_ul.find_all('li')[-3]
    total_pages = last_page.find('a').text
    return int(total_pages)

# использовала режим append, если станет много данных не удивляйтесь :)
def add_csv(data):
    with open('cars.csv', 'a') as f:
        fieldnames = ['title', 'photo', 'price']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows(data)

def get_data(html):
    cars = html.find('div', {'class': 'listing search-page x-3'}).find_all('div', {'class': 'listing-item main'})

    for car in cars:
        # title, photo, price, description
        try:
            title = car.find('div', {'class': 'sign b-l'}).find('span', {'class': 'white font-big'}).text
        except:
            title = 'no title'

        try:
            price = car.find('div', {'class': 'sign b-l'}).find('span', {'class': 'white custom-margins font-big'}).text
        except:
            price = car.find('div', {'class': 'sign b-l'}).find('span', {'class': 'white custom-margins font-small'}).text
        
        try:
            photo = car.find('img').get('data-src')
        except:
            photo = 'no pic'
        cars_data = [{'title':title, 'photo':photo, 'price':price}]
        add_csv(cars_data)

def main():
    site_url = 'https://www.mashina.kg/new/search'
    pages = '?page='

    total_pages = get_total_pages(get_html(site_url))
    for page in range(1, total_pages+1):
        final_url = site_url + pages + str(page)
        html = get_html(final_url)
        get_data(html)
        
main()


