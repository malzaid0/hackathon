from django.contrib import admin
from .models import Genre, Book, BookBorrow

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(BookBorrow)