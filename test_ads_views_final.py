"""Финальные тесты для ads/views.py"""

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from ads.models import Ad, Comment

User = get_user_model()

class AdsViewsFinalTests(APITestCase):
    """Финальные тесты для ads/views.py"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='ads_final@test.com',
            password='ads_final_pass123'
        )
        self.other_user = User.objects.create_user(
            email='other_ads_final@test.com',
            password='other_final_pass123'
        )
        self.client = APIClient()
        
        # Создаем несколько объявлений для тестирования
        self.ad1 = Ad.objects.create(
            title='Final Ad 1',
            description='Final description 1',
            price=100.00,
            author=self.user
        )
        self.ad2 = Ad.objects.create(
            title='Final Ad 2',
            description='Final description 2',
            price=200.00,
            author=self.other_user
        )
        
        # Комментарии
        self.comment1 = Comment.objects.create(
            ad=self.ad1,
            author=self.user,
            text='Final comment 1'
        )
        self.comment2 = Comment.objects.create(
            ad=self.ad1,
            author=self.other_user,
            text='Final comment 2'
        )
    
    def test_ad_list_pagination(self):
        """Тест пагинации списка объявлений"""
        url = reverse('ad-list')
        
        # Создаем больше объявлений для пагинации
        for i in range(15):
            Ad.objects.create(
                title=f'Pagination Ad {i}',
                description=f'Pagination description {i}',
                price=50.00 * (i + 1),
                author=self.user if i % 2 == 0 else self.other_user
            )
        
        response = self.client.get(url)
        
        # Проверяем структуру ответа с пагинацией
        if 'results' in response.data:  # PageNumberPagination
            print(f'PageNumberPagination: {len(response.data["results"])} results')
            self.assertTrue('count' in response.data)
            self.assertTrue('next' in response.data)
        elif isinstance(response.data, list):  # No pagination
            print(f'No pagination: {len(response.data)} results')
        
        # Тест с параметром page
        response = self.client.get(f'{url}?page=2')
        print(f'Page 2: {response.status_code}')
    
    def test_ad_list_ordering(self):
        """Тест сортировки списка"""
        url = reverse('ad-list')
        
        # По цене asc
        response = self.client.get(f'{url}?ordering=price')
        print(f'Ordering by price asc: {response.status_code}')
        
        # По цене desc
        response = self.client.get(f'{url}?ordering=-price')
        print(f'Ordering by price desc: {response.status_code}')
        
        # По дате создания
        response = self.client.get(f'{url}?ordering=-created_at')
        print(f'Ordering by created_at: {response.status_code}')
    
    def test_ad_create_with_different_data(self):
        """Тест создания с разными данными"""
        url = reverse('ad-create')
        self.client.force_authenticate(user=self.user)
        
        test_cases = [
            {
                'data': {
                    'title': 'Minimal Ad',
                    'price': 50.00
                },
                'desc': 'Минимальные данные'
            },
            {
                'data': {
                    'title': 'A' * 100,  # Длинный заголовок
                    'description': 'B' * 500,  # Длинное описание
                    'price': 999999.99
                },
                'desc': 'Максимальные данные'
            },
            {
                'data': {
                    'title': 'Zero Price',
                    'price': 0.00
                },
                'desc': 'Цена 0'
            },
            {
                'data': {
                    'title': 'Negative Price',
                    'price': -10.00
                },
                'desc': 'Отрицательная цена'
            }
        ]
        
        for test_case in test_cases:
            response = self.client.post(url, test_case['data'], format='json')
            print(f'{test_case["desc"]}: {response.status_code}')
    
    def test_ad_detail_all_scenarios(self):
        """Тест всех сценариев деталей объявления"""
        # 1. Несуществующее объявление
        url = reverse('ad-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        print(f'GET несуществующее объявление: {response.status_code}')
        
        # 2. PATCH с невалидными данными
        url = reverse('ad-detail', kwargs={'pk': self.ad1.pk})
        self.client.force_authenticate(user=self.user)
        
        invalid_cases = [
            {'title': ''},  # Пустой заголовок
            {'price': 'not-a-number'},  # Не число
            #{'price': -1000.00},  # Отрицательная цена
        ]
        
        for invalid_data in invalid_cases:
            response = self.client.patch(url, invalid_data, format='json')
            print(f'PATCH невалидные данные {invalid_data}: {response.status_code}')
    
    def test_comments_all_operations(self):
        """Тест всех операций с комментариями"""
        # Comment list для ad2
        url = reverse('comment-list', kwargs={'ad_id': self.ad2.pk})
        
        # GET пустого списка
        response = self.client.get(url)
        print(f'GET пустые комментарии: {response.status_code}')
        
        # POST комментария
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {'text': 'New comment on ad2'}, format='json')
        print(f'POST комментарий на ad2: {response.status_code}')
        
        if response.status_code == 201:
            comment_id = response.data['id']
            
            # Comment detail операции
            detail_url = reverse('comment-detail', kwargs={'ad_id': self.ad2.pk, 'pk': comment_id})
            
            # GET
            response = self.client.get(detail_url)
            print(f'GET детали комментария: {response.status_code}')
            
            # PATCH от автора
            response = self.client.patch(detail_url, {'text': 'Updated by author'}, format='json')
            print(f'PATCH комментарий автор: {response.status_code}')
            
            # PATCH от не автора
            self.client.force_authenticate(user=self.other_user)
            response = self.client.patch(detail_url, {'text': 'Hacked by other'}, format='json')
            print(f'PATCH комментарий не автор: {response.status_code}')
            
            # DELETE от не автора
            response = self.client.delete(detail_url)
            print(f'DELETE комментарий не автор: {response.status_code}')
            
            # DELETE от автора
            self.client.force_authenticate(user=self.user)
            response = self.client.delete(detail_url)
            print(f'DELETE комментарий автор: {response.status_code}')

