from rest_framework import status
from django.urls import reverse
from apps.character.models import CharacterStats
from rest_framework.test import APITestCase


class SetStats(APITestCase):

    fixtures = [
        'fixtures/test_db.json'
    ]

    def setUp(self) -> None:
        self.stats = CharacterStats.objects.select_related('character').first()
        self.character = self.stats.character
        self.client.login(username='admin', password='admin')
        self.url = reverse('set-stats', kwargs={'character_id': self.stats.character_id})
        self.data = {
            "strength": 16
        }

    def test_change_stats(self):
        strength = self.stats.strength
        response = self.client.patch(self.url, self.data, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.stats.refresh_from_db()
        assert self.stats.strength != strength

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username='User', password='admin')
        response = self.client.patch(self.url, self.data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_first_level(self):
        response = self.client.patch(self.url, {"strength": 20}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_second_level(self):
        self.character.level = 2
        self.character.save()
        strength = self.stats.strength
        response = self.client.patch(self.url, {"strength": 20}, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.stats.refresh_from_db()
        assert self.stats.strength != strength
