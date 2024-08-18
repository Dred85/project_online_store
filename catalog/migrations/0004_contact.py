# Generated by Django 5.0.6 on 2024-07-01 19:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0003_remove_product_manufactured_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=20)),
                ("address", models.TextField()),
                ("message", models.TextField()),
            ],
            options={
                "verbose_name": "Contact",
                "verbose_name_plural": "Contacts",
            },
        ),
    ]
