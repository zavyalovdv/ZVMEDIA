from mutagen import File as MutagenFile
from django.core.files.base import ContentFile
from musiclibrary.models import Album, Artist, Track


def extract_metadata(object):
    try:
        audio = MutagenFile(object.file.path, easy=True)
        if audio is None:
            print("не удалось прочитать файл")
            return

        object.file_name = object.file.path.split("/")[-1]
        object.format = object.file_name.split(".")[-1].upper()

        object.title = audio.get("title", [None])[0] or object.file_name.split(".")[0]
        raw_artist = audio.get("artist", ["Unknown Artist"])[0]
        raw_album = audio.get("album", ["Unknown Album"])[0]
        artist_obj, _ = Artist.objects.get_or_create(name=raw_artist)
        album_obj, _ = Album.objects.get_or_create(artist=artist_obj, title=raw_album)
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
        object.save()
        # # Обложку тянем только если у альбома её еще нет
        # if not album.cover:
        #     # Для обложек EasyID3 не подходит, нужно переоткрыть файл
        #     full_audio = MutagenFile(self.file.path)
        #     self.extract_cover(full_audio, album)

    except Exception as e:
        print(f"Ошибка парсинга тегов: {e}")


def extract_cover(self, audio, album):
    # Логика извлечения картинки зависит от формата (APIC для MP3, picture для FLAC)
    cover_data = None
    if "APIC:" in audio:  # MP3
        cover_data = audio.get("APIC:").data
    elif hasattr(audio, "pictures") and audio.pictures:  # FLAC
        cover_data = audio.pictures[0].data

    if cover_data:
        album.cover.save(f"{album.title}.jpg", ContentFile(cover_data), save=True)
