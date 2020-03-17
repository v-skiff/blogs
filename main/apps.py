from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'
    verbose_name = 'Blog platform'

    def ready(self):
        import main.signals