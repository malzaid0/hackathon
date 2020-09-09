from django.shortcuts import render, redirect
from .forms import SignupForm, SigninForm, BookForm, GenreForm
from django.contrib.auth import login, authenticate, logout
from .models import Book, Genre
from django.db.models import Q


# Create your views here.
def create_book(request):
    form = BookForm()
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user
            book.save()
            return redirect('book-list')
    context = {
        "form": form,
    }
    return render(request, 'create_book.html', context)


def book_list(request):
    books = Book.objects.all()
    query = request.GET.get('search_term')
    if query:
        try:
            books = books.filter(
                Q(name__icontains=query) |
                Q(isbn__exact=int(query)) |
                Q(genre__name__icontains=query)
            ).distinct()
        except:
            books = books.filter(
                Q(name__icontains=query) |
                Q(genre__name__icontains=query)
            ).distinct()
    context = {
        "books": books
    }
    return render(request, 'book_list.html', context)


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    context = {
        "book": book,
    }
    return render(request, 'book_detail.html', context)


def book_search(request):
    if request.method == "POST":
        search_term = request.POST.get("searchTerm")
        books = Book.objects.filter(name__contains=search_term)
        context = {
            "search_result": books,
        }
        return render(request, "search_result.html", context)


def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect("signin")
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
                return redirect('signin')
    context = {
        "form": form
    }
    return render(request, 'signin.html', context)


def signout(request):
    logout(request)
    return redirect("signin")
