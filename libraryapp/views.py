from django.shortcuts import render, redirect
from .forms import SignupForm, SigninForm, BookForm, GenreForm
from django.contrib.auth import login, authenticate, logout
from .models import Book, Genre, BookBorrow
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.mail import send_mail
import datetime

"""
BOOK
"""


def book_list(request):
    if not request.user.is_authenticated:
        return redirect("no-access")
    books = Book.objects.all()
    query = request.GET.get('search_term')
    if query:
        books = books.filter(
            Q(name__icontains=query) |
            Q(isbn__icontains=query) |
            Q(genre__name__icontains=query)
        ).distinct()
    context = {
        "books": books
    }
    return render(request, 'book_list.html', context)


def book_detail(request, book_id):
    if not request.user.is_authenticated:
        return redirect("no-access")
    book = Book.objects.get(id=book_id)
    genres = Genre.objects.filter(book=book)
    borrows = BookBorrow.objects.filter(book=book)
    current_borrow = borrows.filter(return_time=None)
    context = {
        "book": book,
        "genres": genres,
        "borrows": borrows,
        "current_borrow": current_borrow,
    }
    return render(request, 'book_detail.html', context)


def create_book(request):
    if not request.user.is_staff:
        return redirect("no-access")
    form = BookForm()
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user
            book.save()
            form.save_m2m()
            return redirect('book-list')
    context = {
        "form": form,
    }
    return render(request, 'create_book.html', context)


def book_delete(request, book_id):
    if not request.user.is_staff:
        return redirect("no-access")
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('book-list')


############################################################################

"""
PROFILE
"""


def profile_detail(request, user_id):
    user = User.objects.get(id=user_id)
    if not request.user == user:
        return redirect("no-access")
    borrows = BookBorrow.objects.filter(user=user)
    current_borrow = borrows.filter(return_time=None)
    context = {
        "user": user,
        "borrows": borrows,
        "current_borrow": current_borrow,
    }
    return render(request, 'profile.html', context)


############################################################################

"""
BORROW AND RETURN
"""


def borrow_book(request, book_id):
    if not request.user.is_authenticated:
        return redirect("no-access")
    book = Book.objects.get(id=book_id)
    if not book.available:
        return redirect("no-access")
    borrow = BookBorrow(book=book, user=request.user)
    borrow.save()
    book.available = False
    book.save()
    return redirect(book)


def borrow_book_to_user(request, book_id, user_id):
    if not request.user.is_staff:
        return redirect("no-access")
    book = Book.objects.get(id=book_id)
    if not book.available:
        return redirect("no-access")
    user = User.objects.get(id=user_id)
    borrow = BookBorrow(book=book, user=user)
    borrow.save()
    book.available = False
    book.save()
    return redirect(book)


def user_list(request, book_id):
    if not request.user.is_staff:
        return redirect("no-access")
    users = User.objects.all()
    query = request.GET.get('search_term')
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        ).distinct()
    context = {
        "users": users,
        "book": book_id,
    }
    return render(request, 'user_list.html', context)


def return_book(request, book_id):
    book = Book.objects.get(id=book_id)
    borrow = BookBorrow.objects.filter(book=book)
    last_borrow = borrow[len(borrow) - 1]
    user = last_borrow.user
    if not request.user.is_staff:
        return redirect("no-access")
    last_borrow.return_time = datetime.datetime.now()
    last_borrow.save()
    book.available = True
    book.save()
    return redirect(book)


############################################################################

"""
GENRE
"""


def create_genre(request):
    if not request.user.is_staff:
        return redirect("no-access")
    form = GenreForm()
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('genre-list')
    context = {
        "form": form,
    }
    return render(request, 'create_genre.html', context)


def genre_list(request):
    if not request.user.is_staff:
        return redirect("no-access")
    genres = Genre.objects.all()
    context = {
        "genres": genres
    }
    return render(request, 'genre_list.html', context)


############################################################################

"""
AUTHENTICATION
"""


def signup(request):
    if not request.user.is_staff:
        return redirect("no-access")
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            send_mail(
                'Welcome to the club!',
                'You are a member now!!',
                '3a1a3f93e1-d2fae3@inbox.mailtrap.io',
                [user.email],
                fail_silently=False,
            )
            login(request, user)
            return redirect("book-list")
    context = {
        "form": form,
    }
    return render(request, 'signup.html', context)


def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('book-list')
    context = {
        "form": form
    }
    return render(request, 'signin.html', context)


def signout(request):
    logout(request)
    return redirect("signin")


def no_access(request):
    return render(request, "no_access.html")
