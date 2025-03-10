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
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="Harry Potter", publication_year=1997, author=self.author)

        self.book_list_url = reverse("book-list")
        self.book_detail_url = reverse("book-detail", kwargs={"pk": self.book.id})
        self.book_create_url = reverse("book-create")
        self.book_update_url = reverse("book-update", kwargs={"pk": self.book.id})
        self.book_delete_url = reverse("book-delete", kwargs={"pk": self.book.id})

    def test_list_books(self):
        """Ensure we can retrieve the list of books."""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Harry Potter")

    def test_create_book_authenticated(self):
        """Ensure an authenticated user can create a book."""
        self.client.force_authenticate(user=self.user)
        data = {"title": "New Book", "publication_year": 2020, "author": self.author.id}
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_unauthenticated(self):
        """Ensure an unauthenticated user cannot create a book."""
        data = {"title": "Unauthorized Book", "publication_year": 2021, "author": self.author.id}
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        """Ensure an authenticated user can update a book."""
        self.client.force_authenticate(user=self.user)
        data = {"title": "Updated Book", "publication_year": 2010, "author": self.author.id}
        response = self.client.put(self.book_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book_authenticated(self):
        """Ensure an authenticated user can delete a book."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_search_books(self):
        """Ensure search functionality works."""
        response = self.client.get(f"{self.book_list_url}?search=Harry")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books_by_year(self):
        """Ensure ordering books by publication year works."""
        Book.objects.create(title="Another Book", publication_year=2022, author=self.author)
        response = self.client.get(f"{self.book_list_url}?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Harry Potter")  # Should be first (oldest)
