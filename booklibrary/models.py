from decimal import Decimal
from django.urls import reverse
from django.contrib.auth.models import User
from booklibrary.const import *
from simple_history import register
from simple_history.models import HistoricalRecords
from django.db import models
from booklibrary.modules.services.utils import (
    get_unique_slugify_models,
    get_user_directory_path,
)


class Book(models.Model):
    user = models.ForeignKey(User, related_name="books", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название", max_length=200, db_index=True)
    file = models.FileField(verbose_name="Файл", upload_to=get_user_directory_path)
    author = models.ManyToManyField("Author", verbose_name="Автор", related_name="book")
    category = models.ForeignKey(
        "Category", verbose_name="Категория", on_delete=models.PROTECT
    )
    subcategory = models.ManyToManyField(
        "Subcategory", verbose_name="Подкатегория", related_name="book"
    )
    status = models.CharField(
        verbose_name="Статус",
        choices=BOOK_STATUS,
        max_length=200,
        default="не читалась",
    )
    pages_count = models.IntegerField(
        verbose_name="Количество страниц", null=True, blank=True
    )
    words_count = models.IntegerField(
        verbose_name="Количество слов", null=True, blank=True
    )
    time_to_read = models.FloatField(
        verbose_name="Часов на чтение", null=True, blank=True
    )
    time_spent = models.FloatField(
        verbose_name="Часов затрачено", null=True, blank=True, default=0
    )
    target_date = models.DateField(verbose_name="Прочитать к", null=True, blank=True)
    time_left = models.DateField(verbose_name="Прочитать к", null=True, blank=True)
    current_page = models.IntegerField(
        verbose_name="Текущая страница", null=True, blank=True, default=1
    )
    progress = models.DecimalField(
        verbose_name="Прогресс", max_digits=5, decimal_places=2, null=True, blank=True
    )
    is_favorites = models.BooleanField(verbose_name="Избранное", default=False)
    slug = models.SlugField(verbose_name="Слаг", max_length=255, unique=True)
    create_time = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-create_time"]
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        indexes = [models.Index(fields=["-create_time"])]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slugify_models(self, self.name)
        if not self.status:
            self.status = "не читалась"
        if not self.is_favorites:
            self.is_favorites = False
        if self.progress:
            self.progress = Decimal(self.progress).quantize(Decimal("1.00"))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("books", kwargs={"slug": self.slug})


class Author(models.Model):
    user = models.ForeignKey(User, related_name="authors", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Имя", max_length=200, db_index=True)
    slug = models.SlugField(verbose_name="Слаг", max_length=255, unique=True)
    create_time = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slugify_models(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("authors", kwargs={"slug": self.slug})


class Category(models.Model):
    user = models.ForeignKey(User, related_name="categories", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Категория", max_length=200, db_index=True)
    slug = models.SlugField(verbose_name="Слаг", max_length=255, unique=True)
    create_time = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slugify_models(self, self.name)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("books", kwargs={"slug": self.slug})


class Subcategory(models.Model):
    user = models.ForeignKey(
        User, related_name="subcategories", on_delete=models.CASCADE
    )
    name = models.CharField(verbose_name="Подкатегория", max_length=200, db_index=True)
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.PROTECT
    )
    slug = models.SlugField(verbose_name="Слаг", max_length=255, unique=True)
    create_time = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slugify_models(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("books", kwargs={"slug": self.slug})
