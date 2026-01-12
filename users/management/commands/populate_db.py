import random
from users.models import User
from catalog.models import Category, Product, Version, Contact

# Получаем администратора для владельца продуктов
owner = User.objects.filter(is_superuser=True).first()

if not owner:
    print("Нет суперпользователя, создайте сначала через createsuperuser")
    exit()

# ========================
# 1. Категории
# ========================
categories_data = [
    ("Ноутбуки", "Разные ноутбуки для работы и игр"),
    ("Смартфоны", "Современные смартфоны"),
    ("Аксессуары", "Чехлы, зарядки, наушники")
]

categories = []
for name, desc in categories_data:
    cat, _ = Category.objects.get_or_create(name=name, description=desc)
    categories.append(cat)

# ========================
# 2. Продукты
# ========================
products_data = [
    ("MacBook Pro 16", "Мощный ноутбук Apple", "Ноутбуки", 199999.99),
    ("Dell XPS 15", "Популярный ноутбук Dell", "Ноутбуки", 149999.99),
    ("iPhone 15", "Новый iPhone с M3 чипом", "Смартфоны", 99999.99),
    ("Galaxy S24", "Флагман Samsung", "Смартфоны", 89999.99),
    ("Беспроводные наушники", "Удобные наушники для музыки", "Аксессуары", 4999.99),
]

products = []
for name, desc, cat_name, price in products_data:
    category = next(c for c in categories if c.name == cat_name)
    prod, _ = Product.objects.get_or_create(
        name=name,
        description=desc,
        category=category,
        price=price,
        is_published=True,
        owner=owner,
    )
    products.append(prod)

# ========================
# 3. Версии продуктов
# ========================
for product in products:
    Version.objects.get_or_create(
        product=product,
        version_number="1.0",
        version_name=f"{product.name} Standard",
        is_current=True
    )
    Version.objects.get_or_create(
        product=product,
        version_number="2.0",
        version_name=f"{product.name} Pro",
        is_current=False
    )

# ========================
# 4. Контакты
# ========================
contacts_data = [
    ("Иван Иванов", "ivan@example.com", "+7 900 123 45 67", "Москва, ул. Ленина, 1", "Хочу узнать про продукты"),
    ("Петр Петров", "petr@example.com", "+7 901 234 56 78", "Санкт-Петербург, ул. Пушкина, 10", "Вопрос о доставке"),
]

for name, email, phone, address, message in contacts_data:
    Contact.objects.get_or_create(
        name=name,
        email=email,
        phone=phone,
        address=address,
        message=message
    )

print("База данных успешно заполнена тестовыми данными!")
