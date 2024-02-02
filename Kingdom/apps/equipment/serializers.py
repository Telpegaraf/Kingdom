from rest_framework import serializers
from apps.equipment.models import Item, Weapon, PlateArmor, WornItems


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name']


class PlateArmorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlateArmor
        fields = ['id', 'name']


class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = ['id', 'name']


class WornItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WornItems
        fields = ['id', 'name']


class PlateArmorDetailSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField()
    armor_traits = serializers.StringRelatedField(many=True)
    armor_specialization = serializers.StringRelatedField(many=True)

    class Meta:
        model = PlateArmor
        fields = ['id', 'name', 'description', 'price', 'currency', 'weight', 'category', 'ac_bonus',
                  'dexterity_modifier_cap', 'check_penalty', 'speed_penalty', 'strength', 'level', 'group',
                  'armor_traits', 'armor_specialization']


class WeaponDetailSerializer(serializers.ModelSerializer):
    weapon_traits = serializers.StringRelatedField(many=True)

    class Meta:
        model = Weapon
        fields = ['id', 'name', 'description', 'price', 'currency', 'weight', 'dice', 'dice_count', 'second_dice',
                  'second_dice_count', 'bonus_damage', 'second_bonus_damage', 'range', 'reload', 'two_hands', 'level',
                  'type_damage', 'second_type_damage', 'weapon_traits']


class WornItemsDetailSerializer(serializers.ModelSerializer):
    slot = serializers.StringRelatedField()
    worn_traits = serializers.StringRelatedField(many=True)

    class Meta:
        model = WornItems
        fields = ['id', 'name', 'description', 'price', 'weight', 'level', 'activate', 'effect', 'currency', 'slot',
                  'worn_traits']
