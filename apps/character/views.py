from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.character.models import EquippedItems
from apps.character import serializers
from apps.character import models as character_models
from apps.permissions import IsOwner


class CharacterOverallView(APIView):
    """ Show all characters """
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CharacterOverallSerializer

    def get(self, request, *args, **kwargs):
        character = character_models.Character.objects.all()
        serializer = self.serializer_class(character, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CharacterDetailView(APIView):
    """ Show detail info about character """
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CharacterDetailSerializer

    def get(self, request, character_id):
        character = get_object_or_404(character_models.Character, pk=character_id)
        serializer = self.serializer_class(character)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CharacterCreateView(APIView):
    """ Create new character """
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CharacterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data,
                                           context={'user': request.user}
                                           )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='character_id', description='character_id', type=int),
        ]
    ),
    patch=extend_schema(
        parameters=[
            OpenApiParameter(name='character_id', description='character_id', type=int),
        ]
    )
)
class ChangeStatView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class_display = serializers.SetStatsDisplaySerializer
    serializer_class = serializers.ChangeStatSerializer

    def get(self, request):
        character_id = request.query_params.get('character_id')
        character = get_object_or_404(character_models.CharacterStats.objects.select_related('character')
                                      , character_id=character_id)
        serializer = self.serializer_class_display(character)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        character_id = request.query_params.get('character_id')
        character_stats = get_object_or_404(character_models.CharacterStats.objects.
                                            select_related('character__character_stat_points')
                                            , character_id=character_id)

        if not IsOwner().has_object_permission(request, self, character_stats):
            return Response({"error": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(instance=character_stats, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='character_id', description='character_id', type=int),
        ]
    )
)
class SetSpeedView(APIView):
    """ Set character's speed """
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = serializers.SetSpeedSerializer

    def get(self, request):
        character_id = request.query_params.get('character_id')
        character = get_object_or_404(character_models.CharacterStats, character_id=character_id)
        serializer = self.serializer_class(character)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        character_id = request.query_params.get('character_id')
        character = get_object_or_404(character_models.CharacterStats, character_id=character_id)
        if not IsOwner().has_object_permission(request, self, character):
            return Response({"error": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(character, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SetMasteryView(APIView):
    """ Change mastery levels """
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = serializers.SetMasterySerializer

    def get(self, request, character_id):
        character = get_object_or_404(character_models.CharacterStats, character_id=character_id)
        serializer = self.serializer_class(character)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, character_id):
        character = get_object_or_404(character_models.CharacterStats, character_id=character_id)
        if not IsOwner().has_object_permission(request, self, character):
            return Response({"error": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(character, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddItemView(APIView):
    """ Add new item in inventory """
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = serializers.AddItemSerializer

    def get(self, request, character_id):
        bag = get_object_or_404(character_models.CharacterBag.objects.select_related('character').
                                prefetch_related('inventory'), character_id=character_id)
        serializer = self.serializer_class(bag.inventory.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, character_id):
        bag = get_object_or_404(character_models.CharacterBag.objects.select_related('character').
                                prefetch_related('inventory'), character_id=character_id)
        if not IsOwner().has_object_permission(request, self, bag):
            return Response({"error": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(data=request.data,
                                           context={"inventory": bag})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RemoveItemView(APIView):
    """ Delete item from character's inventory """

    permission_classes = [IsAuthenticated, IsOwner]

    def delete(self, request, item_id):
        item = get_object_or_404(character_models.InventoryItems.objects.select_related('bag'), id=item_id)
        if not IsOwner().has_object_permission(request, self, item.bag):
            return Response({"error": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EquipItemView(APIView):
    """ Equip Item from inventory """
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = serializers.EquipItemSerializer

    def post(self, request, *args, **kwargs):
        bag = get_object_or_404(character_models.CharacterBag, id=request.data.get('bag_id'))
        if not IsOwner().has_object_permission(request, self, bag):
            return Response({"error": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": f"item equipped"}, status=status.HTTP_201_CREATED)


class BaseUnEquipView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = serializers.UnEquipSerializer
    un_equip_message = ""

    def patch(self, request, character_id):
        equipped_items = get_object_or_404(EquippedItems, bag_id=character_id)
        if not IsOwner().has_object_permission(request, self, equipped_items):
            return Response({"error": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
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

    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = serializers.SecondaryStatsSerializer

    def get(self, request, character_id):
        secondary_stats = get_object_or_404(character_models.SecondaryStats, character_id=character_id)
        serializer = self.serializer_class(secondary_stats)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, character_id):
        secondary_stats = get_object_or_404(character_models.SecondaryStats, character_id=character_id)
        if not IsOwner().has_object_permission(request, self, secondary_stats):
            return Response({"error": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(secondary_stats, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteWornItemView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def delete(self, request, character_id, item_id):
        equipped_items = get_object_or_404(EquippedItems, bag_id=character_id)
        if not IsOwner().has_object_permission(request, self, equipped_items):
            return Response({"error": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        item_to_remove = get_object_or_404(equipped_items.worn_items, pk=item_id)
        equipped_items.worn_items.remove(item_to_remove)
        return Response({"message": "Item removed from worn items successfully"}, status=status.HTTP_204_NO_CONTENT)


class SecondaryStatsView(APIView):
    """ Display secondary characteristics """
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = serializers.SecondaryStatsSerializer

    def get(self, request, character_id):
        secondary_stats = get_object_or_404(character_models.SecondaryStats, character_id=character_id)
        if not IsOwner().has_object_permission(request, self, secondary_stats):
            return Response({"error": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(secondary_stats)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LevelUpView(APIView):
    """ Change character's level """

    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = serializers.LevelUpSerializer

    def get(self, request, character_id):
        character = get_object_or_404(character_models.Character, pk=character_id)
        serializer = self.serializer_class(character)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, character_id):
        character = get_object_or_404(character_models.Character.objects.select_related
                                      ('class_player', 'character_stats', 'secondary_stats'), pk=character_id)
        if not IsOwner().has_object_permission(request, self, character):
            return Response({"error": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(character, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class SetSkillsView(APIView):
    """ Set character's skills """

    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = serializers.CharacterSkillSerializer

    def patch(self, request, character_id):
        character_skills = get_object_or_404(character_models.CharacterSkillList, character_id=character_id)
        if not IsOwner().has_object_permission(request, self, character_skills):
            return Response({"error": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(character_skills, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SetSkillMasteryView(APIView):
    """ Set Character's skill mastery """

    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = serializers.CharacterSkillMasterySerializer

    def get(self, request, skill_id):
        mastery = get_object_or_404(character_models.CharacterSkillMastery.objects.select_related('skill_list')
                                    , id=skill_id)
        serializer = self.serializer_class(mastery)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, skill_id):
        mastery = get_object_or_404(character_models.CharacterSkillMastery.objects.select_related('skill_list')
                                    , id=skill_id)
        if not IsOwner().has_object_permission(request, self, mastery):
            return Response({"error": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(mastery, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SetFeatView(APIView):
    """ Set character's feat list """

    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = serializers.SetFeatSerializer

    def get(self, request, character_id):
        feat_list = get_object_or_404(character_models.CharacterFeatList.objects.
                                      select_related('character').
                                      prefetch_related('feat_class'), character_id=character_id)
        serializer = self.serializer_class(feat_list)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, character_id):
        feat_list = get_object_or_404(character_models.CharacterFeatList.objects.
                                      select_related('character').
                                      prefetch_related('feat_class'), character_id=character_id)
        if not IsOwner().has_object_permission(request, self, feat_list):
            return Response({"error": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(feat_list,
                                           data=request.data,
                                           context={"class_player":feat_list.character.class_player,
                                                    "class_level": feat_list.character.level},
                                           partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SetSpellView(APIView, IsOwner):
    """ Set character's spell list """

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.SetSpellSerializer

    def get(self, request, character_id):
        feat_list = get_object_or_404(character_models.SpellList, character_id=character_id)
        serializer = self.serializer_class(feat_list)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, character_id):
        feat_list = get_object_or_404(character_models.SpellList, character_id=character_id)
        if not IsOwner().has_object_permission(request, self, feat_list):
            return Response({"error": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(feat_list, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SetCondition(APIView):
    """ Set character's defence and vulnerability """

    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = serializers.SetConditionSerializer

    def get(self, request, character_id):
        conditions = get_object_or_404(character_models.DefenceAndVulnerabilityDamage.objects.
                                       select_related('character'), character_id=character_id)
        serializer = self.serializer_class(conditions)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, character_id):
        conditions = get_object_or_404(character_models.DefenceAndVulnerabilityDamage.objects.
                                       select_related('character'), character_id=character_id)
        if not IsOwner().has_object_permission(request, self, conditions):
            return Response({"error": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(conditions, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
