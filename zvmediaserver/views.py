import os
from ZVMEDIA.settings import MEDIA_ROOT
from django.http import Http404, HttpResponse, HttpResponseNotFound, FileResponse
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, render
from zvmediaserver.forms import AddBookCategoryForm, AddBookForm, AddBookReadListForm, AddBookSubcategoryForm
from .models import *
from django.urls import reverse_lazy


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
        return FileResponse(
            open(os.path.join(MEDIA_ROOT, f'{book.file.name}'), 'rb'),
            content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()


def book_view_as_text(request, book_slug):
    book = Book.objects.get(slug=book_slug)
    file = book.file
    try:
        path = os.path.join(MEDIA_ROOT, 'book')
        doc = open(os.path.join(path, f"{book.slug}.txt"), "r")
        print(os.path.join(path, f"{book.slug}.txt"))
        template = 'zvmedia/jinja2/books/detail_book_as_text.html'
        return render(request,template_name=template,context={'book':file})
    except:
        return render(request,template_name=template,context={'book':'error'})
    else:
        my_file.close()


def book_change_favorite(request):
    is_favorites = request.GET['is_favorites']
    book = Book.objects.get(slug=request.GET['slug'])
    if is_favorites == 'False':
        book.is_favorites = False
    else:
        book.is_favorites = True
    try:
        book.save(update_fields=["is_favorites"])
    except:
        response = {'is_taken': False}
    response = {
        'is_taken': True
    }
    return JsonResponse(response)

class CreateBook(CreateView):
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    model = Book
    form_class = AddBookForm
    template_name = 'zvmedia/jinja2/books/add_book.html'
    success_url = "/books"


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


class CreateBookCategory(CreateView):
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    model = BookCategory
    form_class = AddBookCategoryForm
    template_name = 'zvmedia/jinja2/books/add_book.html'
    success_url = "/books"

class ShowBookSubcategory(ListView):
    template_name = "zvmedia/jinja2/books/books_subcategory.html"
    context_object_name = 'books'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        subcategory = context['books'][0].genre
        context['title'] = self.kwargs['book_subcategory_slug']
        return context

    def get_queryset(self):
        return Book.objects.filter(subcategory__slug=self.kwargs['book_subcategory_slug'])


class CreateBookSubcategory(CreateView):
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    model = Book
    form_class = AddBookSubcategoryForm
    template_name = 'zvmedia/jinja2/books/add_book.html'
    success_url = "/books"


class CreateBookReadList(CreateView):
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    model = BookReadList
    form_class = AddBookReadListForm
    template_name = 'zvmedia/jinja2/books/add_book.html'
    success_url = "/books"


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
