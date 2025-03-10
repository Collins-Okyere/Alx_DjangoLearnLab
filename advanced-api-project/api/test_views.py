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

    def test_list_books(self):
        """Ensure listing books returns the correct response with response.data."""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Expecting one book in response
        self.assertEqual(response.data[0]["title"], "Harry Potter")
        self.assertEqual(response.data[0]["publication_year"], 1997)
        self.assertEqual(response.data[0]["author"], self.author.id)

    def test_create_book_authenticated(self):
        """Ensure an authenticated user can create a book and response.data contains the correct data."""
        data = {"title": "New Book", "publication_year": 2020, "author": self.author.id}
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Book")
        self.assertEqual(response.data["publication_year"], 2020)
        self.assertEqual(response.data["author"], self.author.id)

    def test_create_book_unauthenticated(self):
        """Ensure an unauthenticated user cannot create a book."""
        self.client.logout()
        data = {"title": "Unauthorized Book", "publication_year": 2021, "author": self.author.id}
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        """Ensure an authenticated user can update a book and response.data reflects the changes."""
        data = {"title": "Updated Book", "publication_year": 2010, "author": self.author.id}
        response = self.client.put(self.book_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Book")
        self.assertEqual(response.data["publication_year"], 2010)

    def test_delete_book_authenticated(self):
        """Ensure an authenticated user can delete a book."""
        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books_by_author(self):
        """Test filtering books by author name."""
        response = self.client.get(self.book_list_url, {"author": self.author.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Harry Potter")

    def test_search_books_by_title(self):
        """Test searching books by title."""
        response = self.client.get(self.book_list_url, {"search": "Harry"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertIn("Harry Potter", [book["title"] for book in response.data])

    def test_order_books_by_publication_year(self):
        """Test ordering books by publication year."""
        Book.objects.create(title="Another Book", publication_year=2000, author=self.author)
        response = self.client.get(self.book_list_url, {"ordering": "publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["publication_year"], 1997)  # Earliest book first

        response_desc = self.client.get(self.book_list_url, {"ordering": "-publication_year"})
        self.assertEqual(response_desc.status_code, status.HTTP_200_OK)
        self.assertEqual(response_desc.data[0]["publication_year"], 2000)  # Latest book first
