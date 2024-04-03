from django.db import models
from apps.general.models import Skills


class SpellTradition(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class SpellSchool(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class SpellTrait(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class SpellComponent(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class SpellCast(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Spell(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    level = models.PositiveSmallIntegerField(default=0)
    school = models.ForeignKey(SpellSchool, on_delete=models.CASCADE, related_name='spell_school')
    tradition = models.ManyToManyField(SpellTradition, related_name='spell_tradition')
    trait = models.ManyToManyField(SpellTrait, related_name='spell_trait', blank=True)
    component = models.ManyToManyField(SpellComponent, related_name='spell_component', blank=True)
    cast = models.ForeignKey(SpellCast, on_delete=models.CASCADE, related_name='spell_cast')
    spell_range = models.PositiveSmallIntegerField(default=0)
    duration = models.CharField(max_length=200, null=True, blank=True)
    sustain = models.BooleanField(default=False)
    ritual = models.BooleanField(default=False)
    secondary_casters = models.CharField(max_length=200, null=True, blank=True)
    cost = models.CharField(max_length=200)
    primary_check = models.ManyToManyField(Skills, blank=True, related_name='spell_primary_check')
    secondary_check = models.ManyToManyField(Skills, blank=True, related_name='spell_secondary_check')
    target = models.CharField(max_length=200, null=True, blank=True)
    source = models.CharField(max_length=200, null=True, blank=True, verbose_name="Official Book")

    def __str__(self):
        return self.name
