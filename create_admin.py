import os
import django
import sys

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from users.models import User

print("=" * 50)
print("СОЗДАНИЕ СУПЕРПОЛЬЗОВАТЕЛЯ")
print("=" * 50)

try:
    # Проверяем, существует ли уже пользователь
    if User.objects.filter(email='admin@example.com').exists():
        print("⚠️  Пользователь admin@example.com уже существует")
        admin = User.objects.get(email='admin@example.com')
        admin.set_password('admin123')
        admin.save()
        print("✅ Пароль обновлен: admin123")
    else:
        # Создаем суперпользователя
        admin = User.objects.create_superuser(
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            phone='+79991234567'
        )
        print("✅ Суперпользователь успешно создан")
    
    # Проверяем созданного пользователя
    admin = User.objects.get(email='admin@example.com')
    
    print("\nДАННЫЕ ПОЛЬЗОВАТЕЛЯ:")
    print("-" * 30)
    print(f"Email: {admin.email}")
    print(f"Пароль: admin123")
    print(f"Имя: {admin.first_name} {admin.last_name}")
    print(f"Телефон: {admin.phone}")
    print(f"Роль: {admin.role}")
    print(f"is_superuser: {admin.is_superuser}")
    print(f"is_staff: {admin.is_staff}")
    print(f"is_active: {admin.is_active}")
    
    # Создаем обычного пользователя
    if not User.objects.filter(email='user@example.com').exists():
        user = User.objects.create_user(
            email='user@example.com',
            password='user123',
            first_name='John',
            last_name='Doe',
            phone='+79998765432'
        )
        print("\n✅ Обычный пользователь создан:")
        print(f"   Email: user@example.com")
        print(f"   Пароль: user123")
    
    print("\n" + "=" * 50)
    print("ГОТОВО! Можно запускать сервер.")
    print("=" * 50)
    
except Exception as e:
    print(f"\n❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
