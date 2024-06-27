from django.urls import path


from catalog.views import home, contacts, success_view

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('success/', success_view, name='success'),
]