from django.shortcuts import render
from django.http import HttpResponse
from .models import *
  
def index(request):
    books = Book.objects.all()
    return render(request, "zvmedia/jinja2/books/books.html", {'books': books, 'title': 'Книги'})
 
def about(request):
    return HttpResponse("О сайте")
 
def contact(request):
    return HttpResponse("Контакты")
