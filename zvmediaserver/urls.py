from django.urls import path
from zvmediaserver import views

urlpatterns = [
    path('books/<slug:book_category_slug>/<slug:book_genre_slug>/<slug:book_slug>', views.show_books_genre, name="book"),
    path('books/<slug:book_category_slug>/<slug:book_genre_slug>/', views.show_books_genre, name="books_genre"),
    path('books/<slug:book_category_slug>/', views.show_books_category, name="books_category"),
    path('books/', views.show_books,name="books"),
    path('', views.index, name='home'),
]
