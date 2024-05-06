from rest_framework import status
from django.urls import reverse
from apps.character.models import CharacterStats
from rest_framework.test import APITestCase
from apps.general.models import MasteryLevels


class SetMastery(APITestCase):

    fixtures = [
        'fixtures/test_db.json'
    ]

    def setUp(self) -> None:
        self.character_stats = CharacterStats.objects.first()
        self.client.login(username='admin', password='admin')
        self.url = reverse('set-mastery', kwargs={'character_id': self.character_stats.character_id})
        self.data = {
            "reflex_mastery": MasteryLevels.LEGEND,
        }
        self.wrong_data = {
            "reflex_mastery": 'Legendary',
        }

    def test_change_stats(self):
        reflex_mastery = self.character_stats.reflex_mastery
        assert reflex_mastery != self.data.get('reflex_mastery')
        response = self.client.patch(self.url, self.data, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.character_stats.refresh_from_db()
        assert self.character_stats.reflex_mastery != reflex_mastery

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username='User', password='admin')
        response = self.client.patch(self.url, self.data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_wrong_data(self):
        response = self.client.patch(self.url, self.wrong_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
