from django.apps import AppConfig


class BooklibraryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "booklibrary"
    verbose_name = "Библиотека книг"

    # подключить сигналы Django
    def ready(self):
        import booklibrary.signals
