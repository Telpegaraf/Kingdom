from django.db import models
from apps.city.apps import Ruler
from apps.city.apps import God


class Government(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Kingdom(models.Model):
    name = models.CharField(max_length=100)
    form_of_government = models.ForeignKey(Government, related_name='government', on_delete=models.CASCADE)
    ruler = models.ForeignKey(Ruler, related_name='kingdom_ruler', on_delete=models.CASCADE)
    population = models.IntegerField()

    def __str__(self):
        return f"{self.form_of_government} {self.name}"


class Region(models.Model):
    name = models.CharField(max_length=100)
    kingdom = models.ForeignKey(Kingdom, related_name='region', on_delete=models.CASCADE)
    form_of_government = models.ForeignKey(Government, related_name='region_government', on_delete=models.CASCADE)
    ruler = models.ForeignKey(Ruler, related_name='region_ruler', on_delete=models.CASCADE)
    population = models.IntegerField()

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, related_name='city', on_delete=models.CASCADE)
    form_of_government = models.ForeignKey(Government, related_name='city_government', on_delete=models.CASCADE)
    ruler = models.ForeignKey(Ruler, related_name='city_ruler', on_delete=models.CASCADE)
    population = models.IntegerField()
    temples = models.ManyToManyField(God, related_name='city_temples')
    blazon = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
