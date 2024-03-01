import re
from django import forms
from django.forms import CharField, ModelForm, TextInput, FileInput, Select, SelectMultiple, MultipleChoiceField, ValidationError, modelform_factory
from zvmediaserver.modules.services.utils import unique_slugify_models
from .models import Book, BookAuthor, BookCategory, BookReadList, BookSubcategory


class AddBookForm(ModelForm):
    author = CharField(widget=TextInput, label="Автор")

    class Meta:
        model = Book
        fields = [
            'name', 'file', 'author', 'category', 'subcategory','reading_list']
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
                name=self.data['author'], slug=unique_slugify_models(self.instance, self.data['author']))
            if not author and not is_created:
                raise forms.ValidationError("Ошибка добавления автора")
        else:
            raise forms.ValidationError("Ошибка добавления автора")

        self.cleaned_data['author'] = BookAuthor.objects.filter(
            slug=author.slug)
        return self.cleaned_data


class AddBookCategoryForm(ModelForm):
    class Meta:
        model = BookCategory
        fields = ['name']
        widgets = {'name': TextInput(attrs={'class': 'form-control'})}


class AddBookSubcategoryForm(ModelForm):
    class Meta:
        model = BookSubcategory
        fields = ['name', 'category']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'category': Select(attrs={'class': 'form-control'}),
        }
class AddBookReadListForm(ModelForm):
    class Meta:
        model = BookReadList
        fields = ['name']
        widgets = {'name': TextInput(attrs={'class': 'form-control'})}
