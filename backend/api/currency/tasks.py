from celery import shared_task

from api.currency.currencies_rates_services import save_currencies_rates


@shared_task(name="save_currencies_rates_task")
def save_currencies_rates_task():
    return save_currencies_rates()
