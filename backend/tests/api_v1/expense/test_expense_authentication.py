from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


User = get_user_model()


class TestCRUDExpenseWithUnauthenticatedUser(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_expense(self):
        response = self.client.post(f"/api/v1/trip/1/expense/")

        self.assertEqual(response.status_code, 401)

    def test_read_expense(self):
        response = self.client.get("/api/v1/trip/1/expense/1/")

        self.assertEqual(response.status_code, 401)

    def test_update_expense(self):
        response = self.client.put("/api/v1/trip/1/expense/1/")

        self.assertEqual(response.status_code, 401)

    def test_delete_expense(self):
        response = self.client.delete("/api/v1/trip/1/expense/1/")

        self.assertEqual(response.status_code, 401)
