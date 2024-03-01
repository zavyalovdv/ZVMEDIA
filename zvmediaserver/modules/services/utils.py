import os
from PyPDF2 import PdfReader, PdfWriter
import pathlib
from uuid import uuid4
from pytils.translit import slugify
from epub_conversion.utils import open_book, convert_epub_to_lines
from zvmediaserver.const import *
from ZVMEDIA.settings import BASE_DIR, MEDIA_ROOT


def unique_slugify_models(instance, pre_slug):
    """
    Автоматический генератор уникальных SLUG для моделей
    """
    model = instance.__class__
    unique_slug = slugify(pre_slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid4().hex[:8]}'
    return unique_slug


def save_extra_book_infodata(sender, instance):
    """ Заполняет дополнительную информацию о книге """
    if pathlib.Path(instance.file.path).suffix == ".pdf":
        pages_count = len(
            (PdfReader(open(f"{instance.file.path}", 'rb'))).pages)
    elif pathlib.Path(instance.file.path).suffix == ".epub":
        rows = convert_epub_to_lines(open_book(instance.file.path))
        words_count = 0
        for row in rows:
            words_count += len(row.split(" "))
        time_to_read = round(words_count / WORDS_PER_PAGE)

    words_count = pages_count * WORDS_PER_PAGE
    if instance.category.name == "Художественная":
        time_to_read = round(
            ((words_count / WORDS_PER_MINUTE_ART) / 60) * 10) / 10
    elif (instance.category.name == "Образовательная") or (instance.category.name == instance.category.name == "Учебная"):
        time_to_read = round(
            ((words_count / WORDS_PER_MINUTE_EDU) / 60) * 10) / 10
    else:
        time_to_read = round(
            ((words_count / WORDS_PER_MINUTE_ART) / 60) * 10) / 10
    instance.pages_count = pages_count
    instance.words_count = words_count
    instance.time_to_read = time_to_read
    return instance


def create_book_textdata(instance):
    if pathlib.Path(instance.file.path).suffix == ".pdf":
        pdf_object = (PdfReader(open(f"{instance.file.path}", 'rb'))).pages
        path = os.path.join(MEDIA_ROOT, 'book')
        book_doc = open(os.path.join(path, f"{instance.slug}.txt"), "a+")
        try:
            for page in pdf_object:
                book_doc.write(page.extract_text())
        except:
            print("worng")
        else:
            book_doc.close()
            
        # new_output_pdf_object = PdfWriter()
        # with open(instance.file.path, "wb") as f:
        #     new_output_pdf_object.add_js(
        #         "this.console.log('Hello from PDF');")
        #     new_output_pdf_object.write(f)
            
        output = PdfWriter()
        ipdf = PdfReader(open(f"{instance.file.path}", 'rb'))

        for i in range(len(ipdf.pages)):
            page = ipdf.pages[i]
            output.add_page(page)

        with open('new.pdf', 'wb') as f:
            output.add_js("console.log('hello from PDF')")
            output.write(f)
            
            
            
            
# def unique_slugify_forms(pre_slug):
#     """
#     Автоматический генератор уникальных SLUG
#     """
#     unique_slug = slugify(pre_slug)
#     while model.objects.filter(slug=unique_slug).exists():
#         unique_slug = f'{unique_slug}-{uuid4().hex[:8]}'
#     return unique_slug
