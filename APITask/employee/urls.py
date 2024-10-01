from django.urls import path
from .views import add, get

urlpatterns = [
    path('add/', add),
    path('get/', get),
]
