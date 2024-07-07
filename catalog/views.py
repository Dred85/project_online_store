import os
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404


from catalog.models import Product, Contact, Category
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from catalog.models import Contact
from catalog.forms import ContactForm, ProductForm


class HomeView(ListView):
    model = Product
    template_name = 'main/home.html'
    context_object_name = 'latest_products'
    queryset = Product.objects.order_by('-created_at')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_category'] = Category.objects.order_by('name')
        context['list_products'] = Product.objects.all()
        context['nums'] = [2, 3]
        return context


class ContactView(CreateView):
    model = Contact
    template_name = 'main/contacts.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = Contact.objects.all()
        return context

class CatalogView(ListView):
    model = Product
    template_name = 'main/per_page.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.kwargs.get('page', 1)
        per_page = self.kwargs.get('per_page', 10)
        len_product = Product.objects.count()

        if len_product % per_page != 0:
            page_count = [x + 1 for x in range((len_product // per_page) + 1)]
        else:
            page_count = [x + 1 for x in range((len_product // per_page))]

        context['page'] = page
        context['per_page'] = per_page
        context['page_count'] = page_count
        return context

    def get_queryset(self):
        page = self.kwargs.get('page', 1)
        per_page = self.kwargs.get('per_page', 10)
        return Product.objects.all()[per_page * (page - 1): per_page * page]


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagination'] = bool(self.kwargs.get('per_page'))
        context['per_page'] = self.kwargs.get('per_page')
        context['page'] = self.kwargs.get('page')
        return context


def handle_uploaded_file(f, difference_between_files):
    if os.path.exists(os.path.join("product_images", f.name)):
        filename = difference_between_files + f.name
        print(f"file exists! f.name = {f.name}, new={filename}")
    else:
        filename = f.name

    with open(os.path.join("media/product_images", filename), "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return f'product_images/{filename}'


class ProductCreateView(CreateView):
    model = Product
    template_name = 'main/create_product.html'
    form_class = ProductForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        number = Product.objects.count()
        if number > 5:
            products_list = Product.objects.all()[number - 5:number]
        else:
            products_list = Product.objects.all()
        context['object_list'] = products_list
        context['category_list'] = Category.objects.all()
        context['title'] = 'Добавить продукт'
        return context