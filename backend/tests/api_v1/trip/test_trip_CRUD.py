from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime
from rest_framework.test import APIClient
import json

from api.trip.models import Trip, Country
from api.currency.models import CurrencyRates
from tests.mixins.authentication import AuthenticateUserWithTokenMixin


User = get_user_model()


class TestCRUDTrip(AuthenticateUserWithTokenMixin, TestCase):
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

    def test_create_trip(self):
        response = self.client.post(
            "/api/v1/trip/",
            {
                "user": self.user,
                "name": "test_trip",
                "countries": [self.country.id],
                "currencies_rates": self.currency,
            },
        )
        trip = Trip.objects.first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(trip.user, self.user)
        self.assertEqual(trip.name, "test_trip")

    def test_read_trip(self):
        trip = Trip.objects.create(
            user=self.user,
            name="test_trip",
            currencies_rates=self.currency,
        )

        trip.countries.set([self.country.id])

        response = self.client.get(f"/api/v1/trip/{trip.id}/")
        response_content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content["name"], "test_trip")

    def test_update_trip(self):
        trip = Trip.objects.create(
            user=self.user,
            name="test_trip",
            currencies_rates=self.currency,
        )
        trip.countries.set([self.country.id])
        self.assertEqual(trip.name, "test_trip")

        response = self.client.patch(
            f"/api/v1/trip/{trip.id}/",
            {
                "name": "test_trip_update",
            },
        )
        updated_trip = Trip.objects.first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_trip.name, "test_trip_update")

    def test_delete_trip(self):
        trip = Trip.objects.create(
            user=self.user,
            name="test_trip",
            currencies_rates=self.currency,
        )
        trip.countries.set([self.country.id])

        self.assertEqual(Trip.objects.count(), 1)

        response = self.client.delete(f"/api/v1/trip/{trip.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Trip.objects.count(), 0)


class TestListTrips(AuthenticateUserWithTokenMixin, TestCase):
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

    def test_list_trips(self):
        trip = Trip.objects.create(
            user=self.user,
            name="test_trip",
            currencies_rates=self.currency,
        )
        trip.countries.set([self.country.id])

        trip = Trip.objects.create(
            user=self.user,
            name="test_trip_2",
            currencies_rates=self.currency,
        )
        trip.countries.set([self.country.id])

        response = self.client.get("/api/v1/trip/")
        response_content = json.loads(response.content.decode("utf-8"))
        trips = Trip.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_content["trips"]), len(trips))

    def test_list_trips_statistics_total_trips_amount(self):
        trip = Trip.objects.create(
            user=self.user,
            name="test_trip",
            currencies_rates=self.currency,
        )
        trip.countries.set([self.country.id])

        trip = Trip.objects.create(
            user=self.user,
            name="test_trip_2",
            currencies_rates=self.currency,
        )
        trip.countries.set([self.country.id])

        response = self.client.get("/api/v1/trip/")
        response_content = json.loads(response.content.decode("utf-8"))
        statistics = response_content["statistics"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(statistics["total_trips_amount"], 2)

    def test_list_trips_statistics_visited_country_amount(self):
        self.country_1 = Country.objects.create(name="test_country_1")
        self.country_2 = Country.objects.create(name="test_country_2")
        self.country_3 = Country.objects.create(name="test_country_3")

        trip_1 = Trip.objects.create(
            user=self.user,
            name="test_trip",
            currencies_rates=self.currency,
        )
        trip_1.countries.set([self.country_1.id, self.country_2.id])

        trip_2 = Trip.objects.create(
            user=self.user,
            name="test_trip",
            currencies_rates=self.currency,
        )
        trip_2.countries.set([self.country_1.id])

        trip_3 = Trip.objects.create(
            user=self.user,
            name="test_trip",
            currencies_rates=self.currency,
        )
        trip_3.countries.set(
            [self.country_1.id, self.country_2.id, self.country_3.id]
        )

        response = self.client.get("/api/v1/trip/")
        response_content = json.loads(response.content.decode("utf-8"))
        statistics = response_content["statistics"]

        expected_result = 3

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            statistics["visited_countries_amount"], expected_result
        )
