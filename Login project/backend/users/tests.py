import json
from base64 import urlsafe_b64decode

from django.contrib.auth import get_user_model
from django.test import TestCase


class LoginViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="user@example.com",
            password="secret123",
        )

    def decode_payload(self, token):
        _, payload, _ = token.split(".")
        payload += "=" * (-len(payload) % 4)
        return json.loads(urlsafe_b64decode(payload.encode("ascii")).decode("utf-8"))

    def test_login_succeeds_with_email_and_password(self):
        response = self.client.post(
            "/api/login/",
            data=json.dumps({"email": "user@example.com", "password": "secret123"}),
            content_type="application/json",
        )
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["message"], "Login successful")
        self.assertEqual(
            response_data["user"],
            {
                "id": "4e4dd113-1c54-49b8-90b9-513a8eaffffd",
                "name": "testuser",
                "email": "user@example.com",
                "role": "admin",
                "role_display": "Admin",
                "company_id": "619fdc4b-1a67-4547-96d1-4dcbdf2a4f10",
                "company_name": "JMS Advisory Services Pvt Ltd",
            },
        )
        self.assertIsInstance(response_data["refresh"], str)
        self.assertIsInstance(response_data["access"], str)

        refresh_payload = self.decode_payload(response_data["refresh"])
        access_payload = self.decode_payload(response_data["access"])

        self.assertEqual(refresh_payload["token_type"], "refresh")
        self.assertEqual(access_payload["token_type"], "access")
        self.assertEqual(refresh_payload["user_id"], "4e4dd113-1c54-49b8-90b9-513a8eaffffd")
        self.assertEqual(access_payload["user_id"], "4e4dd113-1c54-49b8-90b9-513a8eaffffd")
        self.assertEqual(refresh_payload["name"], "testuser")
        self.assertEqual(access_payload["name"], "testuser")
        self.assertEqual(self.client.session.get("_auth_user_id"), str(self.user.pk))

    def test_login_also_accepts_request_without_trailing_slash(self):
        response = self.client.post(
            "/api/login",
            data=json.dumps({"email": "user@example.com", "password": "secret123"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Login successful")

    def test_login_requires_email_and_password(self):
        response = self.client.post(
            "/api/login/",
            data=json.dumps({"email": "", "password": ""}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "Email and password are required."})

    def test_login_rejects_invalid_credentials(self):
        response = self.client.post(
            "/api/login/",
            data=json.dumps({"email": "user@example.com", "password": "wrong-password"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message": "Invalid email or password."})

    def test_login_rejects_non_post_requests(self):
        response = self.client.get("/api/login/")

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {"message": "Only POST requests are allowed."})