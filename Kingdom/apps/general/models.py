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


class MoralIntentions(models.Model):
    name = models.CharField(max_length=400, unique=True)

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
