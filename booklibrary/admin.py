from django.contrib import admin
from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver


class Admin(admin.ModelAdmin):
    list_display = (
        "name",
        "file",
        "category",
        "status",
        "pages_count",
        "words_count",
        "time_to_read",
        "slug",
        "create_time",
        "update_time",
    )
    # prepopulated_fields = {'slug': ('name',)}
    fields = [
        "user",
        "name",
        "file",
        "author",
        "category",
        "subcategory",
        "target_date",
    ]


class AuthorAdmin(admin.ModelAdmin):
    fields = ["user", "name"]
    # prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    fields = ["user", "name"]
    # prepopulated_fields = {'slug': ('name',)}


class SubcategoryAdmin(admin.ModelAdmin):
    fields = ["user", "name", "category"]
    # prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    fields = ["user", "name"]
    # prepopulated_fields = {'slug': ('name',)}


class ReadingListAdmin(admin.ModelAdmin):
    fields = ["user", "name", "books", "books_ordering"]
    # prepopulated_fields = {'slug': ('name',)}


class OrderingInReadingListAdmin(admin.ModelAdmin):
    fields = ["user", "position", "book"]


admin.site.register(Book, Admin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
