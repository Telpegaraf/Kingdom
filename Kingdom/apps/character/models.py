from django.db import models
from apps.god.models import God, Domains
from apps.equipment.models import Equipment


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


class CharacterStats(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='character_stats')
    strength = models.IntegerField(default=10)
    dexterity = models.IntegerField(default=10)
    constitution = models.IntegerField(default=10)
    intelligence = models.IntegerField(default=10)
    wisdom = models.IntegerField(default=10)
    charisma = models.IntegerField(default=10)
    max_speed = models.IntegerField(default=30)
    speed = models.IntegerField(default=30)
    armor_class = models.IntegerField(default=10)
    attack_class = models.IntegerField(default=0)
    damage_bonus = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.character}'s Stats"


class CharacterBag(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='character_bag')
    max_capacity = models.IntegerField(default=0)
    capacity = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.character}'s Bag"


class InventoryItems(models.Model):
    inventory = models.ForeignKey(CharacterBag, on_delete=models.CASCADE, related_name='inventory')
    is_equip = models.BooleanField(default=False)
    item = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='item')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.item}({self.quantity})"
