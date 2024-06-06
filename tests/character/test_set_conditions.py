from rest_framework import status
from django.urls import reverse
from apps.character.models import DefenceAndVulnerabilityDamage
from apps.general.models import DamageType
from rest_framework.test import APITestCase


class SetConditionsTestCase(APITestCase):

    fixtures = [
        'fixtures/test_db.json'
    ]

    def setUp(self) -> None:
        self.conditions = DefenceAndVulnerabilityDamage.objects.select_related('character').first()
        self.character = self.conditions.character
        self.client.login(username='admin', password='admin')
        self.url = reverse('set-condition', kwargs={'character_id': self.character.id})
        cold_damage_type = DamageType.objects.create(name='cold')
        acid_damage_type = DamageType.objects.create(name='acid')
        electricity_damage_type = DamageType.objects.create(name='electricity')
        self.data = {
            "immunity": [cold_damage_type.id],
            "resistance": [acid_damage_type.id],
            "weakness": [electricity_damage_type.id]
        }
        self.wrong_data = {
            "immunity": [cold_damage_type.id],
            "resistance": [cold_damage_type.id],
            "weakness": [cold_damage_type.id]
        }
        self.many_data = {
            "immunity": [cold_damage_type.id, electricity_damage_type.id],
            "resistance": [acid_damage_type.id],
        }

    def test_change_condition(self):
        immunity_before = list(self.conditions.immunity.all())
        resistance_before = list(self.conditions.resistance.all())
        weakness_before = list(self.conditions.weakness.all())

        response = self.client.patch(self.url, self.data, format='json')
        assert response.status_code == status.HTTP_200_OK

        self.conditions.refresh_from_db()
        immunity_after = list(self.conditions.immunity.all())
        resistance_after = list(self.conditions.resistance.all())
        weakness_after = list(self.conditions.weakness.all())

        assert immunity_after != immunity_before
        assert resistance_after != resistance_before
        assert weakness_after != weakness_before

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username='User', password='admin')
        response = self.client.patch(self.url, self.data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_wrong_data(self):
        response = self.client.patch(self.url, self.wrong_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_many_data(self):
        immunity_before = list(self.conditions.immunity.all())
        resistance_before = list(self.conditions.resistance.all())
        weakness_before = list(self.conditions.weakness.all())

        response = self.client.patch(self.url, self.many_data, format='json')
        assert response.status_code == status.HTTP_200_OK

        self.conditions.refresh_from_db()
        immunity_after = list(self.conditions.immunity.all())
        resistance_after = list(self.conditions.resistance.all())
        weakness_after = list(self.conditions.weakness.all())

        assert immunity_after != immunity_before
        assert resistance_after != resistance_before
        assert weakness_after == weakness_before
