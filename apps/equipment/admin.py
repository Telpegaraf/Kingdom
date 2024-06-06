from django.contrib import admin
from apps.equipment import models


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    ordering = ('name', )


@admin.register(models.ArmorTrait)
class ArmorTraitAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(models.ArmorGroup)
class ArmorGroupAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(models.ArmorSpecialization)
class ArmorSpecializationAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(models.WeaponTrait)
class WeaponTraitAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(models.WeaponGroup)
class WeaponGroupAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(models.WeaponSpecialization)
class WeaponSpecializationAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(models.PlateArmor)
class PlateArmorAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'category', 'ac_bonus')
    search_fields = ('name', 'category')


@admin.register(models.Weapon)
class WeaponAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'damage', 'type_damage', 'second_damage', 'level')
    search_fields = ('name',)

    @admin.display(description="Weapon Damage")
    def damage(self, obj):
        return f"{obj.dice_count}d{obj.dice}+{obj.bonus_damage}"

    @admin.display(description="Bonus Damage", empty_value="None")
    def second_damage(self, obj):
        return f"{obj.second_dice_count}d{obj.second_dice}+{obj.second_bonus_damage} {obj.second_type_damage} damage"


@admin.register(models.TypeWornItems)
class TypeWornItemsAdmin(admin.ModelAdmin):
    list_display = ('slot', 'limit')


@admin.register(models.WornItems)
class WornItemsAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'slot')


@admin.register(models.CommonItems)
class CommonItemsAdmin(admin.ModelAdmin):
    ordering = ('name',)
