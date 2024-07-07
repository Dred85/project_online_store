import os

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from catalog.models import Product, Contact, Category

from django.urls import reverse_lazy

from catalog.forms import ContactForm, ProductForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
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
    context_object_name = 'product_list'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.kwargs.get('page', 1)
        per_page = self.kwargs.get('per_page', 10)
        product_list = Product.objects.all()
        paginator = Paginator(product_list, per_page)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context['product_list'] = products
        context['page'] = page
        context['per_page'] = per_page
        context['page_count'] = paginator.num_pages
        return context

    def get_queryset(self):
        per_page = self.kwargs.get('per_page', 10)
        product_list = Product.objects.all()
        paginator = Paginator(product_list, per_page)
        page = self.kwargs.get('page', 1)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        return products

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

class ProductPaginate2ListView(ListView):
    model = Product
    paginate_by = 2
    queryset = model.objects.all()  # Default: Model.objects.all()


class ProductPaginate3ListView(ListView):
    model = Product
    paginate_by = 3
    queryset = model.objects.all()  # Default: Model.objects.all()


