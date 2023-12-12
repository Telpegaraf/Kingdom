from django.db import models
from apps.god.models import God, Domains


class MoralIntentions(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ClassCharacter(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Race(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CharacterNPC(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='character_race')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    alias = models.CharField(max_length=100, null=True, blank=True)
    class_character = models.ForeignKey(ClassCharacter, related_name='character_class', on_delete=models.CASCADE)
    god = models.ForeignKey(God, related_name='character_god', on_delete=models.CASCADE)
    intentions = models.ManyToManyField(MoralIntentions, related_name='character_intentions')
    domain = models.ForeignKey(Domains, related_name='character_domain', on_delete=models.CASCADE, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    level = models.IntegerField(default=0)
    description = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        name = self.first_name

        if self.last_name:
            name += f" {self.last_name}"
        if self.alias:
            name += f" {self.alias}"

        return name


class Ruler(models.Model):
    character = models.ForeignKey(CharacterNPC, related_name='character', on_delete=models.CASCADE)
    title = models.ForeignKey(Title, related_name='title', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} {self.character}"


class Character(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='player_race')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    alias = models.CharField(max_length=200, null=True, blank=True)
    class_player = models.ForeignKey(ClassCharacter, related_name='player_class', on_delete=models.CASCADE)
    god = models.ForeignKey(God, related_name='player_god', on_delete=models.CASCADE)
    intentions = models.ManyToManyField(MoralIntentions, related_name='player_intentions')
    domain = models.ForeignKey(Domains, related_name='player_domain', on_delete=models.CASCADE, null=True, blank=True)
    age = models.IntegerField()
    level = models.IntegerField(default=1)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.class_player} {self.first_name} {self.last_name} {self.level} уровня"
