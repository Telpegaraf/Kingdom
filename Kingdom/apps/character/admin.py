from django.contrib import admin
from apps.character.models import Ruler, CharacterNPC, Title, Character,\
    CharacterBag, InventoryItems, CharacterStats, SecondaryStats, CharacterSkill,\
    DefenceAndVulnerabilityDamage, EquippedItems, CharacterFeat


model_list = [CharacterNPC, Ruler, Title,
              Character, CharacterBag, InventoryItems, CharacterStats, SecondaryStats,
              CharacterSkill, DefenceAndVulnerabilityDamage, EquippedItems, CharacterFeat]

for model in model_list:
    admin.site.register(model, admin.ModelAdmin)
