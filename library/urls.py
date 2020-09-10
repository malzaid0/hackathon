"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from libraryapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.book_list, name='book-list'),
    path('<int:book_id>/', views.book_detail, name='book-detail'),
    path('<int:book_id>/delete/', views.book_delete, name='book-delete'),
    path('create/', views.create_book, name='book-create'),

    path('<int:book_id>/borrow/', views.borrow_book, name='book-borrow'),
    path('<int:book_id>/return/', views.return_book, name='book-return'),
    path('<int:book_id>/users/', views.user_list, name='users-list'),
    path('<int:book_id>/users/<int:user_id>/', views.borrow_book_to_user, name='borrow-to-user'),

    path('genres/', views.genre_list, name='genre-list'),
    path('genres/create/', views.create_genre, name='genre-create'),

    path('profile/<int:user_id>/', views.profile_detail, name='profile'),

    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path("no-access/", views.no_access, name="no-access"),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)