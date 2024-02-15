from django.db import models


class Book(models.Model):
    book_name = models.CharField(max_length=200, unique=True)
    book_file = models.FileField(upload_to="book")
    book_path = models.CharField(max_length=300,unique=True)
    book_author = models.ManyToManyField("Author",related_name="book")
    book_category = models.ForeignKey("BookCategory", on_delete=models.PROTECT)
    book_genre = models.ForeignKey("BookGenre",on_delete=models.PROTECT)
    book_tag = models.ManyToManyField("BookTag", related_name="book", blank=True)
    book_slug = models.SlugField(max_length=255, unique=True)
    book_create_time = models.DateTimeField(auto_now_add=True)
    book_update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book_name
    
    class Meta:
        ordering = ['-book_create_time']
        indexes = [
            models.Index(fields=['-book_create_time'])
        ]


class Author(models.Model):
    author_name = models.CharField(max_length=200, unique=True,db_index=True)
    author_create_time = models.DateTimeField(auto_now_add=True)
    author_update_time = models.DateTimeField(auto_now=True)
    author_slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.author_name
    
    # def get_absolute_url(self):
    #     return reverse()


class BookCategory(models.Model):
    book_category_name = models.CharField(max_length=200, unique=True,db_index=True)
    book_category_slug = models.SlugField(max_length=255, unique=True)
    book_category_create_time = models.DateTimeField(auto_now_add=True)
    book_category_update_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.book_category_name
    
    # def get_absolute_url(self):
    #     return reverse()


class BookGenre(models.Model):
    book_genre_name = models.CharField(max_length=200, unique=200)
    book_category = models.ForeignKey(BookCategory, on_delete=models.CASCADE)
    book_genre_slug = models.SlugField(max_length=255, unique=True, db_index=True)
    book_genre_create_time = models.DateTimeField(auto_now_add=True)
    book_genre_update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book_genre_name
    
    # def get_absolute_url(self):
    #     return reverse()


class BookTag(models.Model):
    book_tag_name = models.CharField(max_length=200, unique=True, db_index=True)
    book_tag_slug = models.SlugField(max_length=255, unique=True)
    book_tag_create_time = models.DateTimeField(auto_now_add=True)
    book_tag_update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book_tag_name