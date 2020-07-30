from decimal import Decimal

from bs4 import BeautifulSoup

from celery import shared_task

from rate import model_choices as mch
from rate.models import Rate

import requests


def to_decimal(num) -> Decimal:
    return round(Decimal(num), 2)


@shared_task
def parse_private():
    mapper = {
        'USD': mch.CURRENCY_TYPE_USD,
        'EUR': mch.CURRENCY_TYPE_EUR,
    }
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url)
    items = response.json()
    for item in items:
        if item['ccy'] not in mapper:
            continue

        currency_type = mapper[item['ccy']]

        # buy
        amount = to_decimal(item['buy'])
        last_rate = Rate.objects.filter(currency_type=currency_type,
                                        type=mch.RATE_TYPE_BUY,
                                        source=mch.SOURCE_PRIVATBANK).last()

        if last_rate is None or amount != last_rate.amount:
            Rate.objects.create(currency_type=currency_type,
                                source=mch.SOURCE_PRIVATBANK,
                                amount=amount,
                                type=mch.RATE_TYPE_BUY)

        # sale
        amount = to_decimal(item['sale'])

        last_rate = Rate.objects.filter(currency_type=currency_type,
                                        type=mch.RATE_TYPE_SALE,
                                        source=mch.SOURCE_PRIVATBANK).last()

        if last_rate is None or amount != last_rate.amount:
            Rate.objects.create(currency_type=currency_type,
                                source=mch.SOURCE_PRIVATBANK,
                                amount=amount, type=mch.RATE_TYPE_SALE)


@shared_task
def parse_monobank():
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    items = response.json()
    mapper = {
        840: mch.CURRENCY_TYPE_USD,
        978: mch.CURRENCY_TYPE_EUR,
    }

    source = mch.SOURCE_MONOBANK

    for item in items:

        if item == 'errorDescription':
            continue

        if item["currencyCodeA"] not in mapper or item["currencyCodeB"] != 980:
            continue

        currency = mapper[item['currencyCodeA']]

        # buy

        amount = to_decimal(item['rateBuy'])

        last_rate = Rate.objects.filter(currency_type=currency,
                                        type=mch.RATE_TYPE_BUY,
                                        source=source).last()

        if last_rate is None or last_rate.amount != amount:
            Rate.objects.create(currency_type=currency,
                                type=mch.RATE_TYPE_BUY,
                                source=source,
                                amount=amount)

        # sale

        amount = to_decimal(item['rateSell'])

        last_rate = Rate.objects.filter(currency_type=currency,
                                        type=mch.RATE_TYPE_SALE,
                                        source=source).last()

        if last_rate is None or last_rate.amount != amount:
            Rate.objects.create(currency_type=currency,
                                type=mch.RATE_TYPE_SALE,
                                source=source,
                                amount=amount)


@shared_task
def parse_vkurse():
    url = 'http://vkurse.dp.ua/course.json'
    res = requests.get(url)
    items = res.json()

    mapper = {
        'Dollar': mch.CURRENCY_TYPE_USD,
        'Euro': mch.CURRENCY_TYPE_EUR,
    }

    source = mch.SOURCE_VKURSE

    for item in items:
        if item not in mapper:
            continue

        currency = mapper[item]

        # buy

        amount = to_decimal(items[item]['buy'])

        last_rate = Rate.objects.filter(source=source,
                                        currency_type=currency,
                                        type=mch.RATE_TYPE_BUY).last()

        if last_rate is None or last_rate.amount != amount:
            Rate.objects.create(amount=amount,
                                source=source,
                                currency_type=currency,
                                type=mch.RATE_TYPE_BUY)
        # sale

        amount = to_decimal(items[item]['sale'])

        last_rate = Rate.objects.filter(source=source,
                                        currency_type=currency,
                                        type=mch.RATE_TYPE_SALE).last()

        if last_rate is None or last_rate.amount != amount:
            Rate.objects.create(amount=amount,
                                source=source,
                                currency_type=currency,
                                type=mch.RATE_TYPE_SALE)


@shared_task()
def parse_raiffeisen():

    url = 'https://ex.aval.ua/ru/personal/everyday/exchange/exchange/'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    items = (soup.find_all('td', {'class': 'right'}))
    amounts = [to_decimal(item.text.replace(',', '.')) for item in items]
    amounts = amounts[0:4]
    for i in range(len(amounts)):
        if i < 2:
            currency = mch.CURRENCY_TYPE_USD
        else:
            currency = mch.CURRENCY_TYPE_EUR

        if i % 2 == 0:
            rate_type = mch.RATE_TYPE_BUY
        else:
            rate_type = mch.RATE_TYPE_SALE

        last_rate = Rate.objects.filter(source=mch.SOURCE_RAIFFEISEN,
                                        currency_type=currency,
                                        type=rate_type).last()

        if last_rate is None or last_rate.amount != amounts[i]:
            Rate.objects.create(source=mch.SOURCE_RAIFFEISEN,
                                currency_type=currency,
                                type=rate_type,
                                amount=amounts[i])


@shared_task
def parse_alpha():

    url = 'https://alfabank.ua/currency-exchange?refId=MainPageBestOffers'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    items = (soup.find_all('div', {'class': 'currency-item-number'}))
    amounts = [to_decimal(item.text) for item in items[-4:]]

    for i in range(len(amounts)):
        if i < 2:
            currency = mch.CURRENCY_TYPE_USD
        else:
            currency = mch.CURRENCY_TYPE_EUR

        if i % 2 == 0:
            rate_type = mch.RATE_TYPE_BUY
        else:
            rate_type = mch.RATE_TYPE_SALE

        last_rate = Rate.objects.filter(source=mch.SOURCE_ALPHA,
                                        currency_type=currency,
                                        type=rate_type).last()

        if last_rate is None or last_rate.amount != amounts[i]:
            Rate.objects.create(source=mch.SOURCE_ALPHA,
                                currency_type=currency,
                                type=rate_type,
                                amount=amounts[i])


@shared_task
def parse_black():
    url = 'https://minfin.com.ua/currency/'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    items = (soup.find_all('td', {'data-title': 'Черный рынок'}))
    list_cur = [item.text.replace('\n', '').replace(',', '.') for item in items]
    list_cur = list_cur[0:2]
    amounts = []
    for item1 in list_cur:
        amounts += item1.split(' /')

    for i in range(len(amounts)):
        amounts[i] = to_decimal(amounts[i])

    for i in range(len(amounts)):
        if i < 2:
            currency = mch.CURRENCY_TYPE_USD
        else:
            currency = mch.CURRENCY_TYPE_EUR

        if i % 2 == 0:
            rate_type = mch.RATE_TYPE_BUY
        else:
            rate_type = mch.RATE_TYPE_SALE

        last_rate = Rate.objects.filter(source=mch.SOURCE_MINFIN_BLACK,
                                        currency_type=currency,
                                        type=rate_type).last()

        if last_rate is None or last_rate.amount != amounts[i]:
            Rate.objects.create(source=mch.SOURCE_MINFIN_BLACK,
                                currency_type=currency,
                                type=rate_type,
                                amount=amounts[i])


@shared_task
def parse():
    parse_private.delay()
    parse_monobank.delay()
    parse_vkurse.delay()
    parse_raiffeisen.delay()
    parse_alpha.delay()
    parse_black.delay()
