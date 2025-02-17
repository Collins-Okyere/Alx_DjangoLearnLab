
# Create Operation for Book Model

**Command:**
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)  # Output: 1984
```

**Expected Output:**
```
1984
```
