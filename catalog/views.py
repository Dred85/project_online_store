import os

from catalog.models import Product, Contact, Category, Version

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory

from catalog.forms import ContactForm, ProductForm, ProductVersionForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


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


class ProductListView(ListView):
    model = Product
    template_name = 'main/product_list.html'
    paginate_by = 3

    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        # Получаем контекст из родительского класса
        context = super().get_context_data(**kwargs)
        # Получаем все продукты
        products = context['products']
        # Создаем словарь для хранения текущих версий
        current_versions = {}
        # Ищем текущую версию для каждого продукта
        for product in products:
            current_version = Version.objects.filter(product=product, is_current=True).first()
            current_versions[product.id] = current_version
        # Добавляем текущие версии в контекст
        context['current_versions'] = current_versions
        return context




class ProductCreateView(CreateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    template_name = 'main/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    # def form_valid(self, form):
    #     product = form.save()
    #     user = self.request.user
    #     product.owner = user
    #     product.save()
    #     return super().form_valid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)

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


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'main/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, form=ProductVersionForm, extra=1)
        if self.request.method == 'POST':
            context_data["formset"] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)

        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'main/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')


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
    paginate_by = 3
    model = Product
    template_name = 'main/per_page.html'
    context_object_name = 'products_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = self.kwargs.get('page', 1)
        context['per_page'] = self.get_paginate_by(self.get_queryset())
        context['page_count'] = self.paginate_by
        return context


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
    """Функция обработки загруженных файлов"""
    if os.path.exists(os.path.join("product_images", f.name)):
        filename = difference_between_files + f.name
        print(f"file exists! f.name = {f.name}, new={filename}")
    else:
        filename = f.name

    with open(os.path.join("media/product_images", filename), "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return f'product_images/{filename}'
