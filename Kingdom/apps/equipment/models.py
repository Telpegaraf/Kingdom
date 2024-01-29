from django.db import models
from apps.general.models import ArmorCategory, DamageType


class GoldAndCurrency(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.PositiveSmallIntegerField()
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=500)
    currency = models.ForeignKey(GoldAndCurrency, on_delete=models.SET_NULL, related_name='armor_currency', null=True)
    price = models.PositiveSmallIntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.01)

    def __str__(self):
        return self.name


class ArmorTrait(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class ArmorGroup(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    hardness = models.PositiveSmallIntegerField(default=1)
    health = models.PositiveSmallIntegerField()
    broken_threshold = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class ArmorSpecialization(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class PlateArmor(Item):
    category = models.CharField(
        max_length=100,
        choices=ArmorCategory.choices
    )
    ac_bonus = models.PositiveSmallIntegerField(default=0)
    dexterity_modifier_cap = models.PositiveSmallIntegerField(null=True, blank=True)
    check_penalty = models.BooleanField(default=False)
    speed_penalty = models.BooleanField(default=False)
    strength = models.PositiveSmallIntegerField(null=True, blank=True)
    group = models.ForeignKey(ArmorGroup, on_delete=models.CASCADE, related_name='armor_group')
    armor_traits = models.ManyToManyField(ArmorTrait, related_name='traits', blank=True)
    armor_specialization = models.ManyToManyField(ArmorSpecialization, related_name='specialization', blank=True)
    level = models.PositiveSmallIntegerField(default=1)


class WeaponTrait(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class WeaponGroup(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class WeaponSpecialization(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Weapon(Item):
    dice = models.PositiveSmallIntegerField(default=4)
    dice_count = models.PositiveSmallIntegerField(default=1)
    bonus_damage = models.PositiveSmallIntegerField(null=True, blank=True)
    type_damage = models.ForeignKey(DamageType, on_delete=models.CASCADE, related_name='first_type_damage_weapon')
    second_dice = models.PositiveSmallIntegerField(null=True, blank=True)
    second_dice_count = models.PositiveSmallIntegerField(null=True, blank=True)
    second_bonus_damage = models.PositiveSmallIntegerField(null=True, blank=True)
    second_type_damage = models.ForeignKey(DamageType, on_delete=models.CASCADE,
                                           related_name='second_type_damage_weapon', null=True, blank=True)
    range = models.PositiveSmallIntegerField(null=True, blank=True)
    reload = models.PositiveSmallIntegerField(null=True, blank=True)
    two_hands = models.BooleanField(default=True)
    weapon_traits = models.ManyToManyField(WeaponTrait, related_name='weapon_traits', blank=True)
    level = models.PositiveSmallIntegerField(default=1)


class TypeWornItems(models.Model):
    slot = models.CharField(max_length=100, unique=True)
    limit = models.BooleanField(default=True)

    def __str__(self):
        return self.slot


class WornTrait(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class WornItems(Item):
    slot = models.ForeignKey(TypeWornItems, on_delete=models.CASCADE, related_name='slot_item')
    level = models.PositiveSmallIntegerField(default=1)
    worn_traits = models.ManyToManyField(WornTrait, related_name='worn_traits', blank=True)
    activate = models.TextField(max_length=500, null=True, blank=True)
    effect = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.slot})"


class CommonItems(Item):
    pass
