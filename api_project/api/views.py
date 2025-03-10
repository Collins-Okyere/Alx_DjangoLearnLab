from rest_framework.generics import ListAPIView
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class BookList(ListAPIView):
    queryset = Book.objects.all() 
    serializer_class = BookSerializer 

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all() 
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]