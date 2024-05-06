from django.contrib import admin
from apps.equipment.apps import Currency, ArmorTrait, ArmorGroup, ArmorSpecialization,\
    PlateArmor, WeaponTrait, WeaponGroup, WeaponSpecialization, Weapon, TypeWornItems, WornItems, CommonItems

models_list = [Currency, ArmorTrait, ArmorGroup, ArmorSpecialization,
               PlateArmor, WeaponTrait, WeaponGroup, WeaponSpecialization, Weapon,
               TypeWornItems, WornItems, CommonItems]

for model in models_list:
    admin.site.register(model, admin.ModelAdmin)
