import json
from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Fill database with initial data from JSON fixtures"

    @staticmethod
    def json_read_categories():
        with open("fixtures/catalog_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return [item for item in data if item["model"] == "catalog.category"]

    @staticmethod
    def json_read_products():
        with open("fixtures/catalog_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return [item for item in data if item["model"] == "catalog.product"]

    def handle(self, *args, **options):
        # Удалите все продукты
        Product.objects.all().delete()
        # Удалите все категории
        Category.objects.all().delete()

        # Создайте списки для хранения объектов
        category_for_create = []
        product_for_create = []

        # Обходим все значения категорий из фикстуры для получения информации об одном объекте
        for category in Command.json_read_categories():
            category_fields = category["fields"]
            category_for_create.append(Category(id=category["pk"], **category_fields))

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фикстуры для получения информации об одном объекте
        for product in Command.json_read_products():
            product_fields = product["fields"]
            product_for_create.append(
                Product(
                    id=product["pk"],
                    category=Category.objects.get(pk=product_fields["category"]),
                    **{k: v for k, v in product_fields.items() if k != "category"},
                )
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)

        self.stdout.write(
            self.style.SUCCESS("Database has been filled with initial data.")
        )
