from django.contrib import admin
from apps.mastery.models import Race, MoralIntentions, Feats, DamageType, Skills

model_list = [Race, MoralIntentions, Feats, DamageType, Skills]

for model in model_list:
    admin.site.register(model, admin.ModelAdmin)
