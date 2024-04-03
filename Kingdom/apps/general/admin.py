from django.contrib import admin
from apps.general.models import Race, MoralIntentions, DamageType, Skills, FeatTrait, Prerequisite, Action, Trigger,\
    WeaponMastery

model_list = [Race, MoralIntentions, DamageType, Skills, FeatTrait, Prerequisite, Action, Trigger, WeaponMastery]

for model in model_list:
    admin.site.register(model, admin.ModelAdmin)
