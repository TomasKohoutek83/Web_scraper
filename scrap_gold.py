import requests
import os
import csv
from datetime import datetime as dt
from bs4 import BeautifulSoup as BS

DATE_FORMAT = '%d.%m.%Y %H:%M'
URL = "https://markets.businessinsider.com/commodities/gold-price"


def request_gold_price():
    r = requests.get(URL)
    soup = BS(r.text, "html.parser")
    price = soup.find('span', {'class': 'price-section__current-value'}).string
    print(f'The current price is {price}')

    chars = []
    for char in price:
        if char != ',':
            chars.append(char)

    price = ''.join(chars)
    return price


def write_data(price):
    if 'gold_price.csv' in os.listdir():
        mode = 'a'
    else:
        mode = 'w'

    with open('gold_price.csv', mode) as f:
        writer = csv.writer(f)
        writer.writerow([float(price), dt.now().strftime(DATE_FORMAT)])


write_data(request_gold_price())


