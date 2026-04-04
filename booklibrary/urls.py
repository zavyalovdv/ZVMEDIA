from django.urls import path
from booklibrary import views

urlpatterns = [
    path(
        "getsubcategories/<slug:category_slug>/",
        views.get_subcategory_by_category,
        name="get_subcategory_by_category",
    ),
    path("getcategories/", views.get_categories, name="get_categories"),
    path(
        "category/favorites/",
        views.ShowFavoriteBook.as_view(),
        name="books_favorites",
    ),
    path(
        "category/<slug:book_category_slug>/",
        views.ShowBookCategory.as_view(),
        name="books_category",
    ),
    path(
        "subcategory/<slug:book_subcategory_slug>/",
        views.ShowBookSubcategory.as_view(),
        name="books_subcategory",
    ),
    path(
        "browser/<slug:book_slug>",
        views.show_detail_book,
        name="browser_detail_book",
    ),
    path("initpdf/<slug:book_slug>", views.book_init_as_pdf, name="pdf_init_book"),
    path(
        "reader/<slug:book_slug>",
        views.book_reader_as_pdf,
        name="pdf_reader_book",
    ),
    path(
        "extradataupdate/<slug:book_slug>/",
        views.ajax_update_extradata_book,
        name="update_extradata",
    ),
    path("getpdf/<slug:book_slug>", views.book_get_pdf, name="get_pdf_book"),
    path("setpdf/<slug:book_slug>/", views.book_set_pdf, name="set_pdf_book"),
    path("newbook/", views.CreateBook.as_view(), name="add_book"),
    path("removebook/<slug:book_slug>", views.delete_book, name="remove_book"),
    path("editbook/<slug:book_slug>", views.UpdateBook.as_view(), name="edit_book"),
    path("newcategory/", views.CreateBookCategory.as_view(), name="add_category"),
    path(
        "newsubcategory/",
        views.CreateBookSubcategory.as_view(),
        name="add_subcategory",
    ),
    path(
        "author/<slug:author_slug>/",
        views.ShowBookAuthor.as_view(),
        name="books_author",
    ),
    path("newauthor/", views.CreateBookAuthor.as_view(), name="add_author"),
    path("activity/", views.get_activity, name="activity"),
    path("changefavorite/", views.book_change_favorite, name="change_favorite"),
    path("", views.ShowBooks.as_view(), name="books"),
]
