import requests
from bs4 import BeautifulSoup
from decimal import Decimal


def to_decimal(num) -> Decimal:
    return round(Decimal(num), 2)


url = 'https://minfin.com.ua/currency/'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
items = (soup.find_all('td', {'data-title': 'Черный рынок'}))
list_cur = [item.text.replace('\n', '').replace(',','.') for item in items]
list_cur = list_cur[0:2]
amounts = []
for l in list_cur:
    amounts += l.split(' /')
for i in range(len(amounts)):
    amounts[i] = to_decimal(amounts[i])
print(amounts)