from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_directory, name='book_directory'),
]