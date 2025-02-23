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
def get_librarian_for_library(librarian_name):
    try:
        librarian = Librarian.objects.get(name=librarian_name)
        
        if librarian.library:
            return librarian.library 
        else:
            print(f"No librarian by name '{librarian_name}' is assigned to a library.")
            return None
    except Librarian.DoesNotExist:
        print(f"Librarian with name '{librarian_name}' does not exist.")
        return None
