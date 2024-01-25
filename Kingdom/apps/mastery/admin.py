from django.contrib import admin
from apps.mastery.models import Race, MoralIntentions, DamageType, Skills

model_list = [Race, MoralIntentions, DamageType, Skills]

for model in model_list:
    admin.site.register(model, admin.ModelAdmin)
