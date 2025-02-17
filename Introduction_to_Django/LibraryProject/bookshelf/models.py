from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200, blank=False)  # Required
    author = models.CharField(max_length=200, blank=False)  # Required
    publication_year = models.IntegerField(blank=False)  # Required

    def __str__(self):
        return self.title
