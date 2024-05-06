from rest_framework import status
from django.urls import reverse
from apps.character.models import CharacterStats
from rest_framework.test import APITestCase


class SetSpeed(APITestCase):

    fixtures = [
        'fixtures/test_db.json'
    ]

    def setUp(self) -> None:
        self.character_stats = CharacterStats.objects.first()
        self.client.login(username='admin', password='admin')
        self.url = reverse('set-speed', kwargs={'character_id': self.character_stats.character_id})
        self.data = {
            "speed": 35,
            "max_speed": 40
        }
        self.wrong_data = {
            "speed": 35,
            "max_speed": 30
        }

    def test_change_stats(self):
        speed = self.character_stats.speed
        max_speed = self.character_stats.max_speed
        response = self.client.patch(self.url, self.data, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.character_stats.refresh_from_db()
        assert self.character_stats.speed != speed
        assert self.character_stats.max_speed != max_speed

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username='User', password='admin')
        response = self.client.patch(self.url, self.data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_wrong_data(self):
        response = self.client.patch(self.url, self.wrong_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
