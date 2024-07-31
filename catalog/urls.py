from django.urls import path

from catalog.apps import MainConfig
from .views import (HomeView, ContactView, CatalogView, ProductDetailView, ProductCreateView,
                    ProductListView, ProductUpdateView, ProductDeleteView)

app_name = MainConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product_list', ProductListView.as_view(), name='product_list'),
    path('view/<int:pk>/', ProductDetailView.as_view(), name='view_product'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),

    path('contacts/', ContactView.as_view(), name='contacts'),
    path('catalog/<int:page>/<int:per_page>/', CatalogView.as_view(), name='catalog'),

]
