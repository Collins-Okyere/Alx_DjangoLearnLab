from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)
    return books

# List all books in a library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    return books

# Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    try:
        # Try to get the library object
        library = Library.objects.get(name=library_name)
        
        # Check if a librarian is associated with this library
        if library.librarian:
            return library.librarian  # directly access the librarian through the relationship
        else:
            print(f"No librarian assigned to '{library_name}' library.")
            return None
    except Library.DoesNotExist:
        print(f"Library with name '{library_name}' does not exist.")
        return None
