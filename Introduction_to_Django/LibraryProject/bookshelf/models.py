from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100, blank=False)
    author = models.CharField(max_length=100, blank=False)
    publication_year = models.IntegerField(blank=False)

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"
