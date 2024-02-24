from ZVMEDIA import settings
from django.urls import path
from zvmediaserver import views

urlpatterns = [
    path('books/book/<slug:book_slug>', views.show_detail_book, name="detail_book"),
    path('books/genre/<slug:book_genre_slug>/', views.ShowBookGenre.as_view(), name="books_genre"),
    path('books/category/<slug:book_category_slug>/', views.ShowBookCategory.as_view(), name="books_category"),
    path('books/', views.ShowBooks.as_view(),name="books"),
    path('', views.index, name='home'),
]

# if settings.DEBUG:
#     urlpatterns += path('media/books/<slug:book_slug>', views.show_book_pdf, name="show_book_pdf")