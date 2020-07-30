SOURCE_PRIVATBANK = 1
SOURCE_MONOBANK = 2
SOURCE_VKURSE = 3
SOURCE_RAIFFEISEN = 4
SOURCE_ALPHA = 5
SOURCE_MINFIN_BLACK = 6

SOURCE_CHOICES = (
    (SOURCE_PRIVATBANK, "PrivateBank"),
    (SOURCE_MONOBANK, "MonoBank"),
    (SOURCE_VKURSE, "VKurse.dp.ua"),
    (SOURCE_RAIFFEISEN, "Raiffeisen Bank"),
    (SOURCE_ALPHA, "Alpha-Bank"),
    (SOURCE_MINFIN_BLACK, "Black Market")
)

CURRENCY_TYPE_USD = 1
CURRENCY_TYPE_EUR = 2

CURRENCY_TYPES_CHOICES = (
    (CURRENCY_TYPE_USD, "USD"),
    (CURRENCY_TYPE_EUR, "EUR"),
)

RATE_TYPE_SALE = 1
RATE_TYPE_BUY = 2

RATE_TYPES_CHOICES = (
    (RATE_TYPE_SALE, "Sale"),
    (RATE_TYPE_BUY, "Buy"),
)
