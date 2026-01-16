# ads/tests.py
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from ads.models import Ad, Comment

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    return User.objects.create_superuser(
        email="admin@test.com",
        password="testpass123",
        first_name="Admin",
        last_name="User",
        phone="+79991112233",
    )


@pytest.fixture
def regular_user():
    return User.objects.create_user(
        email="user@test.com",
        password="testpass123",
        first_name="John",
        last_name="Doe",
        phone="+79992223344",
    )


@pytest.fixture
def ad(admin_user):
    return Ad.objects.create(
        title="Test Ad", price=1000, description="Test description", author=admin_user
    )


@pytest.mark.django_db
class TestAdsAPI:
    def test_list_ads_unauthorized(self, api_client, ad):
        response = api_client.get("/api/ads/")
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) == 1

    def test_create_ad_authenticated(self, api_client, regular_user):
        api_client.force_authenticate(user=regular_user)
        data = {"title": "New Ad", "price": 2000, "description": "New description"}
        response = api_client.post("/api/ads/create/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Ad.objects.count() == 1
        assert Ad.objects.first().title == "New Ad"

    def test_search_ads(self, api_client, ad):
        response = api_client.get("/api/ads/?search=Test")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_pagination(self, api_client):
        # Создаем 5 объявлений для теста пагинации
        user = User.objects.create_user(
            email="test@test.com",
            password="testpass",
            first_name="Test",
            last_name="User",
            phone="+79993334455",
        )
        for i in range(5):
            Ad.objects.create(
                title=f"Ad {i}",
                price=100 * i,
                description=f"Description {i}",
                author=user,
            )

        response = api_client.get("/api/ads/")
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) == 4  # PAGE_SIZE = 4

    def test_update_ad_author(self, api_client, regular_user, ad):
        # Меняем автора объявления
        ad.author = regular_user
        ad.save()

        api_client.force_authenticate(user=regular_user)
        data = {"title": "Updated Title"}
        response = api_client.patch(f"/api/ads/{ad.id}/", data)
        assert response.status_code == status.HTTP_200_OK
        ad.refresh_from_db()
        assert ad.title == "Updated Title"

    def test_delete_ad_admin(self, api_client, admin_user, ad):
        api_client.force_authenticate(user=admin_user)
        response = api_client.delete(f"/api/ads/{ad.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Ad.objects.count() == 0


@pytest.mark.django_db
class TestCommentsAPI:
    def test_create_comment(self, api_client, regular_user, ad):
        api_client.force_authenticate(user=regular_user)
        data = {"text": "Test comment"}
        response = api_client.post(f"/api/ads/{ad.id}/comments/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.objects.count() == 1
        assert Comment.objects.first().text == "Test comment"
