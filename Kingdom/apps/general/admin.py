from django.contrib import admin
from apps.general.models import Race, MoralIntentions, DamageType, Skills, FeatTrait, Prerequisite, Action, Trigger

model_list = [Race, MoralIntentions, DamageType, Skills, FeatTrait, Prerequisite, Action, Trigger]

for model in model_list:
    admin.site.register(model, admin.ModelAdmin)
