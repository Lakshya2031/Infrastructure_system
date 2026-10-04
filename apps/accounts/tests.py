from django.test import TestCase
from django.urls import reverse

from .models import Role, User


class AccountsTestCase(TestCase):

    def setUp(self):

        self.citizen_role = Role.objects.create(
            name="Citizen",
            description="Citizen",
        )

        self.user = User.objects.create_user(
            username="testcitizen",
            email="citizen@test.com",
            password="TestPassword123",
            role=self.citizen_role,
        )

    def test_login_page_loads(self):

        response = self.client.get(
            reverse("accounts:login")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_register_page_loads(self):

        response = self.client.get(
            reverse("accounts:register")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_login_works(self):

        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "testcitizen",
                "password": "TestPassword123",
            },
        )

        self.assertRedirects(
            response,
            reverse("accounts:dashboard"),
        )

    def test_dashboard_requires_login(self):

        response = self.client.get(
            reverse("accounts:dashboard")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_authenticated_user_can_access_dashboard(self):

        self.client.login(
            username="testcitizen",
            password="TestPassword123",
        )

        response = self.client.get(
            reverse("accounts:dashboard")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Citizen Dashboard",
        )

    def test_user_has_correct_role(self):

        self.assertEqual(
            self.user.role.name,
            "Citizen",
        )

    def test_has_role_method(self):

        self.assertTrue(
            self.user.has_role("Citizen")
        )

        self.assertFalse(
            self.user.has_role("Inspector")
        )