from django.contrib import admin
from apps.character.models import MoralIntentions, ClassCharacter, Ruler, CharacterNPC, Title, Race, Character,\
    CharacterBag, InventoryItems, CharacterStats, Skills, Feats, SecondaryStats, CharacterSkill, CharacterSkillList


model_list = [MoralIntentions, ClassCharacter, CharacterNPC, Ruler, Title, Race,
              Character, CharacterBag, InventoryItems, CharacterStats, Skills, Feats, SecondaryStats,
              CharacterSkill, CharacterSkillList]

for model in model_list:
    admin.site.register(model, admin.ModelAdmin)
