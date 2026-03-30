import os
from PyPDF2 import PdfReader, PdfWriter
import pathlib
from uuid import uuid4
from pytils.translit import slugify
from epub_conversion.utils import open_book, convert_epub_to_lines
from booklibrary.const import *
from ZVMEDIA.settings import BASE_DIR, MEDIA_ROOT


def unique_slugify_models(instance, pre_slug):
    model = instance.__class__
    unique_slug = slugify(pre_slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{unique_slug}-{uuid4().hex[:8]}"
    return unique_slug


def save_extra_book_infodata(sender, instance):
    if pathlib.Path(instance.file.path).suffix == ".pdf":
        pages_count = len((PdfReader(open(f"{instance.file.path}", "rb"))).pages)
    elif pathlib.Path(instance.file.path).suffix == ".epub":
        rows = convert_epub_to_lines(open_book(instance.file.path))
        words_count = 0
        for row in rows:
            words_count += len(row.split(" "))
        time_to_read = round(words_count / WORDS_PER_PAGE)

    words_count = pages_count * WORDS_PER_PAGE
    time_to_read = round(((words_count / WORDS_PER_MINUTE_ART) / 60) * 10) / 10

    instance.pages_count = pages_count
    instance.words_count = words_count
    instance.time_to_read = time_to_read
    return instance


class UserToFormMixin(object):
    def get_form_kwargs(self):
        kwargs = super(UserToFormMixin, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs
