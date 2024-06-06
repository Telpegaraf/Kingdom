from django.db import models


class MasteryLevels(models.TextChoices):
    ABSENT = 'None', 'ABSENT'
    TRAIN = 'Train', 'TRAIN'
    EXPERT = 'Expert', 'EXPERT'
    MASTER = 'Master', 'MASTER'
    LEGEND = 'Legend', 'LEGEND'


class ArmorCategory(models.TextChoices):
    UNARMED = 'None', 'UnARMED'
    LIGHT = 'Light', 'LIGHT'
    MEDIUM = 'Medium', 'MEDIUM'
    HEAVY = 'Heavy', 'HEAVY'


class DamageType(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Skills(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class WeaponMastery(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Race(models.Model):
    name = models.CharField(max_length=200, unique=True)
    health = models.PositiveSmallIntegerField(default=6)
    strength = models.SmallIntegerField(default=0)
    dexterity = models.SmallIntegerField(default=0)
    constitution = models.SmallIntegerField(default=0)
    intelligence = models.SmallIntegerField(default=0)
    wisdom = models.SmallIntegerField(default=0)
    charisma = models.SmallIntegerField(default=0)
    free = models.SmallIntegerField(default=0)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class Action(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Prerequisite(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class FeatTrait(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.name


class Requirements(models.Model):
    name = models.CharField(max_length=600, unique=True)

    def __str__(self):
        return self.name


class Trigger(models.Model):
    name = models.CharField(max_length=600, unique=True)

    def __str__(self):
        return self.name
