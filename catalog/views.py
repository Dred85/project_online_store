import os
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404

from catalog.forms import ContactForm
from catalog.models import Product, Contact, Category


def home(request):
    # Получение категорий
    list_category = Category.objects.order_by('name')
    list_products = Product.objects.all()
    latest_products = Product.objects.order_by('-created_at')[:5]

    # Вывод последних пяти товаров в консоль
    for product in latest_products:
        print(product)

    return render(request, 'main/home.html', {
        'latest_products': latest_products,
        'list_category': list_category,
        'list_products': list_products,
        'nums': [2, 3]
    })


def contacts(request):
    contact_info = Contact.objects.all()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contacts')
    else:
        form = ContactForm()  # Инициализация формы для GET-запроса

    return render(request, 'main/contacts.html', {
        'contact_info': contact_info,
        'form': form  # Передаем форму в контекст
    })


def catalog(request, page, per_page):
    len_product = Product.objects.count()  # Используем count() для оптимизации
    if len_product % per_page != 0:
        page_count = [x + 1 for x in range((len_product // per_page) + 1)]
    else:
        page_count = [x + 1 for x in range((len_product // per_page))]

    product_list = Product.objects.all()[per_page * (page - 1): per_page * page]

    context = {
        "product_list": product_list,
        "page": page,
        "per_page": per_page,
        "page_count": page_count
    }

    return render(request, 'main/per_page.html', context)


def product_detail(request, pk, page=None, per_page=None):
    _object = get_object_or_404(Product, pk=pk)
    context = {
        "object": _object,
        "pagination": bool(per_page),
        "per_page": per_page,
        "page": page
    }

    return render(request, 'main/product_detail.html', context)


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


def create(request):
    """
       Product
       - Наименование name
       - Описание description
       - Изображение (превью) image
       - Категория category
       - Цена за покупку price
       - Дата создания (записи в БД) created_at
       - Дата последнего изменения (записи в БД) updated_at
    """

    number = Product.objects.count()
    if number > 5:
        products_list = Product.objects.all()[number - 5:number]
    else:
        products_list = Product.objects.all()

    category_list = Category.objects.all()

    context = {
        'object_list': products_list,
        'category_list': category_list,
        'title': 'Добавить продукт',
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')  # Получаем файл изображения из запроса

        time_of_creation = datetime.now().strftime('%Y-%m-%d')

        try:
            image_path = handle_uploaded_file(image, f"{time_of_creation}_{name}_")
        except KeyError:
            print("Отсутствует изображение")
            image_path = None

        info = {
            'created_at': time_of_creation,
            'updated_at': time_of_creation,
            'name': name,
            'price': price,
            'description': description,
            'category': Category.objects.get(id=category_id),
            'image': image_path
        }

        print(info)
        Product.objects.create(**info)

    return render(request, 'main/create_product.html', context)
