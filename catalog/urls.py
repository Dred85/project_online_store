from django.urls import path

from catalog.apps import MainConfig
from .views import HomeView, ContactView, CatalogView, ProductDetailView, ProductCreateView, ProductPaginate2ListView, \
    ProductPaginate3ListView, ProductCreateView, BlogPostListView, BlogPostDetailView, BlogPostCreateView, \
    BlogPostUpdateView, BlogPostDeleteView

app_name = MainConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path(
        "home/paginate_by_2/",
        ProductPaginate2ListView.as_view(),
        name="home_paginate_by_2",
    ),
    path(
        "home/paginate_by_3/",
        ProductPaginate3ListView.as_view(),
        name="home_paginate_by_3",
    ),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('catalog/<int:page>/<int:per_page>/', CatalogView.as_view(), name='catalog'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='create_product'),


]
