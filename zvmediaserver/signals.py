import pathlib
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Book, BookAuthor
from zvmediaserver.const import *
# from zvmediaserver.modules.services.utils import create_book_textdata
from PyPDF2 import PdfReader
from epub_conversion.utils import open_book, convert_epub_to_lines
from zvmediaserver.modules.services.utils import save_extra_book_infodata


@receiver(post_save,sender=Book)
def extra_book_data(sender,instance,created,**kwargs):
    if created:
        extra_instance = save_extra_book_infodata(sender,instance)
        # create_book_textdata(instance)
        extra_instance.save()

# @receiver(pre_save,sender=Book)
# def save_extra_book_modeldata(sender,instance,created,**kwargs):
#     print("Hello from pre_save t")
#     if not created:
#         print("Hello from pre_save f")
#         author, is_created = BookAuthor.objects.get_or_create(name=instance.name,slug=unique_slugify(instance, instance.name))
        