from django import forms
from . models import Book

class BookSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Search for books')


class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'isbn', 'summary']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name'}),
            'published_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ISBN'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter book summary'}),
        }
        labels = {
            'title': 'Book Title',
            'author': 'Author',
            'published_date': 'Published Date',
            'isbn': 'ISBN',
            'summary': 'Summary',
        }