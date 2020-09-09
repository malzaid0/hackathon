from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import datetime


class Genre(models.Model):
    name = models.CharField(max_length=50)


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    release_year = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(datetime.datetime.now().year), MinValueValidator(500)])
    isbn = models.PositiveBigIntegerField()
    genre = models.ManyToManyField(Genre)
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    img = models.ImageField()
