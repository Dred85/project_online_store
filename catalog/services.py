from django.core.cache import cache

from catalog.models import Category
from config import settings


def get_cached_category(recached: bool = False):
    if settings.CACHE_ENABLED:
        key = f'category_list'
        if recached:
            category_list = Category.objects.all()
            cache.set(key, category_list)
        else:
            category_list = cache.get(key)
            if category_list is None:
                category_list = Category.objects.all()
                cache.set(key, category_list)
    else:
        category_list = Category.objects.all()
    return category_list
