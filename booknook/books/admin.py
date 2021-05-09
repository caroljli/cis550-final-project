from django.contrib import admin
from books.models import Book, BestBook, BookFollowers

# Register your models here.

admin.site.register(Book)
admin.site.register(BestBook)
admin.site.register(BookFollowers)
