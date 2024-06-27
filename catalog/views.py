from django.shortcuts import render, redirect

from catalog.forms import ContactForm


def home(request):
    return render(request, 'main/home.html')


def contacts(request):
    # if request.method == 'POST':
    #     name = request.POST.get('name')
    #     phone = request.POST.get('phone')
    #     message = request.POST.get('message')
    #     print(f"{name} ({phone}): {message}")

    return render(request, 'main/contacts.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # name = request.POST.get('name')
        # phone = request.POST.get('phone')
        # message = request.POST.get('message')
        # print(f"{name} ({phone}): {message}")
        if form.is_valid():
            form.save()
            return redirect('success')  # Перенаправление на страницу успеха после сохранения
    else:
        form = ContactForm()
    return render(request, 'main/contact_form.html', {'form': form})

# def success_view(request):
#     return render(request, 'main/success.html')