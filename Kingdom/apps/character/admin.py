from django.contrib import admin
from apps.character.models import Ruler, CharacterNPC, Title, Character,\
    CharacterBag, InventoryItems, CharacterStats, SecondaryStats, CharacterSkillList,\
    DefenceAndVulnerabilityDamage, EquippedItems, CharacterFeatList


class InventoryItemsAdmin(admin.ModelAdmin):
    ordering = ['inventory']


class EquippedItemsAdmin(admin.ModelAdmin):
    ordering = ('equipped_items', 'plate_armor', 'first_weapon', 'second_weapon', 'worn_items')


model_list = [CharacterNPC, Ruler, Title,
              Character, CharacterBag, CharacterStats, SecondaryStats,
              CharacterSkillList, DefenceAndVulnerabilityDamage, CharacterFeatList]

admin.site.register(InventoryItems, InventoryItemsAdmin)
admin.site.register(EquippedItems, EquippedItemsAdmin)

for model in model_list:
    admin.site.register(model, admin.ModelAdmin)
