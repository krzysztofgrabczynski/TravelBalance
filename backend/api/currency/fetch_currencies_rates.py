import requests
from dotenv import load_dotenv
from datetime import datetime
import os
from api.currency.models import CurrencyRates

from core.mongodb_connection import MongoDBConnection


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


def save_currencies_rates_mongodb():
    with MongoDBConnection() as db:
        collection = db["currencies_rates"]
        url = "https://api.apilayer.com/exchangerates_data/latest?base=USD"
        headers = {"apikey": "i74J7vrR4E1GOvFGowFnLgwWSD0xIef1"}
        response = requests.request("GET", url, headers=headers)
        result = response.json()

        final_result = {"date": datetime.today(), "rates": result["rates"]}

        collection.insert_one({str(datetime.today()): final_result})
