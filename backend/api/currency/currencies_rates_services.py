import requests
from dotenv import load_dotenv
import os
from datetime import date, timedelta

from api.currency.models import CurrencyRates
from api.currency.email import FetchCurrencyFailedEmail


load_dotenv()


def save_currencies_rates() -> None:
    url = os.environ.get("CURRENCY_RATES_API_URL")
    headers = {"apikey": os.environ.get("CURRENCY_RATES_API_KEY")}
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    result = response.json()
    rates = result["rates"]

    try:
        CurrencyRates.objects.create(rates=rates)
    except:
        status_code = response.status_code
        try:
            message = response.message
        except Exception as e:
            message = "Error in accessing `message`: {e}"

        context = {
            "status_code": status_code,
            "message": message,
            "to": os.environ.get("NOTIFY_EMAIL_IN_FETCH_CURRENCY_FAILURE"),
        }
        FetchCurrencyFailedEmail(context=context).send()


def get_currency_rates_per_date(date: date) -> CurrencyRates:
    for _ in range(2):
        try:
            return CurrencyRates.objects.get(date=date)
        except:
            date -= timedelta(days=1)

    default_rates = CurrencyRates.objects.first()
    return default_rates
