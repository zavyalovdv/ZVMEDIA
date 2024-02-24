import os
from ZVMEDIA.settings import MEDIA_ROOT
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseNotFound, FileResponse
from .models import *


class ShowBooks(ListView):
    template_name = "zvmedia/jinja2/books/books.html"
    context_object_name = 'books'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Book.objects.all()


def show_detail_book(request, book_slug):
    try:
        book = get_object_or_404(Book, slug=book_slug)
        print(MEDIA_ROOT)
        print(os.path.join(MEDIA_ROOT, f'{book.file.name}'))
        return FileResponse(
            open(os.path.join(MEDIA_ROOT, f'{book.file.name}'), 'rb'),
            content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()


class ShowBookCategory(ListView):
    template_name = "zvmedia/jinja2/books/books_category.html"
    context_object_name = 'books'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['books'][0].category
        context['title'] = category.name
        return context

    def get_queryset(self):
        return Book.objects.filter(category__slug=self.kwargs['book_category_slug'])


class ShowBookGenre(ListView):
    template_name = "zvmedia/jinja2/books/books_genre.html"
    context_object_name = 'books'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        genre = context['books'][0].genre
        context['title'] = self.kwargs['book_genre_slug']
        return context

    def get_queryset(self):
        return Book.objects.filter(genre__slug=self.kwargs['book_genre_slug'])


def index(request):
    return render(request, "zvmedia/index.html")


# def show_books_genre(request, book_category_slug, book_genre_slug):
#     genre = BookGenre.objects.get(slug=book_genre_slug)
#     books = Book.objects.filter(genre=genre)
#     return render(request, "zvmedia/jinja2/books/books_genre.html",
#                   {'books': books, 'title': f'Книги по жанру {genre}'})

# def show_books_category(request, book_category_slug):
#     category = BookCategory.objects.get(slug=book_category_slug)
#     books = Book.objects.filter(category=category)
#     return render(request, "zvmedia/jinja2/books/books_category.html",
#                   {'books': books, 'title': f'Книги по категории {category}'})


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
