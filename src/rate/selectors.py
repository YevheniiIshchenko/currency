from django.core.cache import cache

from rate import model_choices as mch
from rate.models import Rate


def get_cache_key(source, currency, type_):
    return f'{source}_{currency}_{type_}'


def get_latest_rates():
    object_list = []

    for s in mch.SOURCE_CHOICES:
        source = s[0]
        for cur in mch.CURRENCY_TYPES_CHOICES:
            currency = cur[0]
            for r in mch.RATE_TYPES_CHOICES:
                rate_type = r[0]

                key = get_cache_key(source, currency, rate_type)
                cached_rate = cache.get(key)

                if cached_rate is None:
                    rate = Rate.objects.filter(
                        source=source,
                        currency_type=currency,
                        type=rate_type
                    ).order_by('created').last()

                    if rate is not None:
                        cache.set(key, rate, 60*15)
                        object_list.append(rate)
                else:
                    object_list.append(cached_rate)

    return object_list
