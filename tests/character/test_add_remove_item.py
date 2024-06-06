from rest_framework import status
from django.urls import reverse
from apps.character.models import InventoryItems, CharacterBag
from rest_framework.test import APITestCase
from apps.equipment.models import PlateArmor, Weapon, WornItems


class AddItemTestCase(APITestCase):

    fixtures = [
        'fixtures/test_db.json'
    ]

    def setUp(self) -> None:
        self.bag = CharacterBag.objects.first()
        self.client.login(username='admin', password='admin')
        self.url = reverse('add-item', kwargs={'character_id': self.bag.id})
        self.weapon = Weapon.objects.first()
        self.worn = WornItems.objects.first()
        self.armor = PlateArmor.objects.first()
        self.data = {
            "item": self.armor.id,
            'quantity': 3
        }
        self.weapon_data = {
            "item": self.weapon.id,
        }

    def test_add_item(self):
        count = InventoryItems.objects.filter(bag_id=self.bag.id).count()
        response = self.client.post(self.url, data=self.data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert count != InventoryItems.objects.filter(bag_id=self.bag.id).count()
        item = InventoryItems.objects.last()
        assert item.quantity == self.data.get('quantity')

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username='User', password='admin')
        response = self.client.post(self.url, self.data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_wrong_data(self):
        response = self.client.post(self.url, data={'item': 999}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_quantity(self):
        count = InventoryItems.objects.filter(bag_id=self.bag.id).count()
        response = self.client.post(self.url, data=self.weapon_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert count != InventoryItems.objects.filter(bag_id=self.bag.id).count()
        item = InventoryItems.objects.last()
        assert item.quantity == 1

    def test_remove_item(self):
        count = InventoryItems.objects.filter(bag_id=self.bag.id).count()
        response = self.client.post(self.url, data=self.weapon_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert count != InventoryItems.objects.filter(bag_id=self.bag.id).count()
        item = InventoryItems.objects.last()
        assert item.quantity == 1
        item = InventoryItems.objects.filter(bag_id=self.bag.id).first()
        item_id = item.id
        remove_url = reverse('remove-item', kwargs={'item_id': item_id})
        response_remove = self.client.delete(remove_url, format='json')
        assert response_remove.status_code == status.HTTP_204_NO_CONTENT
        assert InventoryItems.objects.filter(bag_id=self.bag.id).count() == 0
