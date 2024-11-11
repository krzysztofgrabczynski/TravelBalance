from django.db import models


class CurrencyRates(models.Model):
    date = models.DateField(auto_now_add=True)
    rates = models.JSONField()
