import re
from django import forms
from django.forms import CharField, ModelForm, TextInput, FileInput, Select, SelectMultiple, MultipleChoiceField, ValidationError, HiddenInput
from zvmediaserver.modules.services.utils import unique_slugify_models
from .models import Book, BookAuthor, BookCategory, BookReadingList, BookSubcategory
from django.contrib.auth.forms import AuthenticationForm


class AddBookForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    author = CharField(widget=TextInput, label="Автор")

    class Meta:
        model = Book
        fields = [
            'name', 'file', 'author', 'category', 'subcategory', 'reading_list']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'author': TextInput(attrs={'class': 'form-control'}),
            'category': Select(attrs={'class': 'form-control'}),
            'subcategory': SelectMultiple(attrs={'class': 'form-control'}),
            'reading_list': SelectMultiple(attrs={'class': 'form-control'}),
            'file': FileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        if self.data['author']:
            author, is_created = BookAuthor.objects.get_or_create(
                user=self.request.user, name=self.data['author'], slug=unique_slugify_models(self.instance, self.data['author']))
            if not author and not is_created:
                raise forms.ValidationError("Ошибка добавления автора")
        else:
            raise forms.ValidationError("Ошибка добавления автора")

        # self.cleaned_data['user'] = self.request.user
        self.cleaned_data['author'] = BookAuthor.objects.filter(
            slug=author.slug)
        return self.cleaned_data


class ChangeBookForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    author = CharField(widget=TextInput, label="Автор")

    class Meta:
        model = Book
        fields = [
            'name', 'file', 'author', 'category', 'subcategory', 'reading_list']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'author': TextInput(attrs={'class': 'form-control'}),
            'category': Select(attrs={'class': 'form-control'}),
            'subcategory': SelectMultiple(attrs={'class': 'form-control'}),
            'reading_list': SelectMultiple(attrs={'class': 'form-control'}),
            'file': FileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        if self.data['author']:
            author, is_created = BookAuthor.objects.get_or_create(
                user=self.request.user, name=self.data['author'], slug=unique_slugify_models(self.instance, self.data['author']))
            if not author and not is_created:
                raise forms.ValidationError("Ошибка добавления автора")
        else:
            raise forms.ValidationError("Ошибка добавления автора")

        # self.cleaned_data['user'] = self.request.user
        self.cleaned_data['author'] = BookAuthor.objects.filter(
            slug=author.slug)
        return self.cleaned_data


class AddBookAuthorForm(ModelForm):
    class Meta:
        model = BookAuthor
        fields = ['name']
        widgets = {'name': TextInput(attrs={'class': 'form-control'})}


class UpdatedBookUploadForm(forms.Form):
    file = forms.FileField()


class AddBookCategoryForm(ModelForm):
    class Meta:
        model = BookCategory
        fields = ['name']
        widgets = {'name': TextInput(attrs={'class': 'form-control'})}

    # def clean(self):
    #     print(self.user) # request now available here also
        # def clean_user(self):
        #     data = self.fields['user'] = '2'
        #     # data = self.cleaned_data.get('user') or self.fields['user'].initial
        # return data


class AddBookSubcategoryForm(ModelForm):
    class Meta:
        model = BookSubcategory
        fields = ['name', 'category']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'category': Select(attrs={'class': 'form-control'}),
        }


class AddBookReadingListForm(ModelForm):
    class Meta:
        model = BookReadingList
        fields = ['name']
        widgets = {'name': TextInput(attrs={'class': 'form-control'})}


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='Пароль', widget=forms.TextInput(attrs={'class': 'form-control'}))
