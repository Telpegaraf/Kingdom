from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.character.models import EquippedItems
from apps.character.serializers import CharacterOverallSerializer, CharacterDetailSerializer, CharacterSerializer, \
    AddItemSerializer, EquipItemSerializer, SecondaryStatsSerializer, LevelUpSerializer, SetStatsSerializer, \
    SetStatsDisplaySerializer, SetSpeedSerializer, SetMasterySerializer, CharacterSkillSerializer, \
    CharacterSkillMasterySerializer, SetFeatSerializer, SetSpellSerializer, SetConditionSerializer, \
    UnEquipSerializer, UnEquipWornItemSerializer

from apps.character.models import Character, SecondaryStats, CharacterStats, CharacterSkillList, CharacterSkillMastery,\
    CharacterFeatList, SpellList, DefenceAndVulnerabilityDamage, CharacterBag, InventoryItems
from apps.permissions import IsOwner


class CharacterOverallView(APIView):
    """ Show all characters """
    permission_classes = [IsAuthenticated]
    serializer_class = CharacterOverallSerializer

    def get(self, request, *args, **kwargs):
        character = Character.objects.all()
        serializer = self.serializer_class(character, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CharacterDetailView(APIView):
    """ Show detail info about character """
    permission_classes = [IsAuthenticated]
    serializer_class = CharacterDetailSerializer

    def get(self, request, character_id):
        character = get_object_or_404(Character, pk=character_id)
        serializer = self.serializer_class(character)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CharacterCreateView(APIView):
    """ Create new character """
    permission_classes = [IsAuthenticated]
    serializer_class = CharacterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SetStatsView(APIView):
    """ Sets stats, including when leveling up """
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class_display = SetStatsDisplaySerializer
    serializer_class = SetStatsSerializer

    def get(self, request, character_id):
        character = get_object_or_404(CharacterStats.objects.select_related('character'), character_id=character_id)
        serializer = self.serializer_class_display(character)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, character_id):
         character = get_object_or_404(CharacterStats.objects.select_related('character'), character_id=character_id)
         serializer = self.serializer_class(character, data=request.data, partial=True)
         serializer.is_valid(raise_exception=True)
         serializer.save()
         return Response(serializer.data, status=status.HTTP_200_OK)


class SetSpeedView(APIView):
    """ Set character's speed """
    permission_classes = [IsAuthenticated]
    serializer_class = SetSpeedSerializer

    def get(self, request, character_id):
        character = get_object_or_404(CharacterStats, character_id=character_id)
        serializer = self.serializer_class(character)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, character_id):
        character = get_object_or_404(CharacterStats, character_id=character_id)
        serializer = self.serializer_class(character, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SetMasteryView(APIView):
    """ Change mastery levels """
    permission_classes = [IsAuthenticated]
    serializer_class = SetMasterySerializer

    def get(self, request, character_id):
        character = get_object_or_404(CharacterStats, character_id=character_id)
        serializer = self.serializer_class(character)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, character_id):
        character = get_object_or_404(CharacterStats, character_id=character_id)
        serializer = self.serializer_class(character, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddItemView(APIView):
    """ Add new item in inventory """
    permission_classes = [IsAuthenticated]
    serializer_class = AddItemSerializer

    def get(self, request, character_id):
        bag = get_object_or_404(CharacterBag.objects.select_related('character').
                                prefetch_related('inventory'), character_id=character_id)
        serializer = self.serializer_class(bag.inventory.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, character_id):
        bag = get_object_or_404(CharacterBag.objects.select_related('character').
                                prefetch_related('inventory'), character_id=character_id)
        serializer = self.serializer_class(data=request.data,
                                           context={"inventory": bag})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RemoveItemView(APIView):
    """ Delete item from character's inventory """

    permission_classes = [IsAuthenticated, IsOwner]

    def delete(self, request, item_id):
        item = get_object_or_404(InventoryItems.objects.select_related('bag'), id=item_id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EquipItemView(APIView):
    """ Equip Item from inventory """
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = EquipItemSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": f"item equipped"}, status=status.HTTP_200_OK)


class BaseUnEquipView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = UnEquipSerializer
    un_equip_message = ""

    def patch(self, request, character_id):
        equipped_items = get_object_or_404(EquippedItems, bag_id=character_id)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('un_equip'):
            self.un_equip_item(equipped_items)
            return Response({"message": self.un_equip_message}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No changes made"}, status=status.HTTP_200_OK)

    def un_equip_item(self, equipped_items):
        raise NotImplementedError("Method un_equip_item must be implemented in child class")


class UnEquipArmorView(BaseUnEquipView):
    un_equip_message = "Armor unequipped successfully"

    def un_equip_item(self, equipped_items):
        equipped_items.plate_armor = None
        equipped_items.save()


class UnEquipFirstWeaponView(BaseUnEquipView):
    un_equip_message = "First weapon unequipped successfully"

    def un_equip_item(self, equipped_items):
        equipped_items.first_weapon = None
        equipped_items.save()


class UnEquipSecondWeaponView(BaseUnEquipView):
    un_equip_message = "Second weapon unequipped successfully"

    def un_equip_item(self, equipped_items):
        equipped_items.second_weapon = None
        equipped_items.save()


class SetSecondaryStatsView(APIView):
    """ Change characteristics (health and e.t.c) """

    permission_classes = [IsAuthenticated]
    serializer_class = SecondaryStatsSerializer

    def get(self, request, character_id):
        secondary_stats = get_object_or_404(SecondaryStats, character_id=character_id)
        serializer = self.serializer_class(secondary_stats)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, character_id):
        secondary_stats = get_object_or_404(SecondaryStats, character_id=character_id)
        serializer = self.serializer_class(secondary_stats, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteWornItemView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def delete(self, request, character_id, item_id):
        equipped_items = get_object_or_404(EquippedItems, bag_id=character_id)
        item_to_remove = get_object_or_404(equipped_items.worn_items, pk=item_id)
        equipped_items.worn_items.remove(item_to_remove)
        return Response({"message": "Item removed from worn items successfully"}, status=status.HTTP_204_NO_CONTENT)


class SecondaryStatsView(APIView):
    """ Display secondary characteristics """
    permission_classes = [IsAuthenticated]
    serializer_class = SecondaryStatsSerializer

    def get(self, request, character_id):
        secondary_stats = get_object_or_404(SecondaryStats, character_id=character_id)
        serializer = self.serializer_class(secondary_stats)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LevelUpView(APIView):
    """ Change character's level """

    permission_classes = [IsAuthenticated]
    serializer_class = LevelUpSerializer

    def get(self, request, character_id):
        character = get_object_or_404(Character, pk=character_id)
        serializer = self.serializer_class(character)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, character_id):
        character = get_object_or_404(Character.objects.select_related
                                      ('class_player', 'character_stats', 'secondary_stats'), pk=character_id)
        serializer = self.serializer_class(character, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class SetSkillsView(APIView):
    """ Set character's skills """

    permission_classes = [IsAuthenticated]
    serializer_class = CharacterSkillSerializer

    def put(self, request, character_id):
        character_skills = get_object_or_404(CharacterSkillList, character_id=character_id)
        serializer = self.serializer_class(character_skills, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SetSkillMasteryView(APIView):
    """ Set Character's skill mastery """

    permission_classes = [IsAuthenticated]
    serializer_class = CharacterSkillMasterySerializer

    def get(self, request, skill_id):
        mastery = get_object_or_404(CharacterSkillMastery.objects.select_related('skill_list'), id=skill_id)
        serializer = self.serializer_class(mastery)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, skill_id):
        mastery = get_object_or_404(CharacterSkillMastery.objects.select_related('skill_list'), id=skill_id)
        serializer = self.serializer_class(mastery, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SetFeatView(APIView):
    """ Set character's feat list """

    permission_classes = [IsAuthenticated]
    serializer_class = SetFeatSerializer

    def get(self, request, character_id):
        feat_list = get_object_or_404(CharacterFeatList.objects.
                                      select_related('character').
                                      prefetch_related('feat_class'), character_id=character_id)
        print(feat_list.character.class_player)
        print(feat_list.character.level)
        serializer = self.serializer_class(feat_list)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, character_id):
        feat_list = get_object_or_404(CharacterFeatList.objects.
                                      select_related('character').
                                      prefetch_related('feat_class'), character_id=character_id)
        serializer = self.serializer_class(feat_list,
                                           data=request.data,
                                           context={"class_player":feat_list.character.class_player,
                                                    "class_level": feat_list.character.level},
                                           partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SetSpellView(APIView):
    """ Set character's spell list """

    permission_classes = [IsAuthenticated]
    serializer_class = SetSpellSerializer

    def get(self, request, character_id):
        feat_list = get_object_or_404(SpellList, character_id=character_id)
        serializer = self.serializer_class(feat_list)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, character_id):
        feat_list = get_object_or_404(SpellList, character_id=character_id)
        serializer = self.serializer_class(feat_list, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SetCondition(APIView):
    """ Set character's defence and vulnerability """

    permission_classes = [IsAuthenticated]
    serializer_class = SetConditionSerializer

    def get(self, request, character_id):
        conditions = get_object_or_404(DefenceAndVulnerabilityDamage.objects.
                                       select_related('character'), character_id=character_id)
        serializer = self.serializer_class(conditions)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, character_id):
        conditions = get_object_or_404(DefenceAndVulnerabilityDamage.objects.
                                       select_related('character'), character_id=character_id)
        serializer = self.serializer_class(conditions, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['character_id'] = character_id
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
