from django.shortcuts import render, redirect

from catalog.forms import ContactForm
from catalog.models import Product, Contact





def home(request):
    # Получение последних пяти товаров
    latest_products = Product.objects.order_by('-created_at')[:5]

    # Вывод последних пяти товаров в консоль
    for product in latest_products:
        print(product)

    return render(request, 'main/home.html', {'latest_products': latest_products})

def contacts(request):
    contact_info = Contact.objects.all()
    # return render(request, 'main/contacts.html', {'contact_info': contact_info})

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Перенаправление на страницу успеха после сохранения
    else:
        form = ContactForm()
    return render(request, 'main/contacts.html', {'form': form})