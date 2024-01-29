from django.test import TestCase
from apps.character.models import Character, Race, ClassCharacter
from apps.general.models import MasteryLevels, MoralIntentions
from apps.god.models import God


class CharacterModelTestCase(TestCase):
    fixtures = [
        'fixtures/test_db.json'
    ]

    def test_create_character(self):
        moral_intentions = MoralIntentions.objects.get(id=1)
        new_character = Character.objects.create(
            race=Race.objects.first(),
            first_name="Test name",
            class_player=ClassCharacter.objects.first(),
            age=18,
            god=God.objects.first(),
        )
        new_character.intentions.set([moral_intentions])

        assert new_character.first_name == "Test name"
