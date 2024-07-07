from django.urls import path

from catalog.apps import MainConfig
from .views import HomeView, ContactView, CatalogView, ProductDetailView, ProductCreateView

app_name = MainConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('catalog/<int:page>/<int:per_page>/', CatalogView.as_view(), name='catalog'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
]
