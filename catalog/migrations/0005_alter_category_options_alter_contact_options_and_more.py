# Generated by Django 5.0.6 on 2024-07-02 15:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0004_contact"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name": "Категория", "verbose_name_plural": "Категории"},
        ),
        migrations.AlterModelOptions(
            name="contact",
            options={"verbose_name": "Контакт", "verbose_name_plural": "Контакты"},
        ),
        migrations.AlterModelOptions(
            name="product",
            options={"verbose_name": "Продукт", "verbose_name_plural": "Продукты"},
        ),
    ]
