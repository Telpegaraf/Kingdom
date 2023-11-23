from django.db import models
from apps.character.models import MoralIntentions


class Domains(models.Model):
    name = models.CharField(max_length=100)


class God(models.Model):
    name = models.CharField(max_length=50)
    edict = models.CharField(max_length=100)
    anathema = models.CharField(max_length=100)
    areas_of_interest = models.CharField(max_length=100)
    temples = models.CharField(max_length=100)
    worship = models.CharField(max_length=100)
    sacred_animal = models.CharField(max_length=100)
    sacred_color = models.CharField(max_length=100)
    domain = models.ForeignKey(Domains, on_delete=models.CASCADE, related_name='domain')
    chosen_weapon = models.CharField(max_length=100)
    moral_intentions = models.ManyToManyField(MoralIntentions, related_name='moral_intentions')
