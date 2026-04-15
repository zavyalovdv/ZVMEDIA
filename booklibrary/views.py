import os
import json
from django.core.files.base import ContentFile
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.http import Http404, HttpResponse, HttpResponseNotFound, FileResponse
from django.http import JsonResponse
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    CreateView,
    UpdateView,
)
from django.shortcuts import get_object_or_404, redirect, render
from booklibrary.forms import (
    AddBookAuthorForm,
    AddBookCategoryForm,
    AddBookForm,
    AddBookSubcategoryForm,
    ChangeBookForm,
    UpdatedBookUploadForm,
)
from ZVMEDIA.settings import MEDIA_ROOT
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.urls import reverse_lazy
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from .models import Book


def get_last_week():
    now = timezone.now()
    last_week = now - timedelta(days=7)
    return last_week


def get_cuurent_datetime():
    now = timezone.now()
    return now


class ShowBooks(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    template_name = "booklibrary/books.html"
    context_object_name = "books"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["authors"] = Author.objects.filter(user=self.request.user)
        context["categories"] = Category.objects.filter(user=self.request.user)
        context["subcategories"] = Subcategory.objects.filter(user=self.request.user)
        context["favorites"] = Book.objects.filter(
            user=self.request.user, is_favorites=True
        )
        context["today"] = date.today()
        return context

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user).order_by("-create_time")


def show_detail_book(request, book_slug):
    try:
        book = get_object_or_404(Book, slug=book_slug)
        return FileResponse(
            open(os.path.join(MEDIA_ROOT, f"{book.file.name}"), "rb"),
            content_type="application/pdf",
        )
    except FileNotFoundError:
        raise Http404()


def book_init_as_pdf(request, book_slug):
    pdf_url = f"/books/getpdf/{book_slug}"
    try:
        book = Book.objects.get(slug=book_slug)
    except Exception as e:
        print("book_init_as_pdf: Book.objects.get(slug=book_slug): ZALUPA")
    # try:
    template = "booklibrary/init_detail_book.html"
    context = {
        "pdf_url": pdf_url,
        "slug": book_slug,
        "filename": str(book.file),
    }
    return render(request, template_name=template, context=context)
    # except:
    #     return render(request, template_name=template, context=context)


def book_reader_as_pdf(request, book_slug):
    pdf_url = f"/books/getpdf/{book_slug}"
    try:
        template = "booklibrary/detail_book_as_pdf.html"
        context = {"data": json.dumps(pdf_url, cls=DjangoJSONEncoder)}
        return render(request, template_name=template, context=context)
    except:
        return render(request, template_name=template, context=context)


def book_get_pdf(request, book_slug):
    book = Book.objects.get(slug=book_slug)
    file = book.file
    try:
        return FileResponse(file)
    except:
        return render(request, template_name="", context={"book": "error"})
    finally:
        book.status = "в процессе"
        book.save(update_fields=["status"])


def book_set_pdf(request, book_slug):
    if request.method == "POST":
        # УДАЛЯЕМ json.loads(request.body), файлы живут в request.FILES

        try:
            # 1. Ищем книгу
            book = Book.objects.get(slug=book_slug)

            # 2. Проверяем, прилетел ли файл
            if "book" not in request.FILES:
                return JsonResponse(
                    {"is_taken": False, "error": "No file uploaded"}, status=400
                )

            new_file = request.FILES["book"]

            if book.file and os.path.isfile(book.file.path):
                try:
                    os.remove(book.file.path)
                except OSError:
                    pass

            book.file = new_file
            book.save()

            return JsonResponse({"is_taken": True})

        except Book.DoesNotExist:
            return JsonResponse(
                {"is_taken": False, "error": "Book not found"}, status=404
            )
        except Exception as e:
            print(f"Ошибка сохранения PDF: {e}")
            return JsonResponse({"is_taken": False, "error": str(e)}, status=500)

    return JsonResponse({"is_taken": False, "error": "Invalid request"}, status=400)


@csrf_exempt
def ajax_update_extradata_book(request, book_slug):
    if request.method == "POST":
        data = json.load(request)
        book = Book.objects.get(slug=book_slug)
        current_time_spent = book.time_spent
        current_page = data["current_page"]
        progress = (current_page / book.pages_count) * 100
        update_time_spent = float((data["seconds"]) / 60) / 60
        book.time_spent = current_time_spent + update_time_spent
        book.current_page = current_page
        book.progress = float(f"{progress:.2f}")
        if book.progress == 100.00:
            book.status = "прочитана"
        try:
            book.save()
        except:
            response = {"is_taken": False}
        response = {"is_taken": True}
    return JsonResponse(response)


def book_change_favorite(request):
    is_favorites = request.GET["is_favorites"]
    book = Book.objects.get(slug=request.GET["slug"])
    if is_favorites == "False":
        book.is_favorites = False
    else:
        book.is_favorites = True
    try:
        book.save(update_fields=["is_favorites"])
    except:
        response = {"is_taken": False}
    response = {"is_taken": True}
    return JsonResponse(response)


class CreateBook(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    model = Book
    form_class = AddBookForm
    template_name = "booklibrary/add_book.html"
    success_url = "/books"
    context_object_name = "books"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = Book.objects.filter(user=self.request.user)
        context["categories"] = Category.objects.filter(user=self.request.user)
        context["user"] = self.request.user
        return context

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs["request"] = self.request
        return form_kwargs

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        form.save_m2m()
        return redirect(self.success_url)


class UpdateBook(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    model = Book
    form_class = ChangeBookForm
    template_name = "booklibrary/edit_book.html"
    success_url = "/books"
    context_object_name = "book"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['books'] = Book.objects.get(user=self.request.user)
        context["categories"] = Category.objects.filter(user=self.request.user)
        context["subcategories"] = Subcategory.objects.filter(
            user=self.request.user, category=context["object"].category
        )
        context["user"] = self.request.user
        return context

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs["request"] = self.request
        return form_kwargs

    def get_object(self, queryset=None):
        return Book.objects.get(user=self.request.user, slug=self.kwargs["book_slug"])

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        form.save_m2m()
        return redirect(self.success_url)


def delete_book(request, book_slug):
    # get_object_or_404 сразу выкинет 404, если слага нет, а не упадет с ошибкой
    book = get_object_or_404(Book, slug=book_slug)

    try:
        # Удаляем файл с диска перед удалением записи
        if book.file and os.path.isfile(book.file.path):
            os.remove(book.file.path)

            # Если хочешь удалить и папку со слагом (чтобы не плодить пустые папки):
            folder_path = os.path.dirname(book.file.path)
            if os.path.isdir(folder_path) and not os.listdir(folder_path):
                os.rmdir(folder_path)

        book.delete()

        if request.headers.get("x-requested-with") != "XMLHttpRequest":
            return redirect("books")

        return JsonResponse({"state": True, "url": "/books/"})

    except Exception as e:
        return JsonResponse({"state": False, "error": str(e)}, status=500)


class CreateBookAuthor(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    model = Author
    form_class = AddBookAuthorForm
    template_name = "booklibrary/add_book.html"
    success_url = "/books"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ShowBookCategory(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    template_name = "booklibrary/books_category.html"
    context_object_name = "books"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["authors"] = Author.objects.filter(user=self.request.user)
        context["categories"] = Category.objects.filter(user=self.request.user)
        context["subcategories"] = Subcategory.objects.filter(user=self.request.user)
        context["favorites"] = Book.objects.filter(
            user=self.request.user, is_favorites=True
        )
        context["today"] = date.today()
        return context

    def get_queryset(self):
        return Book.objects.filter(
            category__slug=self.kwargs["book_category_slug"]
        ).order_by("-create_time")


class ShowBookSubcategory(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    template_name = "booklibrary/books_subcategory.html"
    context_object_name = "books"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["authors"] = Author.objects.filter(user=self.request.user)
        context["categories"] = Category.objects.filter(user=self.request.user)
        context["subcategories"] = Subcategory.objects.filter(user=self.request.user)
        context["favorites"] = Book.objects.filter(
            user=self.request.user, is_favorites=True
        )
        context["today"] = date.today()
        return context

    def get_queryset(self):
        return Book.objects.filter(
            subcategory__slug=self.kwargs["book_subcategory_slug"]
        ).order_by("-create_time")


class ShowFavoriteBook(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    template_name = "booklibrary/books_category.html"
    context_object_name = "books"

    def get_queryset(self):
        qs = Book.objects.filter(user=self.request.user, is_favorites=True)
        print("--- DEBUG START ---")
        print(f"Request User: {self.request.user}")
        print(f"Is Authenticated: {self.request.user.is_authenticated}")
        print(f"Queryset Count: {qs.count()}")
        print(f"SQL Query: {qs.query}")  # Это покажет реальный SQL запрос
        print("--- DEBUG END ---")
        return qs


class CreateBookCategory(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    model = Category
    form_class = AddBookCategoryForm
    template_name = "booklibrary/add_category.html"
    success_url = "/books"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ShowBookAuthor(LoginRequiredMixin, ListView):
    model = Book
    template_name = "booklibrary/books_subcategory.html"
    context_object_name = "books"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Book.objects.filter(
            user=self.request.user, author__slug=self.kwargs["author_slug"]
        ).order_by("-create_time")


class CreateBookSubcategory(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    model = Book
    form_class = AddBookSubcategoryForm
    template_name = "booklibrary/add_subcategory.html"
    success_url = "/books"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def get_subcategory_by_category(request, category_slug):
    if request.method == "GET":
        user = request.user
        subcategories = Subcategory.objects.filter(
            user=user, category__slug=category_slug
        )
        response = {}
        count = 0
        for subcategory in subcategories:
            response[count] = [subcategory.pk, subcategory.name]
            count += 1
    return JsonResponse(response)


def get_categories(request):
    if request.method == "GET":
        categories = Category.objects.filter(user=request.user)
        response = {}
        count = 0
        for category in categories:
            response[count] = [category.pk, category.name]
            count += 1
    return JsonResponse(response)


def get_activity(request):
    if request.method == "GET":
        context = {}
        end_date = timezone.now()
        start_date = end_date - timedelta(days=6)
        datasets = []
        labels = []
        user = request.user
        books = Book.objects.filter(user=user)

        for book in books:
            object = {}
            object["values"] = []
            book_history = book.history.filter(history_date__gte=start_date)
            book_history_last = book_history.first()
            book_history_first = book_history.last()
            value = round(
                (book_history_last.time_spent - book_history_first.time_spent), 2
            )
            if value > 0.0:
                object["label"] = book.name
                object["values"].append(value)
                datasets.append(object)
                labels.append(book.name)
        context = {
            "dataset": datasets,
            "labels": labels,
            "authors": Author.objects.filter(user=request.user),
            "categories": Category.objects.filter(user=request.user),
            "subcategories": Subcategory.objects.filter(user=request.user),
            "favorites": Book.objects.filter(user=request.user, is_favorites=True),
            "today": date.today(),
        }

    return render(request, "booklibrary/last_activity.html", context=context)
