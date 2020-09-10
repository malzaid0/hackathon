from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
import datetime


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    release_year = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(datetime.datetime.now().year), MinValueValidator(500)])
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.ManyToManyField(Genre)
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    img = models.ImageField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'book_id': self.id})


class BookBorrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    borrow_time = models.DateTimeField(auto_now_add=True)
    return_time = models.DateTimeField(null=True, blank=True)
