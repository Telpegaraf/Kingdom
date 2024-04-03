from rest_framework import status
from django.urls import reverse
from apps.character.models import InventoryItems, CharacterBag, EquippedItems
from rest_framework.test import APITestCase
from apps.equipment.models import PlateArmor, Weapon, WornItems


class UnEquipItemTestCase(APITestCase):

    fixtures = [
        'fixtures/test_db.json'
    ]

    def setUp(self) -> None:
        self.bag = CharacterBag.objects.first()
        self.client.login(username='admin', password='admin')
        self.armor_url = reverse('un-equip-armor', kwargs={'character_id': self.bag.id})
        self.weapon_url = reverse('un-equip-first', kwargs={'character_id': self.bag.id})
        self.weapon_two_url = reverse('un-equip-second', kwargs={'character_id': self.bag.id})
        self.weapon = Weapon.objects.first()
        self.worn = WornItems.objects.first()
        self.armor = PlateArmor.objects.first()
        InventoryItems.objects.create(bag_id=self.bag.id, item=self.armor)
        equipped = EquippedItems.objects.get(bag_id=self.bag.id)
        equipped.plate_armor = InventoryItems.objects.last()
        InventoryItems.objects.create(bag_id=self.bag.id, item=self.weapon)
        equipped.first_weapon = InventoryItems.objects.last()
        InventoryItems.objects.create(bag_id=self.bag.id, item=self.worn)
        worn = InventoryItems.objects.last()
        equipped.worn_items.add(worn)
        self.worn_url = reverse('un-equip-worn', kwargs={'character_id': self.bag.id, 'item_id': worn.id})
        self.data = {
            "bag_id": self.bag.id,
            'item_id': self.armor.id
        }
        self.weapon_data = {
            "bag_id": self.bag.id,
            "item": self.weapon.id,
        }

    def test_un_equip_item(self):
        response = self.client.patch(self.armor_url)
        assert response.status_code == status.HTTP_200_OK
        response = self.client.patch(self.weapon_url)
        assert response.status_code == status.HTTP_200_OK
        response = self.client.delete(self.worn_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username='User', password='admin')
        response = self.client.patch(self.armor_url, self.data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
