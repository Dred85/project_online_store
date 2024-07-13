from django.urls import path

from catalog.apps import MainConfig
from .views import HomeView, ContactView, CatalogView, ProductDetailView, ProductCreateView, ProductPaginate2ListView, \
    ProductPaginate3ListView, ProductCreateView, ProductListView, ProductUpdateView, ProductDeleteView

app_name = MainConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products_list', ProductListView.as_view(), name="products_list"),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name="update_products"),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name="delete_product"),

    path('contacts/', ContactView.as_view(), name='contacts'),
    path('catalog/<int:page>/<int:per_page>/', CatalogView.as_view(), name='catalog'),

]
