from django.contrib import admin
from .models import Genre, Book, BookBorrow
# Register your models here.
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(BookBorrow)