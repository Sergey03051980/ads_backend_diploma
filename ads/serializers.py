# ads/serializers.py
from rest_framework import serializers
from .models import Ad, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'ad', 'created_at')
        read_only_fields = ('author', 'ad', 'created_at')


class AdSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Ad
        fields = ('id', 'title', 'price', 'description', 'author', 'image', 'created_at', 'comments')
        read_only_fields = ('author', 'created_at', 'comments')
