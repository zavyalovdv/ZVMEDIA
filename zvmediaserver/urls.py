from django.urls import path
from zvmediaserver import views

urlpatterns = [
    path('books/subcategory/<slug:book_subcategory_slug>/', views.ShowBookSubcategory.as_view(), name="books_subcategory"),
    path('books/category/<slug:book_category_slug>/', views.ShowBookCategory.as_view(), name="books_category"),
    path('books/browser/<slug:book_slug>', views.show_detail_book, name="browser_detail_book"),
    path('books/django/<slug:book_slug>', views.book_view_as_text, name="django_detail_book"),
    path('books/newbook/', views.CreateBook.as_view(), name="add_book"),
    path('books/newcategory/', views.CreateBookCategory.as_view(), name="add_category"),
    path('books/newsubcategory/', views.CreateBookSubcategory.as_view(), name="add_subcategory"),
    path('books/newreadlist/', views.CreateBookReadList.as_view(), name="add_readlist"),
    path('books/changefavorite/', views.book_change_favorite, name="change_favorite"),
    path('books/', views.ShowBooks.as_view(),name="books"),
    path('', views.index, name='home'),
]
