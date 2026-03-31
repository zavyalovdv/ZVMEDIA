from django.urls import path
from musiclibrary import views

urlpatterns = [
    path("", views.MainMusics.as_view(), name="music"),
    path("add-track/", views.AddTrack.as_view(), name="add_track"),
    path("add-genre/", views.AddGenre.as_view(), name="add_genre"),
    path("getgenres/", views.get_genres, name="get_genres"),
]
