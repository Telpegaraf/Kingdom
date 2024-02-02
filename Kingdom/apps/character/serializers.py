import math

from rest_framework import serializers
from apps.equipment.models import Item, Weapon, PlateArmor, WornItems
from apps.character.models import Character, CharacterStats, CharacterBag, InventoryItems, SecondaryStats,\
    CharacterSkillList, DefenceAndVulnerabilityDamage, EquippedItems, CharacterFeatList, CharacterSkillMastery,\
    SpellList
from apps.player_class.serializers import FeatsSerializer


class InventoryItemSerializer(serializers.ModelSerializer):
    item = serializers.StringRelatedField()
    weight = serializers.SerializerMethodField()
    price = serializers.IntegerField(source='item.price', read_only=True)

    class Meta:
        model = InventoryItems
        fields = ['item', 'quantity', 'weight', 'price']

    def get_weight(self, obj):
        return obj.item.weight * obj.quantity


class EquippeditemSerializer(serializers.Serializer):
    plate_armor = serializers.StringRelatedField()
    first_weapon = serializers.StringRelatedField()
    second_weapon = serializers.StringRelatedField()
    worn_items = serializers.StringRelatedField(many=True)

    class Meta:
        model = EquippedItems
        fields = ['plate_armor', 'first_weapon', 'second_weapon', 'worn_items']


class CharacterBagSerializer(serializers.ModelSerializer):
    inventory = InventoryItemSerializer(read_only=True, many=True)
    equipped_items = EquippeditemSerializer(read_only=True, many=True)

    class Meta:
        model = CharacterBag
        fields = ['max_capacity', 'capacity', 'inventory', 'equipped_items']


class CharacterStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterStats
        fields = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma',
                  'max_speed', 'speed', 'perception_mastery', 'unarmed_mastery', 'light_armor_mastery',
                  'medium_armor_mastery', 'heavy_armor_mastery', 'fortitude_mastery',
                  'reflex_mastery', 'will_mastery',]


class SecondaryStatsSerializer(serializers.ModelSerializer):
    armor_class = serializers.SerializerMethodField()

    class Meta:
        model = SecondaryStats
        fields = ['armor_class', 'attack_class', 'damage_bonus', 'max_health', 'health', 'initiative',
                  'fortitude_saving', 'reflex_saving', 'will_saving']


class CharacterOverallSerializer(serializers.ModelSerializer):
    class_player = serializers.StringRelatedField()

    class Meta:
        model = Character
        fields = ['id', 'first_name', 'last_name', 'alias', 'class_player', 'level']


class CharacterSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterSkillList
        fields = ['skill']


class CharacterSkillMasterySerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterSkillMastery
        fields = ['mastery_level']


class CharacterFeatsSerializer(serializers.ModelSerializer):
    feat_class = FeatsSerializer(many=True)

    class Meta:
        model = CharacterFeatList
        fields = ['id', 'feat_class']


class SetFeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterFeatList
        fields = ['feat_class']

    def validate(self, data):
        print(self.context)
        player_class = self.context.get('class_player')
        player_level = self.context.get('class_level')
        feat_list = data.get('feat_class')
        print(data)
        for feat in feat_list:
            if feat.class_character is not None and feat.class_character != player_class:
                raise serializers.ValidationError(f"Wrong class, {feat} only for {feat.class_character}")
            if feat.level is not None and feat.level > player_level:
                raise serializers.ValidationError(f"Wrong level, {feat} need {feat.level} level")
            print(feat.class_character)
            print(feat.level)

        return data


class SetSpellSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellList
        fields = ['spell']


class DefenceAndVulnerabilitySerializer(serializers.ModelSerializer):
    immunity = serializers.StringRelatedField(read_only=True, many=True)
    resistance = serializers.StringRelatedField(read_only=True, many=True)
    weakness = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = DefenceAndVulnerabilityDamage
        fields = ['immunity', 'resistance', 'weakness']


class CharacterDetailSerializer(serializers.ModelSerializer):
    class_player = serializers.StringRelatedField()
    god = serializers.StringRelatedField()
    race = serializers.StringRelatedField()
    intentions = serializers.StringRelatedField(read_only=True, many=True)
    stats = CharacterStatsSerializer(
        read_only=True,
        many=True,
        source='character_stats'
    )
    secondary_stats = SecondaryStatsSerializer(
        read_only=True,
        many=True,
    )
    bag = CharacterBagSerializer(
        read_only=True,
        many=True,
        source='character_bag'
    )
    skill_list = CharacterSkillSerializer(
        read_only=True,
        many=True,
    )

    defence_and_vulnerability = DefenceAndVulnerabilitySerializer(
        read_only=True,
    )
    feat_list = CharacterFeatsSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        model = Character
        fields = ['race', 'first_name', 'last_name', 'alias', 'class_player', 'god', 'intentions', 'domain',
                  'age', 'level', 'description', 'stats', 'secondary_stats', 'skill_list', 'bag',
                  'defence_and_vulnerability', 'feat_list']


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['race', 'first_name', 'last_name', 'alias', 'class_player', 'god', 'intentions', 'domain',
                  'age', 'size', 'description',]


class CharacterStatsDisplay(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['stat_count', 'class_feat_count', 'general_feat_count', 'background_feat_count', 'skill_count']


class SetStatsDisplaySerializer(serializers.ModelSerializer):
    character_stats = CharacterStatsDisplay(read_only=True)

    class Meta:
        model = CharacterStats
        fields = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma', 'character_stats']


class SetStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterStats
        fields = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']

    def validate(self, data):
        character = self.instance
        if character.character.level == 1 and not all(value <= 18 for value in data.values()):
            raise serializers.ValidationError("All stats must be 18 or lower at level 1.")

        return data


class SetSpeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterStats
        fields = ['max_speed', 'speed']

    def validate(self, data):
        if data['speed'] > data['max_speed']:
            raise serializers.ValidationError("The speed should not exceed the maximum")

        return data


class SetMasterySerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterStats
        fields = ['perception_mastery', 'unarmed_mastery', 'light_armor_mastery', 'medium_armor_mastery',
                  'heavy_armor_mastery', 'fortitude_mastery', 'reflex_mastery', 'will_mastery']


class AddItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)
    inventory_id = serializers.IntegerField()

    def validate(self, data):
        item_id = data.get('item_id')
        inventory_id = data.get('inventory_id')

        try:
            Item.objects.get(pk=item_id)
            CharacterBag.objects.get(pk=inventory_id)
        except Item.DoesNotExist:
            raise serializers.ValidationError("Item with specified ID does not exist.")
        except InventoryItems.DoesNotExist:
            raise serializers.ValidationError("Inventory with specified ID does not exist.")

        return data

    def save(self):
        item_id = self.validated_data['item_id']
        quantity = self.validated_data.get('quantity', 1)
        inventory_id = self.validated_data['inventory_id']

        inventory = CharacterBag.objects.get(pk=inventory_id)
        item = Item.objects.get(pk=item_id)
        inventory_item, created = InventoryItems.objects.get_or_create(inventory=inventory, item=item)

        if not created:
            inventory_item.quantity += quantity
            inventory_item.save()

        return inventory_item


class EquipItemSerializer(serializers.Serializer):
    equipped_items = serializers.IntegerField()
    item_id = serializers.IntegerField()

    def validate(self, data):
        item_id = data.get('item_id')
        equipped_items = data.get('equipped_items')
        type_item = None

        try:
            item = Weapon.objects.get(item_ptr_id=item_id)
            if item.two_hands:
                type_item = '2h_weapon'
            else:
                type_item = '1h_weapon'
        except Weapon.DoesNotExist:
            pass

        try:
            item = PlateArmor.objects.get(item_ptr_id=item_id)
            type_item = 'plate_armor'
        except PlateArmor.DoesNotExist:
            pass

        try:
            item = WornItems.objects.get(item_ptr_id=item_id)
            type_item = 'worn_item'
        except WornItems.DoesNotExist:
            pass

        try:
            bag = CharacterBag.objects.get(pk=equipped_items)
        except EquippedItems.DoesNotExist:
            raise serializers.ValidationError("Inventory with specified ID does not exist.")

        if type_item is None:
            raise serializers.ValidationError(
                "Item with specified ID does not exist or is not one of the supported types.")

        data['type_item'] = type_item

        return data

    def save(self):
        item_id = self.validated_data['item_id']
        equipped_items_id = self.validated_data['equipped_items']
        type_item = self.validated_data['type_item']
        equipped_items, created = EquippedItems.objects.get_or_create(equipped_items_id=equipped_items_id)
        try:
            item = InventoryItems.objects.get(item_id=item_id)
        except:
            raise serializers.ValidationError("Item does not exist in Inventory")
        if type_item == 'plate_armor':
            equipped_items.plate_armor = item
        elif type_item == '2h_weapon':
            equipped_items.second_weapon = None
            equipped_items.first_weapon = item
        elif type_item == '1h_weapon':
            if equipped_items.first_weapon is not None and equipped_items.first_weapon.two_hands:
                equipped_items.first_weapon = item
            elif equipped_items.first_weapon is not None:
                equipped_items.second_weapon = item
        elif type_item == 'worn_item':
            equipped_items.worn_items.add(item)

        equipped_items.save()

        return equipped_items


class LevelUpSerializer(serializers.ModelSerializer):
    old_level = serializers.SerializerMethodField()
    max_health = serializers.IntegerField(source='secondary_stats.max_health')
    health_by_level = serializers.IntegerField(source='class_player.health_by_level')
    constitution_mod = serializers.SerializerMethodField()

    class Meta:
        model = Character
        fields = ['id', 'old_level', 'level', 'max_health', 'health_by_level', 'constitution_mod']

    def get_constitution_mod(self, obj):
        return math.floor((obj.character_stats.constitution)/2-5)

    def get_old_level(self, obj):
        return obj.level

    def validate(self, data):
        new_level = data['level']
        if new_level is None or new_level > 20:
            return serializers.ValidationError("Invalid level value")

        return data

    def save(self, **kwargs):
        character_id = self.data.get('id')
        old_level = self.data.get('old_level')
        constitution_mod = self.data.get('constitution_mod')
        health_by_level = self.data.get('health_by_level')
        level = self.validated_data.get('level')
        level_difference = level - old_level
        health_add = level_difference * (constitution_mod+health_by_level)
        character = Character.objects.select_related('secondary_stats').get(id=character_id)
        character.level = level
        character.secondary_stats.max_health += health_add
        character.secondary_stats.health += health_add
        character.save()
        character.secondary_stats.save()

