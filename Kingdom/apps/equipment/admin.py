from django.contrib import admin
from apps.equipment.models import Equipment, ArmorType


admin.site.register(ArmorType)
admin.site.register(Equipment)
