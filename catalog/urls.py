from django.urls import path

from catalog import views
from catalog.views import home, contacts

urlpatterns = [
    path('', home),
    path('contacts/', contacts,name='contacts'),

]