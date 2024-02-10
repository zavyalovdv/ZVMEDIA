from django.db import models

class Book(models.Model):
    book_name = models.CharField(max_length=200, unique=True)
    book_path = models.CharField(max_length=300,unique=True)
    book_author = models.ManyToManyField("Author")
    book_category = models.ForeignKey("BookCategory", on_delete=models.CASCADE)
    book_genre = models.ForeignKey("BookGenre",on_delete=models.CASCADE)

    def __str__(self):
        return self.book_name

class Author(models.Model):
    author_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.author_name

class BookCategory(models.Model):
    book_category_name = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.book_category_name


class BookGenre(models.Model):
    book_genre_name = models.CharField(max_length=200, unique=200)
    book_category = models.ForeignKey(BookCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.book_genre_name
