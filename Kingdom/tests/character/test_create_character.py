from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from apps.character.models import Race, ClassCharacter
from apps.god.models import God


class CreateCharacterTest(APITestCase):
    fixtures = [
        'fixtures/test_db.json'
    ]

    def setUp(self):
        self.url = reverse('character-create')
        self.client.login(username='admin', password='admin')
        self.race = Race.objects.first()
        self.class_player = ClassCharacter.objects.first()
        self.god = God.objects.first()
        self.data={
           "race": 1,
           "first_name": "Test Name",
           "class_player": 1,
           "age": 18,
           "god": 1,
           "intentions": [1]

        }

    def test_create_client(self):
        response = self.client.post(self.url, self.data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['first_name'] == "Test Name"

    def test_no_auth(self):
        self.client.logout()
        response = self.client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_wrong_data(self):
        self.data['god'] = None
        response = self.client.post(self.url, self.data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
