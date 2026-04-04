import os
from ZVMEDIA import settings
from mutagen import File as MutagenFile
from django.core.files.base import ContentFile
from musiclibrary.models import Album, Artist, Track
from pathlib import Path


def extract_metadata(object):
    # try:
    audio = MutagenFile(object.file.path, easy=True)
    if audio is None:
        print("не удалось прочитать файл")
        return

    file_name = object.file.path.split("/")[-1]
    file_title = file_name.split(".")[-0]
    file_format = file_name.split(".")[-1]

    if check_file_extension(file_format):
        file_format = fix_file_extension(file_format)
        file_name = f"{file_title}.{file_format.lower()}"

    raw_artist = audio.get("artist", ["Unknown Artist"])[0]
    raw_album = audio.get("album", ["Unknown Album"])[0]

    fix_album = fix_album_name(raw_album)

    object.file_name = file_name
    object.file_format = file_format
    object.title = audio.get("title", [None])[0] or object.file_name.split(".")[0]
    object.format = file_format.upper()
    artist_obj, _ = Artist.objects.get_or_create(name=raw_artist, user=object.user)
    album_obj, _ = Album.objects.get_or_create(
        artist=artist_obj, title=fix_album, user=object.user
    )
    object.date = audio.get("date", [None])[0]
    object.duration = getattr(audio.info, "length", 0)
    object.track_number = audio.get("tracknumber", [None])[0]
    object.disk = audio.get("disknumber", [None])[0]
    object.total_tracks = audio.get("totaltracks", [None])[0]
    object.bitrate = None
    object.genre = object.genre
    object.genre_auto_detect = audio.get("genre", ["Unknown"])[0]
    object.artist = artist_obj
    object.album = album_obj
    return object


def check_file_extension(raw_file_extension):
    print("In check_file_extension")
    if raw_file_extension.lower() == "flacon":
        return True


def fix_file_extension(raw_file_extension):
    if raw_file_extension.lower() == "flacon":
        new_file_extension = "flac"

    return new_file_extension


def rename_file(file):
    old_path = Path(file.file.path)
    if old_path.suffix.lower() == ".flacon":
        new_path = old_path.with_suffix(".flac")

        if old_path.exists():
            old_path.rename(new_path)

        file.file.name = str(new_path.relative_to(settings.MEDIA_ROOT))
        file.save(update_fields=["file"])


def fix_album_name(raw_album):
    if "(" in raw_album:
        return raw_album.split("(")[0].strip()
    return raw_album


def extract_cover(self, audio, album):
    # Логика извлечения картинки зависит от формата (APIC для MP3, picture для FLAC)
    cover_data = None
    if "APIC:" in audio:  # MP3
        cover_data = audio.get("APIC:").data
    elif hasattr(audio, "pictures") and audio.pictures:  # FLAC
        cover_data = audio.pictures[0].data

    if cover_data:
        album.cover.save(f"{album.title}.jpg", ContentFile(cover_data), save=True)
