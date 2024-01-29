from django.contrib import admin
from apps.player_class.models import ClassCharacter, ClassFeat, ClassFeature

model_list = [ClassCharacter, ClassFeat, ClassFeature]

for model in model_list:
    admin.site.register(model, admin.ModelAdmin)
