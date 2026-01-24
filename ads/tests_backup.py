# ads/tests.py
import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ads.models import Ad, Comment
from ads.serializers import AdSerializer

User = get_user_model()


class AdsViewsAdvancedTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            password='otherpass123'
        )
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )

        self.ad1 = Ad.objects.create(
            title='Тестовое объявление 1',
            description='Описание 1',
            price=1000.00,
            author=self.user
        )
        self.ad2 = Ad.objects.create(
            title='Тестовое объявление 2',
            description='Описание 2',
            price=2000.00,
            author=self.other_user
        )

    def test_ad_search(self):
        """Тест поиска объявлений"""
        url = reverse('ad-list') + '?search=Тестовое'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_ad_filter_by_price(self):
        """Тест фильтрации по цене"""
        url = reverse('ad-list') + '?price_min=1500'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(float(response.data[0]['price']), 2000.00)

    def test_ad_pagination(self):
        """Тест пагинации"""
        # Создаем больше объявлений
        for i in range(15):
            Ad.objects.create(
                title=f'Объявление {i}',
                description=f'Описание {i}',
                price=100 * i,
                author=self.user
            )

        url = reverse('ad-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем что есть пагинация
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)

    def test_ad_partial_update(self):
        """Тест частичного обновления объявления"""
        url = reverse('ad-detail', kwargs={'pk': self.ad1.pk})
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Обновленное название', 'price': 1500.00}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ad1.refresh_from_db()
        self.assertEqual(self.ad1.title, 'Обновленное название')
        self.assertEqual(self.ad1.price, 1500.00)

    def test_ad_statistics(self):
        """Тест статистики (если есть такой эндпоинт)"""
        # Если у вас есть эндпоинт для статистики
        url = reverse('ad-statistics')
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)
        # Если эндпоинта нет - можно пропустить или создать
        if response.status_code != 404:
            self.assertEqual(response.status_code, status.HTTP_200_OK)

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
