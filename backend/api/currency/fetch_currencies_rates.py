import requests
from dotenv import load_dotenv

import os
from api.currency.models import CurrencyRates


load_dotenv()


def save_currencies_rates():
    url = os.environ.get("CURRENCY_RATES_API_URL")
    headers = {"apikey": os.environ.get("CURRENCY_RATES_API_KEY")}
    response = requests.request("GET", url, headers=headers)
    result = response.json()
    rates = result["rates"]

    try:
        CurrencyRates.objects.create(rates=rates)
    except:
        pass
        # not implemented
