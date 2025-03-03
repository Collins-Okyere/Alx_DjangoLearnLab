from django.urls import path
from .views import list_books, LibraryDetailView 
from .views import admin_view, librarian_view, member_view
from .import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import add_book, edit_book, delete_book

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
    
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),

    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),

    path('books/', views.list_books, name='list_books'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    path('add_book/', add_book, name='add_book'),
    path('edit_book/', edit_book, name='edit_book'),
    path('delete_book/', delete_book, name='delete_book'),

    ]

