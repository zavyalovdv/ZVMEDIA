import pathlib
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Book, BookAuthor
from zvmediaserver.const import *
from zvmediaserver.modules.services.utils import unique_slugify_models
from PyPDF2 import PdfReader
from epub_conversion.utils import open_book, convert_epub_to_lines


@receiver(post_save,sender=Book)
def save_extra_book_infodata(sender,instance,created,**kwargs):
    if created:
        if pathlib.Path(instance.file.path).suffix == ".pdf":
            pages_count = len((PdfReader(open(f"{instance.file.path}", 'rb'))).pages)
        elif pathlib.Path(instance.file.path).suffix == ".epub":
            rows = convert_epub_to_lines(open_book(instance.file.path))
            words_count = 0
            for row in rows:
                words_count += len(row.split(" "))
            time_to_read = round(words_count / WORDS_PER_PAGE)
        
        words_count = pages_count * WORDS_PER_PAGE
        if instance.category.name == "Художественная":
            time_to_read = round(((words_count / WORDS_PER_MINUTE_ART) / 60) * 10) / 10
        elif (instance.category.name == "Образовательная") or (instance.category.name == instance.category.name == "Учебная"):
            time_to_read = round(((words_count / WORDS_PER_MINUTE_EDU) / 60) * 10) / 10
        instance.pages_count = pages_count
        instance.words_count = words_count
        instance.time_to_read = time_to_read
        instance.save()
        
# @receiver(pre_save,sender=Book)
# def save_extra_book_modeldata(sender,instance,created,**kwargs):
#     print("Hello from pre_save t")
#     if not created:
#         print("Hello from pre_save f")
#         author, is_created = BookAuthor.objects.get_or_create(name=instance.name,slug=unique_slugify(instance, instance.name))
        