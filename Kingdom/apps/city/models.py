from django.db import models
from apps.character.models import Ruler
from apps.god.models import God


class Government(models.Model):
    name = models.CharField(max_length=100)


class Kingdom(models.Model):
    name = models.CharField(max_length=100)
    form_of_government = models.ForeignKey(Government, related_name='government', on_delete=models.CASCADE)
    ruler = models.ForeignKey(Ruler, related_name='kingdom_ruler', on_delete=models.CASCADE)
    population = models.IntegerField()


class Region(models.Model):
    name = models.CharField(max_length=100)
    kingdom = models.ForeignKey(Kingdom, related_name='region', on_delete=models.CASCADE)
    ruler = models.ForeignKey(Ruler, related_name='region_ruler', on_delete=models.CASCADE)
    population = models.IntegerField()


class City(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, related_name='city', on_delete=models.CASCADE)
    ruler = models.ForeignKey(Ruler, related_name='city_ruler', on_delete=models.CASCADE)
    population = models.IntegerField()
    temples = models.ManyToManyField(God, related_name='city_temples')
    blazon = models.ImageField(null=True, blank=True)
