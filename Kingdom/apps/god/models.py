from django.db import models


class Domains(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class God(models.Model):
    name = models.CharField(max_length=50, unique=True)
    alias = models.CharField(max_length=100)
    edict = models.CharField(max_length=250)
    anathema = models.CharField(max_length=250)
    areas_of_interest = models.CharField(max_length=100)
    temples = models.CharField(max_length=100)
    worship = models.CharField(max_length=100)
    sacred_animal = models.CharField(max_length=100)
    sacred_color = models.CharField(max_length=100)
    domain = models.ManyToManyField(Domains, related_name='domain')
    chosen_weapon = models.CharField(max_length=100)
    taro = models.CharField(max_length=100)
    alignment = models.CharField(max_length=100, default="Unknown")

    def __str__(self):
        return f"{self.name}, {self.alias}"
