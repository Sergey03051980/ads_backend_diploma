# users/tests.py
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserAPI:
    def test_register_user(self):
        client = APIClient()
        data = {
            "email": "newuser@test.com",
            "password": "TestPass123",
            "first_name": "New",
            "last_name": "User",
            "phone": "+79998887766",
        }
        response = client.post("/api/user/register/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="newuser@test.com").exists()

    def test_get_jwt_token(self):
        client = APIClient()
        user = User.objects.create_user(
            email="test@test.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            phone="+79991112233",
        )

        data = {"email": "test@test.com", "password": "testpass123"}
        response = client.post("/api/token/", data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_refresh_token(self):
        client = APIClient()
        user = User.objects.create_user(
            email="test@test.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            phone="+79991112233",
        )

        # Получаем токен
        token_response = client.post(
            "/api/token/", {"email": "test@test.com", "password": "testpass123"}
        )
        refresh_token = token_response.data["refresh"]

        # Обновляем токен
        refresh_response = client.post(
            "/api/token/refresh/", {"refresh": refresh_token}
        )
        assert refresh_response.status_code == status.HTTP_200_OK
        assert "access" in refresh_response.data

    def test_get_user_profile(self):
        client = APIClient()
        user = User.objects.create_user(
            email="test@test.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            phone="+79991112233",
        )

        client.force_authenticate(user=user)
        response = client.get("/api/user/me/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == "test@test.com"
