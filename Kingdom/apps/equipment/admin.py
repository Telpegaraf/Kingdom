from django.contrib import admin
from apps.equipment.models import Equipment, ItemType, Trait


admin.site.register(ItemType)
admin.site.register(Equipment)
admin.site.register(Trait)
