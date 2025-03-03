from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ExampleForm
from .forms import BookSearchForm
from .models import Book
from django.http import HttpResponseForbidden
from .models import Article
# Create your views here.

@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
     books = Book.objects.all()
     return render(request)

@permission_required("bookshelf.can_create", raise_exception=True)
def create_book(request):
    if request.method == "POST":
         pass
    return render(request)

@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        pass
    return render(request)

@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return render("request")


@login_required
def example_form_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            return redirect('example_success')
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/example_form.html', {'form': form})