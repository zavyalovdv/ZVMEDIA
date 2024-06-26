import os
import json
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.http import Http404, HttpResponse, HttpResponseNotFound, FileResponse
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from zvmediaserver.forms import AddBookAuthorForm, AddBookCategoryForm, AddBookForm, AddBookReadingListForm, AddBookSubcategoryForm, ChangeBookForm, UpdatedBookUploadForm, UserLoginForm
from ZVMEDIA.settings import MEDIA_ROOT
from zvmediaserver.modules.services.utils import UserToFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.urls import reverse_lazy
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.contrib import messages


def get_last_week():
    now = timezone.now()
    last_week = now - timedelta(days=7)
    return last_week


def get_cuurent_datetime():
    now = timezone.now()
    return now


class ShowBooks(LoginRequiredMixin, ListView):
    template_name = "zvmedia/jinja2/books/books.html"
    context_object_name = 'books'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = BookAuthor.objects.filter(user=self.request.user)
        context['categories'] = BookCategory.objects.filter(
            user=self.request.user)
        context['subcategories'] = BookSubcategory.objects.filter(
            user=self.request.user)
        context['readinglists'] = BookReadingList.objects.filter(
            user=self.request.user)
        context['favorites'] = Book.objects.filter(
            user=self.request.user, is_favorites=True)
        context['tags'] = BookTag.objects.filter(user=self.request.user)
        context['today'] = date.today()
        return context

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)


def show_detail_book(request, book_slug):
    try:
        book = get_object_or_404(Book, slug=book_slug)
        return FileResponse(
            open(os.path.join(MEDIA_ROOT, f'{book.file.name}'), 'rb'),
            content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()


def book_init_as_pdf(request, book_slug):
    pdf_url = f'/books/getpdf/{book_slug}'
    try:
        template = 'zvmedia/jinja2/books/init_detail_book.html'
        context = {
            'pdf_url': json.dumps(pdf_url, cls=DjangoJSONEncoder),
            'slug': json.dumps(book_slug, cls=DjangoJSONEncoder),
        }
        return render(request, template_name=template, context=context)
    except:
        return render(request, template_name=template, context=context)
    else:
        my_file.close()


def book_reader_as_pdf(request, book_slug):
    pdf_url = f'/books/getpdf/{book_slug}'
    try:
        template = 'zvmedia/jinja2/books/detail_book_as_pdf.html'
        context = {
            'my_data': json.dumps(pdf_url, cls=DjangoJSONEncoder)
        }
        return render(request, template_name=template, context=context)
    except:
        return render(request, template_name=template, context=context)
    else:
        my_file.close()


def book_get_pdf(request, book_slug):
    book = Book.objects.get(slug=book_slug)
    print(book_slug)
    file = book.file
    try:
        return FileResponse(file)
    except:
        return render(request, template_name="", context={'book': 'error'})
    else:
        my_file.close()
    finally:
        book.status = "в процессе"
        book.save(update_fields=["status"])


@csrf_exempt
def book_set_pdf(request, book_slug):
    if request.method == 'POST':
        book = Book.objects.get(slug=book_slug)
        try:
            book_path = book.file.path
            filename = (book.file.name).split('/')[1]
            # filename = book.file.name
            # book.file.name = filename.split('/')[1]
            book.file = request.FILES['book']
            # with open(f'{book_path}', 'rb+') as b:
            #     file_obj = File(b)
            #     book.file.save('book_path', file_obj, save=True)
            book.file.name = filename
            os.remove(book_path)
            book.save(update_fields=["file"])
            # path = os.path.join(MEDIA_ROOT, 'book')
            # doc = open(os.path.join(path, f"{book.slug}.txt"), "r")
            # print(os.path.join(path, f"{book.slug}.txt"))
        except:
            response = {'is_taken': False}
    response = {
        'is_taken': True
    }
    return JsonResponse(response)


@csrf_exempt
def ajax_update_extradata_book(request, book_slug):
    if request.method == "POST":
        ajax_request = json.load(request)
        book = Book.objects.get(slug=book_slug)
        current_time_spent = book.time_spent
        current_page = ajax_request['current_page']
        progress = ((current_page / book.pages_count) * 100)
        update_time_spent = float((ajax_request['seconds'])/60)/60
        book.time_spent = current_time_spent + update_time_spent
        book.current_page = current_page
        book.progress = float(f"{progress:.2f}")
        print(get_cuurent_datetime())
        if (book.progress == 100.00):
            book.status = "прочитана"
        try:
            book.save()
        except:
            response = {'is_taken': False}
        response = {
            'is_taken': True
        }
    return JsonResponse(response)


def book_change_favorite(request):
    is_favorites = request.GET['is_favorites']
    book = Book.objects.get(slug=request.GET['slug'])
    if is_favorites == 'False':
        book.is_favorites = False
    else:
        book.is_favorites = True
    try:
        book.save(update_fields=["is_favorites"])
    except:
        response = {'is_taken': False}
    response = {
        'is_taken': True
    }
    return JsonResponse(response)


class CreateBook(LoginRequiredMixin, CreateView):
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    model = Book
    form_class = AddBookForm
    template_name = 'zvmedia/jinja2/books/add_book.html'
    success_url = "/books"
    context_object_name = 'books'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(user=self.request.user)
        context['categories'] = BookCategory.objects.filter(
            user=self.request.user)
        context['user'] = self.request.user
        context['reading_list'] = BookReadingList.objects.filter(
            user=self.request.user)
        return context

    def get_queryset(self):
        return BookCategory.objects.filter(user=self.request.user)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs['request'] = self.request
        return form_kwargs

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        form.save_m2m()
        return redirect(self.success_url)


class UpdateBook(LoginRequiredMixin, UpdateView):
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    model = Book
    form_class = ChangeBookForm
    template_name = 'zvmedia/jinja2/books/edit_book.html'
    success_url = "/books"
    context_object_name = 'book'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['books'] = Book.objects.get(user=self.request.user)
        context['categories'] = BookCategory.objects.filter(
            user=self.request.user)
        context['subcategories'] = BookSubcategory.objects.filter(
            user=self.request.user, category=context['object'].category)
        context['user'] = self.request.user
        context['reading_list'] = BookReadingList.objects.filter(
            user=self.request.user)
        return context

    def get_queryset(self):
        return BookCategory.objects.filter(user=self.request.user)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs['request'] = self.request
        return form_kwargs

    def get_object(self, queryset=None):
        return Book.objects.get(user=self.request.user, slug=self.kwargs['book_slug'])

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        form.save_m2m()
        return redirect(self.success_url)


def delete_book(request, book_slug):
    if request.method == 'POST':
        try:
            Book.objects.get(slug=book_slug).delete()
        except:
            response = {'state': False}
    response = {'state': True}
    return redirect("books")


class CreateBookAuthor(LoginRequiredMixin, CreateView):
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    model = BookAuthor
    form_class = AddBookAuthorForm
    template_name = 'zvmedia/jinja2/books/add_book.html'
    success_url = "/books"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ShowBookCategory(LoginRequiredMixin, ListView):
    template_name = "zvmedia/jinja2/books/books_category.html"
    context_object_name = 'books'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = BookAuthor.objects.filter(user=self.request.user)
        context['categories'] = BookCategory.objects.filter(
            user=self.request.user)
        context['subcategories'] = BookSubcategory.objects.filter(
            user=self.request.user)
        context['readinglists'] = BookReadingList.objects.filter(
            user=self.request.user)
        context['tags'] = BookTag.objects.filter(user=self.request.user)
        context['favorites'] = Book.objects.filter(
            user=self.request.user, is_favorites=True)
        return context

    def get_queryset(self):
        return Book.objects.filter(category__slug=self.kwargs['book_category_slug'])


class CreateBookCategory(LoginRequiredMixin, CreateView):
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    model = BookCategory
    form_class = AddBookCategoryForm
    template_name = 'zvmedia/jinja2/books/add_category.html'
    success_url = "/books"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ShowBookSubcategory(ListView):
    template_name = "zvmedia/jinja2/books/books_subcategory.html"
    context_object_name = 'books'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        subcategory = context['books'][0].subcategory
        context['title'] = self.kwargs['book_subcategory_slug']
        return context

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user, subcategory__slug=self.kwargs['book_subcategory_slug'])


class ShowBookAuthor(LoginRequiredMixin, ListView):
    model = Book
    template_name = "zvmedia/jinja2/books/books_subcategory.html"
    context_object_name = 'books'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user, author__slug=self.kwargs['author_slug'])


class CreateBookSubcategory(LoginRequiredMixin, CreateView):
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    model = Book
    form_class = AddBookSubcategoryForm
    template_name = 'zvmedia/jinja2/books/add_subcategory.html'
    success_url = "/books"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CreateBookReadingList(LoginRequiredMixin, CreateView):
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    model = BookReadingList
    form_class = AddBookReadingListForm
    template_name = 'zvmedia/jinja2/books/add_readlist.html'
    success_url = "/books"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DetailBookReadingList(LoginRequiredMixin, DetailView):
    model = BookReadingList
    context_object_name = "readinglist"
    template_name = 'zvmedia/jinja2/books/detail_readinglist.html'

    def get_object(self, queryset=None):
        return BookReadingList.objects.get(user=self.request.user, slug=self.kwargs['readinglist_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = BookAuthor.objects.filter(user=self.request.user)
        context['categories'] = BookCategory.objects.filter(
            user=self.request.user)
        context['subcategories'] = BookSubcategory.objects.filter(
            user=self.request.user)
        context['readinglists'] = BookReadingList.objects.filter(
            user=self.request.user)
        context['tags'] = BookTag.objects.filter(user=self.request.user)
        context['favorites'] = Book.objects.filter(
            user=self.request.user, is_favorites=True)
        # context['book_sequence'] = BookOrderingInReadingList.objects.filter(
        #     user=self.request.user,reading_list__slug=self.kwargs['readinglist_slug']).order_by('position')
        return context


def index(request):
    return render(request, "zvmedia/index.html")


def userlogin(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Успешный вход')
            return redirect('books')
        else:
            messages.error(request, 'Ошибка входа')
    else:
        form = UserLoginForm()
    return render(request, template_name="zvmedia/login.html", context={'form': form})


def userlogout(request):
    logout(request)
    return redirect('login')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def get_subcategory_by_category(request, category_slug):
    if request.method == "GET":
        user = request.user
        subcategories = BookSubcategory.objects.filter(
            user=user, category__slug=category_slug)
        response = {}
        count = 0
        for subcategory in subcategories:
            response[count] = [subcategory.pk, subcategory.name]
            count += 1
    return JsonResponse(response)


def get_categories(request):
    if request.method == "GET":
        categories = BookCategory.objects.filter(
            user=request.user)
        response = {}
        count = 0
        for category in categories:
            response[count] = [category.pk, category.name]
            count += 1
    return JsonResponse(response)


def get_activity(request):
    if request.method == "GET":
        end_date = timezone.now()
        start_date = end_date - timedelta(days=6)
        visited = []
        datasets = []
        labels = []
        values = []
        # datasets['dates'] = []
        # datasets['labels'] = []
        # datasets['names'] = []
        user = request.user
        books = Book.objects.filter(user=user)
        for book in books:
            # data = []
            object = {}            
            object["label"] = book.name
            object["values"] = []
            try:
                book_history = book.history.filter(history_date__gte=start_date)
                book_history_last = book_history.first()
                book_history_first = book_history.last()
                value = book_history_last.time_spent - book_history_first.time_spent
                object['values'].append(value)
            except:
                object['values'].append(0.0)
                object['values'].append(0.0)
                    
            # data.append(object)
            datasets.append(object)
            labels.append(book.name)
            
                       
        context = {"dataset": datasets,"labels": labels}
        print(context)
        # print(labels)
    return render(request, "zvmedia/jinja2/books/last_activity.html", context=context)


















# def get_activity(request):
#     if request.method == "GET":
#         now = timezone.now()
#         delta7days = now - timedelta(days=6)
#         json_response = {}
#         json_response["books"] = []
#         json_response["dates"] = []
#         json_response["data"] = []
#         count = 0
#         user = request.user
       
#         for day in range(7):
#             date = delta7days + timedelta(days=day)
#             books_histories = Book.history.as_of(date)
#             date_str = f"{date.day}.{date.month}.{date.year}"
#             json_response["dates"].append(date_str)
#             for book_history in books_histories:
#                 if not book_history.name in json_response["books"]:
#                     json_response["books"].append(book_history.name)
#                 json_response["data"].append({
#                     "name": book_history.name,
#                     "date": date_str,
#                     "value": book_history.time_spent,
#                 })
#         context = {"dataset": json_response}
#         print(context)
#     return render(request, "zvmedia/jinja2/books/last_activity.html", context=context)