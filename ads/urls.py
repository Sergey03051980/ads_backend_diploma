# ads/urls.py
from django.urls import path
from .views import (
    AdListView,
    AdCreateView,
    AdDetailView,
    CommentListView,
    CommentDetailView,
)

urlpatterns = [
    path("ads/", AdListView.as_view(), name="ad-list"),
    path("ads/create/", AdCreateView.as_view(), name="ad-create"),
    path("ads/<int:pk>/", AdDetailView.as_view(), name="ad-detail"),
    path("ads/<int:ad_id>/comments/", CommentListView.as_view(), name="comment-list"),
    path(
        "ads/<int:ad_id>/comments/<int:pk>/",
        CommentDetailView.as_view(),
        name="comment-detail",
    ),
]
