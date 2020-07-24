from decimal import Decimal

from django.db import models

from rate import model_choices as mch


class Rate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    source = models.PositiveSmallIntegerField(choices=mch.SOURCE_CHOICES)
    currency_type = models.PositiveSmallIntegerField(choices=mch.CURRENCY_TYPES_CHOICES)
    type = models.PositiveSmallIntegerField(choices=mch.RATE_TYPES_CHOICES)  # noqa

    def save(self, *args, **kwargs):
        self.amount = round(Decimal(self.amount), 2)
        super().save(*args, **kwargs)
