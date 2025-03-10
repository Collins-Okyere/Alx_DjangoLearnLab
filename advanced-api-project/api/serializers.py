from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    This serializer handles serialization and deserialization of Book instances.
    It includes validation to prevent books from being created with a future
    publication year.

    Fields:
        - title: The book's title.
        - publication_year: The year the book was published.
        - author: A foreign key reference to the author.

    Validation:
        - `validate_publication_year()`: Ensures that the book’s publication year
          is not in the future.
    """

    def validate_publication_year(self, value):
        """
        Ensure the publication year is not set in the future.

        Args:
            value (int): The publication year provided by the user.

        Raises:
            serializers.ValidationError: If the year is greater than the current year.

        Returns:
            int: The validated publication year.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

    class Meta:
        model = Book
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.

    This serializer handles serialization and deserialization of Author instances.
    It includes a nested BookSerializer to display books authored by each author.

    Fields:
        - name: The author's name.
        - books: A nested list of books written by the author, using BookSerializer.

    Relationship Handling:
        - The `books` field uses `BookSerializer(many=True, read_only=True)`, which
          allows nested representation of books associated with an author.
        - `read_only=True` ensures that books are only included in the response
          and are not directly created through this serializer.

    Example Output:
    ```json
    {
        "name": "J.K. Rowling",
        "books": [
            {
                "title": "Harry Potter and the Philosopher's Stone",
                "publication_year": 1997,
                "author": 1
            }
        ]
    }
    ```
    """

    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']
