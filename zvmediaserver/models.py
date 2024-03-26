from decimal import Decimal
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
    return f'books/{instance.user.username}/{filename}'


class UserProfileSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    book_verbose_type = models.BooleanField(verbose_name="Просмотрщик книг", choices=BOOK_VERBOSE_TYPE, default=True)
    order_by = models.CharField(verbose_name="Поле для сортировки",max_length=200, blank=True,null=True)
    is_reverse_order_by = models.BooleanField(verbose_name="Прямой или обратный порядок сортировки", blank=True, null=True)


class Book(models.Model):
    user = models.ForeignKey(User, related_name='books',
                             on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название",
                            max_length=200, db_index=True)
    file = models.FileField(verbose_name="Файл", upload_to=user_directory_path)
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
    time_spent = models.FloatField(
        verbose_name="Часов затрачено", null=True, blank=True, default=0)
    target_date = models.DateField(
        verbose_name="Прочитать к", null=True, blank=True)
    time_left = models.DateField(
        verbose_name="Прочитать к", null=True, blank=True)
    current_page = models.IntegerField(
        verbose_name="Текущая страница", null=True, blank=True, default=1)
    progress = models.DecimalField(
        verbose_name="Прогресс",max_digits=5, decimal_places=2, null=True, blank=True)
    # reading_list = models.ManyToManyField(
    #     "BookReadingList", verbose_name="Список чтения", related_name='book', blank=True)
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
        if self.progress:
             self.progress = Decimal(self.progress).quantize(Decimal("1.00"))
             print(self.progress)
             print(type(self.progress))
        # if self.time_spent:
        #     self.time_spent = round(self.time_spent, 1)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('books', kwargs={"slug": self.slug})


class BookAuthor(models.Model):
    user = models.ForeignKey(User, related_name='authors',
                             on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name="Имя", max_length=200, db_index=True)
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
                            max_length=200, db_index=True)
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
                            max_length=200, db_index=True)
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
    user = models.ForeignKey(User, related_name='readinglists',
                             on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название",
                            max_length=200, db_index=True)
    # position = models.IntegerField(verbose_name="Номер позиции в списке")
    books = models.ManyToManyField(Book, verbose_name="Книга", related_name="readinglists",
                            max_length=200, db_index=True, blank=True, null=True)
    books_ordering = models.ForeignKey("BookOrderingInReadingList",verbose_name="Порядок чтения",
                            max_length=200, on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name="Слаг", max_length=255, unique=True)
    create_time = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True)
    update_time = models.DateTimeField(
        verbose_name="Дата изменения", auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.user = User.objects.get(pk=1)
        if not self.slug:
            self.slug = unique_slugify_models(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('books', kwargs={"slug": self.slug})


# class BookPositionInReadingList(models.Model):
#     user = models.ForeignKey(User, related_name='bookpositions',
#                              on_delete=models.CASCADE)
#     position = models.IntegerField(verbose_name="Номер позиции в списке")
#     reading_list = models.ForeignKey(BookReadingList, verbose_name="Список чтения",
#                             max_length=200, db_index=True,on_delete=models.DO_NOTHING)
#     book = models.ForeignKey(Book, verbose_name="Книга",
#                             max_length=200, db_index=True,on_delete=models.CASCADE)
#     create_time = models.DateTimeField(
#         verbose_name="Дата создания", auto_now_add=True)
#     update_time = models.DateTimeField(
#         verbose_name="Дата изменения", auto_now=True)


class BookOrderingInReadingList(models.Model):
    user = models.ForeignKey(User, related_name='bookpositions',
                             on_delete=models.CASCADE)
    position = models.IntegerField(verbose_name="Номер позиции в списке")
    # reading_list = models.ForeignKey(BookReadingList, verbose_name="Список чтения",
    #                         max_length=200, db_index=True,on_delete=models.DO_NOTHING)
    book = models.ForeignKey(Book, verbose_name="Книга",
                            max_length=200, db_index=True,on_delete=models.CASCADE, blank=True, null=True)
    create_time = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True)
    update_time = models.DateTimeField(
        verbose_name="Дата изменения", auto_now=True)

    # def __str__(self):
    #     return self.name

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = unique_slugify_models(self, self.name)
    #     super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('books', kwargs={"slug": self.slug})



class BookTag(models.Model):
    user = models.ForeignKey(User, related_name='tags',
                             on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name="Тэг", max_length=200, db_index=True)
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
