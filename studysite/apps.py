from django.apps import AppConfig


class StudysiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'studysite'

    def ready(self):
        import studysite.signals
