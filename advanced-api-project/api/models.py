from django.db import models

class Author(models.Model):
    """
    The Author model represents an individual author in the system.

    Attributes:
        name (str): A string field to store the author's name.
    
    Relationship:
        One-to-Many: One author can have multiple books, which is represented
        by the related_name="books" in the Book model.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        """Return the string representation of the author (their name)."""
        return self.name


class Book(models.Model):
    """
    The Book model represents a book in the system.

    Attributes:
        title (str): The title of the book.
        publication_year (int): The year the book was published.
        author (ForeignKey): A reference to the Author model, establishing a
        one-to-many relationship where multiple books can belong to a single author.

    Relationship:
        Many-to-One: Each book is linked to a single author through the ForeignKey
        field. If an author is deleted, all related books will also be deleted
        due to on_delete=models.CASCADE.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        """Return the string representation of the book (its title)."""
        return self.title
