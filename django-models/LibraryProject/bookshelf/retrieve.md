
# Retrieve Operation for Book Model

**Command:**
```python
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)  # Output: 1984 George Orwell 1949
```

**Expected Output:**
```
1984 George Orwell 1949
```
