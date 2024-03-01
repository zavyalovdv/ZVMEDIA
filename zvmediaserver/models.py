import os
import pathlib

from django.urls import reverse
from zvmediaserver.const import *
from PyPDF2 import PdfFileReader
from django.db import models
from epub_conversion.utils import open_book, convert_epub_to_lines
from zvmediaserver.modules.services.utils import unique_slugify_models


class Book(models.Model):

    name = models.CharField(verbose_name="Название",
                            max_length=200, db_index=True)
    file = models.FileField(verbose_name="Файл", upload_to="book")
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
        "BookReadList", verbose_name="Список чтения", related_name='book', blank=True)
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

    # def get_absolute_url(self):
    #     return reverse('books', kwargs={"slug": self.slug})


class BookAuthor(models.Model):
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

    # def get_absolute_url(self):
    #     return reverse()


class BookCategory(models.Model):
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

    # def get_absolute_url(self):
    #     return reverse()


class BookSubcategory(models.Model):
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

    # def get_absolute_url(self):
    #     return reverse()


class BookReadList(models.Model):
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


class BookTag(models.Model):
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
