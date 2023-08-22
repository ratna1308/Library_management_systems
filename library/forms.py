from django import forms
from .models import Book, BookRequest


class BookRequestForm(forms.ModelForm):
    class Meta:
        model = BookRequest
        fields = []


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
