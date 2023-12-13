from django.contrib import admin
from apps.equipment.models import Equipment, ArmorType, Trait


admin.site.register(ArmorType)
admin.site.register(Equipment)
admin.site.register(Trait)
