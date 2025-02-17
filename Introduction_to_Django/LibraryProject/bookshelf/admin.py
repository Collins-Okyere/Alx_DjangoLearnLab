from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    # Display the title, author, and publication year in the admin list view
    list_display = ('title', 'author', 'publication_year')

    # Enable search functionality on title and author fields
    search_fields = ('title', 'author')

    # Add filter options for publication year
    list_filter = ('publication_year',)

admin.site.register(Book)
