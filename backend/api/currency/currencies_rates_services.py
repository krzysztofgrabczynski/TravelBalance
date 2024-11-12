import requests
from dotenv import load_dotenv
import os
from datetime import date, timedelta

from api.currency.models import CurrencyRates


load_dotenv()


def save_currencies_rates() -> None:
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


def get_currency_rates_per_date(date: date) -> CurrencyRates:
    for _ in range(2):
        try:
            return CurrencyRates.objects.get(date=date)
        except:
            date -= timedelta(days=1)

    default_rates = CurrencyRates.objects.first()
    return default_rates


def convert_currency(
    amount_source_currency: float,
    rate_source_to_USD: float,
    rate_targed_to_USD: float,
) -> float:
    return (amount_source_currency / rate_source_to_USD) * rate_targed_to_USD
