from django.db import models
from apps.god.models import God, Domains


class MoralIntentions(models.Model):
    name = models.CharField(max_length=100)


class Title(models.Model):
    name = models.CharField(max_length=100)


class ClassCharacter(models.Model):
    name = models.CharField(max_length=50)


class CharacterNPC(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    alias = models.CharField(max_length=100, null=True, blank=True)
    class_character = models.ForeignKey(ClassCharacter, related_name='character_npc', on_delete=models.CASCADE)
    god = models.ForeignKey(God, related_name='character_god', on_delete=models.CASCADE)
    intentions = models.ManyToManyField(MoralIntentions, related_name='character_intentions')
    domain = models.ForeignKey(Domains, related_name='character_domain', on_delete=models.CASCADE, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    level = models.IntegerField(default=0)


class Ruler(models.Model):
    character = models.ForeignKey(CharacterNPC, related_name='character', on_delete=models.CASCADE)
    title = models.ForeignKey(Title, related_name='title', on_delete=models.CASCADE)
