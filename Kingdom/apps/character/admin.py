from django.contrib import admin
from apps.character.models import MoralIntentions, ClassCharacter, Ruler

model_list = [MoralIntentions, ClassCharacter, Ruler]

for model in model_list:
    admin.site.register(model, admin.ModelAdmin)
