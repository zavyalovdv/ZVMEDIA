from django.urls import path
from zvmediaserver import views

urlpatterns = [
    path('books/subcategory/<slug:book_subcategory_slug>/', views.ShowBookSubcategory.as_view(), name="books_subcategory"),
    path('books/getsubcategories/<slug:category_slug>/', views.get_subcategory_by_category, name="get_subcategory_by_category"),
    path('books/category/<slug:book_category_slug>/', views.ShowBookCategory.as_view(), name="books_category"),
    path('books/browser/<slug:book_slug>', views.show_detail_book, name="browser_detail_book"),
    path('books/initpdf/<slug:book_slug>', views.book_init_as_pdf, name="pdf_init_book"),
    path('books/reader/<slug:book_slug>', views.book_reader_as_pdf, name="pdf_reader_book"),
    path('books/timeupdate/<slug:book_slug>', views.update_time, name="update_time"),
    path('books/getpdf/<slug:book_slug>', views.book_get_pdf, name="get_pdf_book"),
    path('books/setpdf/<slug:book_slug>', views.book_set_pdf, name="set_pdf_book"),
    path('books/newbook/', views.CreateBook.as_view(), name="add_book"),
    path('books/removebook/<slug:book_slug>', views.delete_book, name="remove_book"),
    path('books/editbook/<slug:book_slug>', views.UpdateBook.as_view(), name="edit_book"),
    path('books/newcategory/', views.CreateBookCategory.as_view(), name="add_category"),
    path('books/newsubcategory/', views.CreateBookSubcategory.as_view(), name="add_subcategory"),
    #path('books/authors/', views.ShowBookAuthor.as_view(), name="book_authors"),
    path('books/author/<slug:author_slug>/', views.ShowBookAuthor.as_view(), name="books_author"),
    path('books/newauthor/', views.CreateBookAuthor.as_view(), name="add_author"),
    path('books/newreadinglist/', views.CreateBookReadingList.as_view(), name="add_readinglist"),
    path('books/changefavorite/', views.book_change_favorite, name="change_favorite"),
    path('books/', views.ShowBooks.as_view(),name="books"),
    path('login/', views.userlogin,name="login"),
    path('logout/', views.userlogout,name="logout"),
    path('', views.index, name='home'),
]
