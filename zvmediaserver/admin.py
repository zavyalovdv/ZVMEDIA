from django.contrib import admin
from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', 'category', 'status', 'pages_count',
                    'words_count', 'time_to_read', 'slug', 'create_time', 'update_time')
    # prepopulated_fields = {'slug': ('name',)}
    fields = ['name', 'file', 'author', 'category', 'subcategory','target_date']


class BookAuthorAdmin(admin.ModelAdmin):
    fields = ['name']
    # prepopulated_fields = {'slug': ('name',)}


class BookCategoryAdmin(admin.ModelAdmin):
    fields = ['name']
    # prepopulated_fields = {'slug': ('name',)}


class BookSubcategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'category']
    # prepopulated_fields = {'slug': ('name',)}


class BookTagAdmin(admin.ModelAdmin):
    fields = ['name']
    # prepopulated_fields = {'slug': ('name',)}


class BookReadingListAdmin(admin.ModelAdmin):
    fields = ['name']
    # prepopulated_fields = {'slug': ('name',)}


admin.site.register(Book, BookAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookCategory, BookCategoryAdmin)
admin.site.register(BookSubcategory, BookSubcategoryAdmin)
admin.site.register(BookTag, BookTagAdmin)
admin.site.register(BookReadingList, BookReadingListAdmin)
