from django.contrib import admin
from .models import *

# admin.site.register(Book)
# admin.site.register(BookAuthor)
# admin.site.register(BookCategory)
# admin.site.register(BookGenre)
# admin.site.register(BookTag)
# admin.site.register(BookReadingList)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BookGenre)
class BookGenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BookTag)
class BookTagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BookReadingList)
class BookReadingListAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
