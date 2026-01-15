# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserCreateView, UserRetrieveUpdateView
from .views import PasswordResetView, PasswordResetConfirmView

urlpatterns = [
    path('user/reset_password/', PasswordResetView.as_view(), name='reset-password'),
    path('user/reset_password_confirm/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/register/', UserCreateView.as_view(), name='user-register'),
    path('user/me/', UserRetrieveUpdateView.as_view(), name='user-me'),
]
