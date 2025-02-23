from django.urls import path
from .views import LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from . import views, admin_view, librarian_view, member_view
from .views import list_books

urlpatterns = [
    # Authentication URLs
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),

    # Other views
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'), 
    path('admin-view/', admin_view.admin_view, name='admin_view'),
    path('librarian-view/', librarian_view.librarian_view, name='librarian_view'),
    path('member-view/', member_view.member_view, name='member_view'),
     path('add_book/', views.add_book, name='add_book'),  # Add book URL
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),  # Edit book URL
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),  # Delete book URL
    path('book_list/', views.book_list, name='book_list'),  #
]
