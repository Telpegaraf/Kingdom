from rest_framework import status
from django.urls import reverse
from apps.character.models import SecondaryStats
from rest_framework.test import APITestCase


class ChangeStats(APITestCase):

    fixtures = [
        'fixtures/test_db.json'
    ]

    def setUp(self) -> None:
        self.secondary_stats = SecondaryStats.objects.last()
        self.client.login(username='admin', password='admin')
        self.url = reverse('change-stats', kwargs={'pk': self.secondary_stats.id})
        self.data = {
            "health": 4
        }

    def test_change_stats(self):
        health = self.secondary_stats.health
        response = self.client.patch(self.url, self.data, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.secondary_stats.refresh_from_db()
        assert self.secondary_stats.health != health

