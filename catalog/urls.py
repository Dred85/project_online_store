from django.urls import path


from catalog.views import home

urlpatterns = [
    path('', home),
]