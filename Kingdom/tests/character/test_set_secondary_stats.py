from rest_framework import status
from django.urls import reverse
from apps.character.models import SecondaryStats
from rest_framework.test import APITestCase


class SetSecondaryTestCase(APITestCase):

    fixtures = [
        'fixtures/test_db.json'
    ]

    def setUp(self) -> None:
        self.secondary_stats = SecondaryStats.objects.first()
        self.client.login(username='admin', password='admin')
        self.url = reverse('set-secondary-stats', kwargs={'character_id': self.secondary_stats.character_id})
        self.data = {
            "health": 4
        }

    def test_change_stats(self):
        health = self.secondary_stats.health
        response = self.client.patch(self.url, self.data, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.secondary_stats.refresh_from_db()
        assert self.secondary_stats.health != health

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username='User', password='admin')
        response = self.client.patch(self.url, self.data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
