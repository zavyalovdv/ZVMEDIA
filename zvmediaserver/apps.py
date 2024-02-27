from django.apps import AppConfig


class ZvmediaserverConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'zvmediaserver'
    verbose_name = "Книги"

    # подключить сигналы Django
    def ready(self):
        import zvmediaserver.signals
