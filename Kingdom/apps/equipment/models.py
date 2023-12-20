from django.db import models


class ItemType(models.Model):
    name = models.CharField(max_length=100)
    max_slots = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name


class Trait(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    type_item = models.ForeignKey(ItemType, related_name='armor_type', on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(null=True, blank=True)
    traits = models.ManyToManyField(Trait, related_name='traits', blank=True)
    price = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=1000)
    weight = models.DecimalField(max_digits=7, decimal_places=2, default=0.01)
    armor_class = models.SmallIntegerField(null=True, blank=True)
    attack_bonus = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
