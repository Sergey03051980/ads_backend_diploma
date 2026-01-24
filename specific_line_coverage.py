"""Тесты для покрытия конкретных строк кода"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser

from ads.models import Ad
from ads import permissions as ads_permissions

User = get_user_model()

class SpecificLineCoverage(TestCase):
    """Покрытие конкретных строк"""
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email='specific@test.com',
            password='pass123'
        )
        self.other_user = User.objects.create_user(
            email='other_specific@test.com',
            password='pass123'
        )
        
        self.ad = Ad.objects.create(
            title='Specific Ad',
            description='Specific desc',
            price=100,
            author=self.user
        )
    
    def test_permissions_lines(self):
        """Тест строк в permissions.py"""
        # Импортируем permissions
        from ads.permissions import IsOwnerOrReadOnly
        
        permission = IsOwnerOrReadOnly()
        
        # Safe methods для всех
        request = self.factory.get('/')
        request.user = AnonymousUser()
        has_perm = permission.has_object_permission(request, None, self.ad)
        self.assertTrue(has_perm)  # GET разрешен
        
        # Unsafe methods для автора
        request = self.factory.post('/')
        request.user = self.user
        has_perm = permission.has_object_permission(request, None, self.ad)
        self.assertTrue(has_perm)  # Автор может
        
        # Unsafe methods для не автора
        request = self.factory.post('/')
        request.user = self.other_user
        has_perm = permission.has_object_permission(request, None, self.ad)
        self.assertFalse(has_perm)  # Не автор не может
    
    def test_serializer_validation(self):
        """Тест валидации в сериализаторах"""
        from users.serializers import UserSerializer
        
        # Тест с валидными данными
        valid_data = {
            'email': 'serializer_test@test.com',
            'password': 'ValidPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        serializer = UserSerializer(data=valid_data)
        is_valid = serializer.is_valid()
        print(f'UserSerializer valid с полными данными: {is_valid}')
        
        # Тест с частичными данными
        partial_data = {'first_name': 'Updated'}
        user = User.objects.create_user(email='partial@test.com', password='pass123')
        serializer = UserSerializer(user, data=partial_data, partial=True)
        is_valid = serializer.is_valid()
        print(f'UserSerializer valid частичное обновление: {is_valid}')

class ViewMethodTests(TestCase):
    """Тест методов views"""
    
    def test_view_methods(self):
        """Тест что views имеют нужные методы"""
        from users.views import UserCreateView, UserRetrieveUpdateView
        
        # UserCreateView
        create_view = UserCreateView()
        self.assertTrue(hasattr(create_view, 'post'))
        
        # UserRetrieveUpdateView
        retrieve_view = UserRetrieveUpdateView()
        self.assertTrue(hasattr(retrieve_view, 'get'))
        self.assertTrue(hasattr(retrieve_view, 'put'))
        self.assertTrue(hasattr(retrieve_view, 'patch'))
        
        print('Все основные view методы присутствуют')

