from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='product_images/', verbose_name='Изображение')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')

    owner = models.ForeignKey(User, verbose_name="владелец", help_text="Укажите владельца продукта", blank=True,
                              null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        permissions = [
            ("can_edit_description", "can_edit_description"),
            ("can_edit_category", "can_edit_category"),
            ("can_edit_publish", "can_edit_publish")
        ]

    def __str__(self):
        return self.name


class Contact(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Version(models.Model):
    product = models.ForeignKey(Product, related_name='versions', on_delete=models.CASCADE)
    version_number = models.CharField(max_length=50)
    version_name = models.CharField(max_length=100)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - {self.version_name} ({self.version_number})"

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
