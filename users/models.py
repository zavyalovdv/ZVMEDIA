from django.contrib.auth.models import User
from booklibrary.const import *
from simple_history import register
from django.db import models


register(User)


class UserProfileSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    book_verbose_type = models.BooleanField(
        verbose_name="Просмотрщик книг", choices=BOOK_VERBOSE_TYPE, default=True
    )
    order_by = models.CharField(
        verbose_name="Поле для сортировки", max_length=200, blank=True, null=True
    )
    is_reverse_order_by = models.BooleanField(
        verbose_name="Прямой или обратный порядок сортировки", blank=True, null=True
    )
