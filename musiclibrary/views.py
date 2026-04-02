from django.http import HttpResponseRedirect, JsonResponse
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
        form.instance.user = self.request.user
        self.object = form.save()
        if self.object.file:
            services.extract_metadata(self.object)

        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        # Получаем список всех файлов из инпута
        files = request.FILES.getlist("file")

        if form.is_valid():
            # Если файлов нет, но форма валидна (например, только жанр выбрали)
            if not files:
                return self.form_invalid(form)

            for f in files:
                # Создаем объект в памяти, не сохраняя в БД
                track = Track(
                    user=request.user,
                    file=f,
                    genre=form.cleaned_data["genre"],
                    # Временный заголовок из имени файла, пока extract_metadata не вытащит теги
                    title=f.name,
                )

                # Сохраняем объект. Здесь сработает твой upload_to
                track.save()

                # Запускаем твой сервис (с pathlib и фиксом расширения)
                track = services.extract_metadata(track)
                services.rename_file(track)
                track.save()

            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


class AddGenre(CreateView):
    model = Genre
    fields = ["name"]
    template_name = "musiclibrary/add-genre.html"
    success_url = reverse_lazy("music")

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


def get_genres(request):
    if request.method == "GET":
        categories = Genre.objects.filter(user=request.user)
        response = {}
        count = 0
        for category in categories:
            response[count] = [category.pk, category.name]
            count += 1
    return JsonResponse(response)
