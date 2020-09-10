from django import forms
from django.contrib.auth.models import User
from .models import Genre, Book


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = "__all__"


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ["added_by", "available", ]

        widgets = {
            "genre": forms.CheckboxSelectMultiple(),
        }


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

        widgets = {
            'password': forms.PasswordInput(),
        }


class SigninForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
