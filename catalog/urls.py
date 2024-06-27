from django.urls import path


from catalog.views import home, contacts, contact_view

urlpatterns = [
    path('', home),
    path('contacts/', contacts),
]