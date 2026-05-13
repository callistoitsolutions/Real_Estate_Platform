from django.apps import AppConfig

class AdminAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Admin_App'

    def ready(self):
        import seo.signals  # load signals when app is ready
