from django.db import models
from django.urls import reverse
from uuid import uuid4
from pytils.translit import slugify


def get_unique_slugify_models(instance, pre_slug):
    model = instance.__class__
    unique_slug = slugify(pre_slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{unique_slug}-{uuid4().hex[:8]}"
    return unique_slug


class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="artists/", null=True, blank=True)
    slug = models.SlugField(verbose_name="Слаг", unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slugify_models(self, self.name)
        super().save(*args, **kwargs)


class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="Albums")
    release_year = models.IntegerField(null=True, blank=True)
    cover = models.ImageField(upload_to="covers/", null=True, blank=True)
    slug = models.SlugField(verbose_name="Слаг", unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slugify_models(self, self.title)
        super().save(*args, **kwargs)


class Track(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, related_name="Tracks", null=True, blank=True
    )
    artist = models.ForeignKey(
        to="Artist",
        verbose_name="Исполнитель",
        related_name="Tracks",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    date = models.CharField(verbose_name="Год", null=True, blank=True)
    file_name = models.CharField(verbose_name="Имя файла", null=True, blank=True)
    file = models.FileField(upload_to="music/")
    duration = models.FloatField(default=0, null=True, blank=True)
    track_number = models.IntegerField(
        verbose_name="Номер трека", null=True, blank=True
    )
    disk = models.IntegerField(verbose_name="Номер диска", null=True, blank=True)
    total_tracks = models.IntegerField(
        verbose_name="Всего треков", null=True, blank=True
    )
    total_disks = models.IntegerField(
        verbose_name="Всего дисков", null=True, blank=True
    )
    bitrate = models.CharField(verbose_name="Битрейт", null=True, blank=True)
    format = models.CharField(max_length=10, null=True, blank=True)
    genre = models.ForeignKey(
        to="Genre",
        verbose_name="Жанр",
        related_name="Tracks",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    genre_auto_detect = models.CharField(
        verbose_name="Жанр автоопределение",
        null=True,
        blank=True,
    )
    slug = models.SlugField(verbose_name="Слаг", unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Если это первая загрузка файла
        if not self.slug:
            self.slug = get_unique_slugify_models(self, self.title)

        super().save(*args, **kwargs)


class Genre(models.Model):
    name = models.CharField(verbose_name="Жанр", unique=True)
    slug = models.SlugField(verbose_name="Слаг", unique=True, null=True, blank=True)

    # def get_absolute_url(self):
    #     # Например, возвращать пользователя на страницу со списком всех жанров
    #     return reverse("genres")
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slugify_models(self, self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
