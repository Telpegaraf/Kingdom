from rest_framework import status
from django.urls import reverse
from apps.character.models import InventoryItems, CharacterBag, EquippedItems
from rest_framework.test import APITestCase
from apps.equipment.models import Item, PlateArmor, Weapon, WornItems


class EquipItemTestCase(APITestCase):

    fixtures = [
        'fixtures/test_db.json'
    ]

    def setUp(self) -> None:
        self.bag = CharacterBag.objects.first()
        self.client.login(username='admin', password='admin')
        self.url = reverse('equip-item')
        self.weapon = Weapon.objects.first()
        self.worn = WornItems.objects.first()
        self.armor = PlateArmor.objects.first()
        self.data = {
            "bag_id": self.bag.id,
            'item_id': self.armor.id
        }
        self.weapon_data = {
            "bag_id": self.bag.id,
            "item": self.weapon.id,
        }

    def test_equip_item(self):
        armor = EquippedItems.objects.get(bag_id=self.bag.id)
        InventoryItems.objects.create(bag_id=self.bag.id, item=self.armor)
        response = self.client.post(self.url, data=self.data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert armor.plate_armor != EquippedItems.objects.get(bag_id=self.bag.id).plate_armor

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username='User', password='admin')
        response = self.client.post(self.url, self.data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_equip_without_item_in_inventory(self):
        response = self.client.post(self.url, data=self.data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_wrong_data(self):
        InventoryItems.objects.create(bag_id=self.bag.id, item=self.armor)
        response = self.client.post(self.url, data={"bag_id": 999, "item": self.weapon.id,}, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
