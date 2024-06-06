from django.contrib import admin
from apps.character import models


admin.site.register(models.Title, admin.ModelAdmin)


@admin.register(models.CharacterNPC)
class CharacterNpcAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ('__str__', 'class_character', 'level', 'race', 'id')
    search_fields = ('first_name',)


admin.site.register(models.Ruler, admin.ModelAdmin)


@admin.register(models.Character)
class CharacterAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ('__str__', 'class_player', 'level', 'race', 'id')
    search_fields = ('first_name',)


class BaseCharacterAdmin(admin.ModelAdmin):
    ordering = ('character',)
    list_display = ('character_name', 'character_level', 'character_class', 'character_id')
    list_select_related = ('character',)

    @admin.display(description='Character Name', ordering='character__first_name')
    def character_name(self, obj):
        return obj.character.__str__()

    @admin.display(description='Character ID')
    def character_id(self, obj):
        return obj.character.id

    @admin.display(description='Character Level', ordering='character__level')
    def character_level(self, obj):
        return obj.character.level

    @admin.display(description='Character Class', ordering='character__class_player')
    def character_class(self, obj):
        return obj.character.class_player


@admin.register(models.CharacterStats)
class CharacterStatsAdmin(BaseCharacterAdmin):
    pass


@admin.register(models.CharacterPoints)
class CharacterPointsAdmin(BaseCharacterAdmin):
    pass


@admin.register(models.SecondaryStats)
class CharacterSecondaryStatsAdmin(BaseCharacterAdmin):
    pass


@admin.register(models.CharacterFeatList)
class CharacterFeatListAdmin(BaseCharacterAdmin):
    pass


@admin.register(models.CharacterSkillList)
class CharacterSkillListAdmin(BaseCharacterAdmin):
    pass


@admin.register(models.CharacterSkillMastery)
class CharacterSkillMasteryAdmin(admin.ModelAdmin):
    ordering = ('skill_list', 'skill')
    search_fields = ('skill__name',)
    list_display = ('character', 'skill', 'mastery_level', 'character_id')
    list_select_related = ('skill_list__character', 'skill')

    @admin.display(description='Character Name', ordering='skill_list__character__first_name')
    def character(self, obj):
        return obj.skill_list.character.__str__()

    @admin.display()
    def character_id(self, obj):
        return obj.skill_list.character.id


@admin.register(models.WeaponList)
class WeaponListAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CharacterWeaponMastery)
class CharacterWeaponMasteryAdmin(admin.ModelAdmin):
    ordering = ('weapon_list', 'weapon')
    search_fields = ('weapon__name',)
    list_display = ('character', 'weapon', 'mastery_level', 'character_id')
    list_select_related = ('weapon_list__character', 'weapon')

    @admin.display(description='Character Name', ordering='weapon_list__character__first_name')
    def character(self, obj):
        return obj.weapon_list.character.__str__()

    @admin.display()
    def character_id(self, obj):
        return obj.weapon_list.character.id


@admin.register(models.SpellList)
class SpellListAdmin(BaseCharacterAdmin):
    pass


@admin.register(models.CharacterBag)
class CharacterBagAdmin(BaseCharacterAdmin):
    pass


@admin.register(models.CharacterCurrency)
class CharacterCurrencyAdmin(admin.ModelAdmin):
    ordering = ('bag',)
    list_display = ('character_bag', 'currency', 'quantity', 'character_id')
    list_select_related = ('bag__character', 'currency')

    @admin.display(description="Character Bag", ordering='bag__character__first_name')
    def character_bag(self, obj):
        return obj.bag.character.__str__()

    @admin.display(description="Character ID")
    def character_id(self, obj):
        return obj.bag.character.id


@admin.register(models.InventoryItems)
class InventoryItemsAdmin(admin.ModelAdmin):
    ordering = ('bag',)
    list_display = ('character_bag', 'item', 'quantity', 'character_id')
    list_select_related = ('bag__character', 'item')

    @admin.display(description="Character Bag", ordering='bag__character__first_name')
    def character_bag(self, obj):
        return obj.bag.character.__str__()

    @admin.display(description="Character ID")
    def character_id(self, obj):
        return obj.bag.character.id


@admin.register(models.EquippedItems)
class EquippedItemsAdmin(admin.ModelAdmin):
    ordering = ('bag',)
    list_display = ('character_bag', 'character_id')
    list_select_related = ('bag__character',)

    @admin.display(description="Character Bag", ordering='bag__character__first_name')
    def character_bag(self, obj):
        return obj.bag.character.__str__()

    @admin.display(description="Character ID")
    def character_id(self, obj):
        return obj.bag.character.id


@admin.register(models.DefenceAndVulnerabilityDamage)
class DefenceAndVulnerabilityDamageAdmin(BaseCharacterAdmin):
    pass
