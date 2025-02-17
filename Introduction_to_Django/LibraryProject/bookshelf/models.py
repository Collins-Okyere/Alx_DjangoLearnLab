from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200, blank=False)  # Required field
    author = models.CharField(max_length=100, blank=False)  # Required field
    publication_year = models.IntegerField(blank=False)  # Required field

    def __str__(self):
        return self.title
