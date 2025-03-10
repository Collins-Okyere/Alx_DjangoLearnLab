from rest_framework import serializers
from .models import Book  # Import the Book model

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # Includes all fields from the Book model
