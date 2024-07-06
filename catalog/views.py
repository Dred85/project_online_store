from django.shortcuts import render, redirect

from catalog.forms import ContactForm
from catalog.models import Product, Contact, Category


def home(request):
    # Получение категорий
    list_category = Category.objects.order_by('name')

    latest_products = Product.objects.order_by('-created_at')[:5]

    # Вывод последних пяти товаров в консоль
    for product in latest_products:
        print(product)

    return render(request, 'main/home.html', {'latest_products': latest_products, 'list_category': list_category})


def contacts(request):
    contact_info = Contact.objects.all()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contacts')
    return render(request, 'main/contacts.html', {'contact_info': contact_info})


def products(request):
    contact_info = Contact.objects.all()

    return render(request, 'main/products.html', {'contact_info': contact_info})
