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


class TestCRUDTExpense(AuthenticateUserWithTokenMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username="test_user", password="test123!"
        )
        cls.country = Country.objects.create(name="test_country")
        cls.currency = CurrencyRates.objects.create(
            date=datetime.now(), rates={"USD": 1}
        )
        cls.trip = Trip.objects.create(
            user=cls.user, name="test_trip", currencies_rates=cls.currency
        )

    def setUp(self):
        self.client = APIClient()
        self.authenticate_user(self.client, self.user)

    def test_create_expense(self):
        response = self.client.post(
            f"/api/v1/trip/{self.trip.id}/expense/",
            {
                "title": "test_expense",
                "cost": 10,
                "category": 0,
                "currency": "USD",
            },
        )
        expense = Expense.objects.first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(expense.trip.name, "test_trip")
        self.assertEqual(expense.cost, 10)

    def test_read_expense(self):
        expense = Expense.objects.create(
            trip=self.trip,
            cost=10,
            category=0,
            currency="USD",
        )

        response = self.client.get(
            f"/api/v1/trip/{self.trip.id}/expense/{expense.id}/"
        )
        response_content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content["trip"], self.trip.id)
        self.assertEqual(response_content["cost"], 10)

    def test_update_expense(self):
        expense = Expense.objects.create(
            trip=self.trip,
            cost=10,
            category=0,
            currency="USD",
        )
        self.assertEqual(expense.cost, 10)

        response = self.client.patch(
            f"/api/v1/trip/{self.trip.id}/expense/{expense.id}/",
            {
                "cost": 15,
            },
        )
        updated_expense = Expense.objects.first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_expense.cost, 15)

    def test_delete_expense(self):
        expense = Expense.objects.create(
            trip=self.trip,
            cost=10,
            category=0,
            currency="USD",
        )

        self.assertEqual(Expense.objects.count(), 1)

        response = self.client.delete(
            f"/api/v1/trip/{self.trip.id}/expense/{expense.id}/"
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Expense.objects.count(), 0)


class TestListExpenses(AuthenticateUserWithTokenMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username="test_user", password="test123!"
        )
        cls.country = Country.objects.create(name="test_country")
        cls.currency = CurrencyRates.objects.create(
            date=datetime.now(), rates={"USD": 1}
        )
        cls.trip = Trip.objects.create(
            user=cls.user, name="test_trip", currencies_rates=cls.currency
        )

    def setUp(self):
        self.client = APIClient()
        self.authenticate_user(self.client, self.user)

    def test_list_expenses(self):
        Expense.objects.create(
            trip=self.trip,
            cost=10,
            category=0,
            currency="USD",
        )
        Expense.objects.create(
            trip=self.trip,
            cost=10,
            category=0,
            currency="USD",
        )
        response = self.client.get(f"/api/v1/trip/{self.trip.id}/expense/")
        response_content = json.loads(response.content.decode("utf-8"))
        expenses = Expense.objects.filter(trip=self.trip.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_content), len(expenses))
