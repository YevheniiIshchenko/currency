from datetime import date, datetime
from unittest.mock import patch

from django.core.management.base import BaseCommand
from django.utils import timezone

from rate import model_choices as mch
from rate.models import Rate

import requests


def create_dates() -> list:
    d = date.today()
    start_year = d.year - 5
    start_day = d.day
    start_month = d.month
    num_days = {
        1: 31,
        2: 28,  # can be 29
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }
    dates = []
    for year in range(start_year, d.year+1):
        if year % 4 == 0:
            num_days[2] = 29
        else:
            num_days[2] = 28
        for month in range(start_month, 13):
            for day in range(start_day, num_days[month]+1):
                dates.append(f'{day}.{month}.{year}')
            start_day = 1
        start_month = 1
    return dates


mapper = {
    'USD': mch.CURRENCY_TYPE_USD,
    'EUR': mch.CURRENCY_TYPE_EUR,
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        base = 'https://api.privatbank.ua/p24api/exchange_rates?json'
        dates = create_dates()

        source = mch.SOURCE_PRIVATBANK

        for d in dates:
            res = requests.get(base, params={'date': d}).json()
            for item in res['exchangeRate']:

                currency = item.get('currency')
                if currency in mapper:
                    currency = mapper[currency]
                else:
                    continue

                with patch.object(timezone, 'now', return_value=datetime.strptime(d, '%d.%m.%Y')):
                    # buy
                    amount = item.get('purchaseRateNB')
                    if amount is None:
                        continue
                    rate_type = mch.RATE_TYPE_BUY
                    Rate.objects.create(source=source,
                                        currency_type=currency,
                                        type=rate_type,
                                        amount=amount)

                    # sale
                    amount = item.get('saleRateNB')
                    if amount is None:
                        continue
                    rate_type = mch.RATE_TYPE_SALE
                    Rate.objects.create(source=source,
                                        currency_type=currency,
                                        type=rate_type,
                                        amount=amount)
