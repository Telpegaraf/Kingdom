from django.contrib import admin
from apps.character.apps import Ruler, CharacterNPC, Title, Character,\
    CharacterBag, InventoryItems, CharacterStats, SecondaryStats, CharacterSkillList,\
    DefenceAndVulnerabilityDamage, EquippedItems, CharacterFeatList, CharacterSkillMastery, WeaponList, \
    CharacterWeaponMastery, SpellList, CharacterCurrency


class InventoryItemsAdmin(admin.ModelAdmin):
    ordering = ['bag']


class EquippedItemsAdmin(admin.ModelAdmin):
    ordering = ['bag']


class CharacterSkillMasteryAdmin(admin.ModelAdmin):
    ordering = ['skill_list']


model_list = [CharacterNPC, Ruler, Title,
              Character, CharacterBag, CharacterStats, SecondaryStats,
              CharacterSkillList, DefenceAndVulnerabilityDamage, CharacterFeatList, CharacterWeaponMastery, WeaponList,
              SpellList, CharacterCurrency]

admin.site.register(InventoryItems, InventoryItemsAdmin)
admin.site.register(EquippedItems, EquippedItemsAdmin)
admin.site.register(CharacterSkillMastery, CharacterSkillMasteryAdmin)

for model in model_list:
    admin.site.register(model, admin.ModelAdmin)
