# Delete Operation for Book Model

**Command:**
```python
from bookshelf.models import Book

# Delete the book instance
book.delete()

# Check if the book was deleted
print(Book.objects.all())  # Output: <QuerySet []>
