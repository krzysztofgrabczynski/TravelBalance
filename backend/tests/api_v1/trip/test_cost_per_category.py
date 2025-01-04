from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime
from rest_framework.test import APIClient
import json

from api.expense.models import Expense
from api.trip.models import Trip, Country
from api.currency.models import CurrencyRates
from tests.mixins.authentication import AuthenticateUserWithTokenMixin


User = get_user_model()


class TestCostPerCategoryTrip(AuthenticateUserWithTokenMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username="test_user", password="test123!"
        )
        cls.country = Country.objects.create(name="test_country")
        cls.currency = CurrencyRates.objects.create(
            date=datetime.now(), rates={"USD": 1}
        )

    def setUp(self):
        self.client = APIClient()
        self.authenticate_user(self.client, self.user)

    def test_get_cost_per_category(self):
        trip = Trip.objects.create(
            user=self.user,
            name="test_trip",
            currencies_rates=self.currency,
        )
        trip.countries.set([self.country.id])

        activities_category = 0
        accomodation_category = 1
        food_category = 2
        activities_cost = 10
        accomodation_cost = 5
        Expense.objects.create(
            trip=trip,
            cost=activities_cost,
            category=activities_category,
            currency="USD",
        )
        Expense.objects.create(
            trip=trip,
            cost=accomodation_cost,
            category=accomodation_category,
            currency="USD",
        )

        response = self.client.get(
            f"/api/v1/trip/{trip.id}/get_cost_per_category/"
        )

        response_content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_content[str(activities_category)], activities_cost
        )
        self.assertEqual(
            response_content[str(accomodation_category)], accomodation_cost
        )
        self.assertEqual(response_content[str(food_category)], 0)
