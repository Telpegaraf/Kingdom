from django.contrib import admin
from apps.character.models import MoralIntentions, ClassCharacter, Ruler, CharacterNPC, Title, Race

model_list = [MoralIntentions, ClassCharacter, CharacterNPC, Ruler, Title, Race]

for model in model_list:
    admin.site.register(model, admin.ModelAdmin)
