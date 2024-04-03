from django.apps import AppConfig
from django.core.signals import setting_changed


class CharacterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.character'

    def ready(self) -> None:
        import apps.character.signals
