import os
import pathlib

from django.urls import reverse
from django.contrib.auth.models import User
from zvmediaserver.const import *
from PyPDF2 import PdfFileReader
from django.db import models
from epub_conversion.utils import open_book, convert_epub_to_lines
from zvmediaserver.modules.services.utils import unique_slugify_models



def user_directory_path(instance, filename):
    return f'books/{instance.user.name}/{filename}'


class UserProfileSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    book_verbose_type = models.CharField(choices=BOOK_VERBOSE_TYPE)


class Book(models.Model):
    user = models.ForeignKey(User, related_name='books',
                             on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название",
                            max_length=200, db_index=True)
    file = models.FileField(verbose_name="Файл", upload_to="user_directory_path")
    author = models.ManyToManyField(
        "BookAuthor", verbose_name="Автор", related_name="book")
    category = models.ForeignKey(
        "BookCategory", verbose_name="Категория", on_delete=models.PROTECT)
    subcategory = models.ManyToManyField(
        "BookSubcategory", verbose_name="Подкатегория", related_name="book")
    status = models.CharField(
        verbose_name="Статус", choices=BOOK_STATUS, max_length=200, default="не читалась")
    pages_count = models.IntegerField(
        verbose_name="Количество страниц", null=True, blank=True)
    words_count = models.IntegerField(
        verbose_name="Количество слов", null=True, blank=True)
    time_to_read = models.FloatField(
        verbose_name="Часов на чтение", null=True, blank=True)
    reading_list = models.ManyToManyField(
        "BookReadingList", verbose_name="Список чтения", related_name='book', blank=True)
    is_favorites = models.BooleanField(verbose_name="Избранное", default=False)
    tag = models.ManyToManyField(
        "BookTag", verbose_name="Тэги", related_name="book", blank=True)
    slug = models.SlugField(verbose_name="Слаг", max_length=255, unique=True)
    create_time = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True)
    update_time = models.DateTimeField(
        verbose_name="Дата изменения", auto_now=True)

    class Meta:
        ordering = ['-create_time']
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        indexes = [
            models.Index(fields=['-create_time'])
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify_models(self, self.name)
        if not self.status:
            self.status = "не читалась"
        if not self.is_favorites:
            self.is_favorites = False

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('books', kwargs={"slug": self.slug})


class BookAuthor(models.Model):
    user = models.ForeignKey(User, related_name='authors',
                             on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name="Имя", max_length=200, unique=True, db_index=True)
    slug = models.SlugField(verbose_name="Слаг", max_length=255, unique=True)
    create_time = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True)
    update_time = models.DateTimeField(
        verbose_name="Дата изменения", auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify_models(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('authors', kwargs={"slug": self.slug})


class BookCategory(models.Model):
    user = models.ForeignKey(User, related_name='categories',
                             on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Категория",
                            max_length=200, unique=True, db_index=True)
    slug = models.SlugField(verbose_name="Слаг", max_length=255, unique=True)
    create_time = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True)
    update_time = models.DateTimeField(
        verbose_name="Дата изменения", auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify_models(self, self.name)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('books', kwargs={"slug": self.slug})


class BookSubcategory(models.Model):
    user = models.ForeignKey(User, related_name='subcategories',
                             on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Подкатегория",
                            max_length=200, unique=True, db_index=True)
    category = models.ForeignKey(
        BookCategory, verbose_name="Категория", on_delete=models.PROTECT)
    slug = models.SlugField(verbose_name="Слаг", max_length=255, unique=True)
    create_time = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True)
    update_time = models.DateTimeField(
        verbose_name="Дата изменения", auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify_models(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('books', kwargs={"slug": self.slug})


class BookReadingList(models.Model):
    user = models.ForeignKey(User, related_name='readinglist',
                             on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название",
                            max_length=200, unique=True, db_index=True)
    slug = models.SlugField(verbose_name="Слаг", max_length=255, unique=True)
    create_time = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True)
    update_time = models.DateTimeField(
        verbose_name="Дата изменения", auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify_models(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('books', kwargs={"slug": self.slug})


class BookTag(models.Model):
    user = models.ForeignKey(User, related_name='tags',
                             on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name="Тэг", max_length=200, unique=True, db_index=True)
    slug = models.SlugField(verbose_name="Слаг", max_length=255, unique=True)
    create_time = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True)
    update_time = models.DateTimeField(
        verbose_name="Дата изменения", auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify_models(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('books', kwargs={"slug": self.slug})