from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
  
def index(request):
    return render(request, "zvmedia/index.html")
 
def show_books(request):
    books = Book.objects.all()
    return render(request, "zvmedia/jinja2/books/books.html", {'books': books, 'title': 'Книги'})

def show_book(request, book_pk):
    if show_books_category:
        book = get_object_or_404(Book, pk=book_pk)
    data = {
        'title': book.title,
    }
    return render(request, "zvmedia/jinja2/books/book.html", context=data)

def show_books_category(request, books_category_slug):
    return HttpResponse(f"<h1>{books_category_slug}</h1>")

def show_books_genre(request, book_category_slug, book_genre_slug, book_slug):
    data = {
        'title': book_genre_slug,
    }
    return render(request, "zvmedia/jinja2/books/book.html", context=data)
def contact(request):
    return HttpResponse("Контакты")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")