from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class VerySimpleTest(TestCase):
    def test_1(self):
        user = User.objects.create_user(email='test1@example.com', password='pass')
        self.assertEqual(user.email, 'test1@example.com')
    
    def test_2(self):
        user = User.objects.create_user(email='test2@example.com', password='pass')
        self.assertTrue(user.check_password('pass'))
    
    def test_3(self):
        user = User.objects.create_superuser(email='admin@example.com', password='admin')
        self.assertTrue(user.is_superuser)
    
    def test_4(self):
        from ads.models import Ad
        user = User.objects.create_user(email='author@example.com', password='pass')
        ad = Ad.objects.create(title='Test', description='Desc', price=100, author=user)
        self.assertEqual(ad.title, 'Test')
    
    def test_5(self):
        from ads.models import Ad, Comment
        user = User.objects.create_user(email='commenter@example.com', password='pass')
        ad = Ad.objects.create(title='Ad', description='Desc', price=100, author=user)
        comment = Comment.objects.create(ad=ad, author=user, text='Comment')
        self.assertEqual(comment.text, 'Comment')
