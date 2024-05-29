from django.apps import AppConfig

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class CommonsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'commons'
    SETTING_KEY = 'COMMONS_APP_SETTINGS'
    REQUIRED_SETTINGS = ['API_KEY', 'ACM_BASE_URL']

    def ready(self):
        if not hasattr(settings, self.SETTING_KEY):
            raise ImproperlyConfigured(f"add {self.SETTING_KEY} in settings.py")
        app_settings = getattr(settings, self.SETTING_KEY)
        for setting in self.REQUIRED_SETTINGS:
            if setting not in app_settings:
                raise ImproperlyConfigured(f"add {setting} key to {self.SETTING_KEY} in settings.py")

