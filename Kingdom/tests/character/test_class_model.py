from django.test import TestCase
from apps.character.models import ClassCharacter
from apps.general.models import MasteryLevels


class ClassModelTestCase(TestCase):
    def test_create_class(self):
        new_class = ClassCharacter.objects.create(
            name="Test Class",
            health_by_level=8,
            perception_mastery=MasteryLevels.TRAIN,
            fortitude_mastery=MasteryLevels.ABSENT,
            reflex_mastery=MasteryLevels.TRAIN,
            will_mastery=MasteryLevels.EXPERT,
            unarmed_mastery=MasteryLevels.ABSENT,
            light_armor_mastery=MasteryLevels.TRAIN,
            medium_armor_mastery=MasteryLevels.TRAIN,
            heavy_armor_mastery=MasteryLevels.TRAIN
        )

        assert new_class.name == "Test Class"
        assert new_class.health_by_level == 8
        assert new_class.perception_mastery == MasteryLevels.TRAIN
        assert new_class.fortitude_mastery == MasteryLevels.ABSENT
        assert new_class.heavy_armor_mastery == MasteryLevels.TRAIN
