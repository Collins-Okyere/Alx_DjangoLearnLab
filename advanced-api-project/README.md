<!-- Advanced API ProjectOverview -->
This project is built with Django REST Framework to handle book and author management.

<!-- API Endpoints -->
--- Method --- Endpoint    --- Description      --- Authentication
--- GET    --- /api/books/ --- Retrieve all books   --- Public
--- GET    --- /api/books/{id}/        --- Retrieve a specific book    --- Public
--- POST   --- /api/books/create/      --- Create a new book    --- Authenticated
--- PUT    --- /api/books/update/{id}/ --- Update an existing book     --- Authenticated
--- DELETE --- /api/books/delete/{id}/ --- Delete a book    --- Authenticated

<!-- Setup -->
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Start the server: `python manage.py runserver`

<!-- API Query Features -->
- Filter by author, title, or publication year: `/api/books/?author=1`
- Search books by title or author name: `/api/books/?search=Harry`
- Order results by title or publication year: `/api/books/?ordering=-publication_year`

<!-- Running API Tests -->
- Run tests using: `python manage.py test api`
- Tests include:
  - CRUD operations for the Book model
  - Filtering, searching, and ordering
  - Authentication-based access controls
- Ensure all tests pass before deploying.
