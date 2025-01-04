from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


User = get_user_model()


class TestCRUDTripWithUnauthenticatedUser(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_trip(self):
        response = self.client.post("/api/v1/trip/")

        self.assertEqual(response.status_code, 401)

    def test_read_trip(self):
        response = self.client.get("/api/v1/trip/1/")

        self.assertEqual(response.status_code, 401)

    def test_update_trip(self):
        response = self.client.put("/api/v1/trip/1/")

        self.assertEqual(response.status_code, 401)

    def test_delete_trip(self):
        response = self.client.delete("/api/v1/trip/1/")

        self.assertEqual(response.status_code, 401)


class TestCostPerCategoryTripWithUnauthenticatedUser(TestCase):
    def test_get_cost_per_category(self):
        response = self.client.get(f"/api/v1/trip/1/get_cost_per_category/")
        self.assertEqual(response.status_code, 401)
