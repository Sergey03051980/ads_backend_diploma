# ads/permissions.py
from rest_framework import permissions

class IsAuthorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешаем чтение всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешаем изменение/удаление только автору или админу
        return obj.author == request.user or request.user.is_superuser or request.user.role == 'admin'
