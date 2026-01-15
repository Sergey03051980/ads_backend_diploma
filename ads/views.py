from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ad, Comment
from .serializers import AdSerializer, CommentSerializer
from .permissions import IsAuthorOrAdmin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

class AdListView(generics.ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description']
    permission_classes = [IsAuthenticatedOrReadOnly]

class AdCreateView(generics.CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class AdDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrAdmin]

class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Исправление для Swagger
        if getattr(self, 'swagger_fake_view', False):
            return Comment.objects.none()
        ad_id = self.kwargs['ad_id']
        return Comment.objects.filter(ad_id=ad_id)

    def perform_create(self, serializer):
        ad_id = self.kwargs['ad_id']
        ad = generics.get_object_or_404(Ad, id=ad_id)
        serializer.save(author=self.request.user, ad=ad)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrAdmin]

    def get_queryset(self):
        # Исправление для Swagger
        if getattr(self, 'swagger_fake_view', False):
            return Comment.objects.none()
        ad_id = self.kwargs['ad_id']
        return Comment.objects.filter(ad_id=ad_id, id=self.kwargs['pk'])
