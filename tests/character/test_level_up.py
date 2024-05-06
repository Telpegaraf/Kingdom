from rest_framework import status
from django.urls import reverse
from apps.character.models import Character
from rest_framework.test import APITestCase


class LevelUpTestCase(APITestCase):

    fixtures = [
        'fixtures/test_db.json'
    ]

    def setUp(self) -> None:
        self.character = Character.objects.first()
        self.client.login(username='admin', password='admin')
        self.url = reverse('level-up', kwargs={'character_id': self.character.id})
        self.data = {
            "level": self.character.level + 1,
        }
        self.wrong_data = {
            "level": 21
        }

    def test_level_up(self):
        response = self.client.patch(self.url, self.data, format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username='User', password='admin')
        response = self.client.patch(self.url, self.data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_wrong_data(self):
        response = self.client.patch(self.url, self.wrong_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
