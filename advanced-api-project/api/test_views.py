from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author, Book

class BookAPITestCase(APITestCase):
    """Test CRUD operations, filtering, searching, and ordering for the Book API."""

    def setUp(self):
        """Set up test data before each test."""
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")  # Login the user

        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="Harry Potter", publication_year=1997, author=self.author)

        self.book_list_url = reverse("book-list")
        self.book_create_url = reverse("book-create")
        self.book_update_url = reverse("book-update", kwargs={"pk": self.book.id})
        self.book_delete_url = reverse("book-delete", kwargs={"pk": self.book.id})

    def test_create_book_authenticated(self):
        """Ensure an authenticated user can create a book using self.client.login()."""
        data = {"title": "New Book", "publication_year": 2020, "author": self.author.id}
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_unauthenticated(self):
        """Ensure an unauthenticated user cannot create a book."""
        self.client.logout()  # Logout to test unauthenticated scenario
        data = {"title": "Unauthorized Book", "publication_year": 2021, "author": self.author.id}
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        """Ensure an authenticated user can update a book."""
        data = {"title": "Updated Book", "publication_year": 2010, "author": self.author.id}
        response = self.client.put(self.book_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book_authenticated(self):
        """Ensure an authenticated user can delete a book."""
        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
