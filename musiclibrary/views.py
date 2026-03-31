from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from .models import Genre, Track, Album, Artist
from django import forms
from django.views.generic import FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from musiclibrary import services


class MainMusics(ListView):
    model = Track
    template_name = "musiclibrary/musics.html"
    # context_object_name = "tracks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем жанры в словарь контекста
        context["genres"] = Genre.objects.all()
        context["tracks"] = Track.objects.all()
        return context


class AlbumDetailView(DetailView):
    model = Album
    template_name = "player/album.html"
    # В шаблоне обратимся через album.tracks.all


class AddTrack(CreateView):
    model = Track
    fields = ["title", "genre", "file"]
    template_name = "musiclibrary/add-track.html"
    success_url = reverse_lazy("music")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем жанры в словарь контекста
        context["genres"] = Genre.objects.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        if self.object.file:
            file_path = self.object.file.path
            services.extract_metadata(self.object)

        self.object.save()
        return super().form_valid(form)


class AddGenre(CreateView):
    model = Genre
    # fields = ["name"]
    template_name = "musiclibrary/add-genre.html"
    success_url = reverse_lazy("music")


def get_genres(request):
    if request.method == "GET":
        categories = Genre.objects.filter(user=request.user)
        response = {}
        count = 0
        for category in categories:
            response[count] = [category.pk, category.name]
            count += 1
    return JsonResponse(response)
