from django.contrib import admin
from apps.equipment.models import Helmet, PlateArmor, FirstWeapon, SecondWeapon,\
    FirstRing, SecondRing, Amulet, Gloves, FirstBracer, SecondBracer, Boots


models_list = [Helmet, PlateArmor, FirstWeapon, SecondWeapon, FirstRing, SecondRing, Amulet, Gloves, FirstBracer, SecondBracer, Boots]

for model in models_list:
    admin.site.register(model, admin.ModelAdmin)
