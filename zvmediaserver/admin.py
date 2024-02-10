from django.contrib import admin
from .models import Author, Book, BookCategory, BookGenre

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(BookCategory)
admin.site.register(BookGenre)
