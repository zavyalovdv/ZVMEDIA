import os
import pathlib
from zvmediaserver.const import *
from PyPDF2 import PdfFileReader
from django.db import models
from epub_conversion.utils import open_book, convert_epub_to_lines
from zvmediaserver.modules.services.utils import unique_slugify


class Book(models.Model):

    name = models.CharField(verbose_name="Название",
                            max_length=200, unique=True, db_index=True)
    file = models.FileField(verbose_name="Файл", upload_to="book")
    author = models.ManyToManyField(
        "BookAuthor", verbose_name="Автор", related_name="book")
    category = models.ForeignKey(
        "BookCategory", verbose_name="Категория", on_delete=models.PROTECT)
    genre = models.ManyToManyField(
        "BookGenre", verbose_name="Жанр", related_name="book")
    status = models.CharField(
        verbose_name="Статус", choices=BOOK_STATUS, max_length=200, default="NO_READ")
    pages_count = models.IntegerField(verbose_name="Количество страниц")
    words_count = models.IntegerField(verbose_name="Количество слов")
    time_to_read = models.FloatField(verbose_name="Часов на чтение")
    reading_list = models.ManyToManyField(
        "BookReadingList", verbose_name="Список чтения", related_name='book', blank=True)
    is_favorites = models.BooleanField(verbose_name="Избранное")

    tag = models.ManyToManyField(
        "BookTag", verbose_name="Тэги", related_name="book", blank=True)
    slug = models.SlugField(verbose_name="Слаг", max_length=255, unique=True)
    create_time = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True)
    update_time = models.DateTimeField(
        verbose_name="Дата изменения", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-create_time']
        indexes = [
            models.Index(fields=['-create_time'])
        ]

    def get_pdf_pages_count(file):
        document = PdfFileReader(open(file, 'rb'))
        return document.getNumPages()

    def get_words_count(pages_number):
        return pages_number * WORDS_PER_PAGE

    def get_epub_pages_count(file):
        book = open_book(file)
        rows = convert_epub_to_lines(book)
        words_count = 0
        for row in rows:
            words_count += len(row.split(" "))
        return round(words_count / WORDS_PER_PAGE)

    def get_reading_time(words_count, type):
        if type == "Художественная":
            return round(((words_count / WORDS_PER_MINUTE_IMAGINATIVE) / 60) * 10) / 10
        elif type == "Обучающая":
            return round(((words_count / WORDS_PER_MINUTE_LEARN) / 60) * 10) / 10

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        if not self.status:
            self.status = "NO_READ"
        if not self.time_to_read:
            if pathlib.Path(self.file.path).suffix == ".pdf":
                self.pages_count = self.get_pdf_pages_count(self.file)
            elif pathlib.Path(self.file.path).suffix == ".epub":
                self.pages_count = self.get_epub_pages_count(self.file)
            self.words_count = self.get_words_count(self.pages_count)
            self.time_to_read = self.get_reading_time(
                self.words_count, self.category.name)

        super().save(*args, **kwargs)


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

    # def get_absolute_url(self):
    #     return reverse()


class BookGenre(models.Model):
    name = models.CharField(verbose_name="Жанр",
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

    # def get_absolute_url(self):
    #     return reverse()


class BookReadingList(models.Model):
    name = models.CharField(verbose_name="Название",
                            max_length=200, unique=True, db_index=True)
    slug = models.SlugField(verbose_name="Слаг", max_length=255, unique=True)
    create_time = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True)
    update_time = models.DateTimeField(
        verbose_name="Дата изменения", auto_now=True)

    def __str__(self):
        return self.name


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
