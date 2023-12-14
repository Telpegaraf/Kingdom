from django.db import models
from apps.god.models import God, Domains
from apps.equipment.models import Equipment
from apps.mastery.models import MasteryLevels


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


class Feats(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    level = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.name


class Skills(models.Model):
    name = models.CharField(max_length=100)

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
    level = models.PositiveSmallIntegerField(default=0)
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
    level = models.PositiveSmallIntegerField(default=1)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.class_player} {self.first_name} {self.last_name} {self.level} уровня"


class CharacterStats(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='character_stats')
    strength = models.PositiveSmallIntegerField(default=10)
    dexterity = models.PositiveSmallIntegerField(default=10)
    constitution = models.PositiveSmallIntegerField(default=10)
    intelligence = models.PositiveSmallIntegerField(default=10)
    wisdom = models.PositiveSmallIntegerField(default=10)
    charisma = models.PositiveSmallIntegerField(default=10)
    max_speed = models.PositiveSmallIntegerField(default=30)
    speed = models.PositiveSmallIntegerField(default=30)

    def __str__(self):
        return f"{self.character}'s Stats"


class SecondaryStats(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='secondary_stats')
    armor_class = models.SmallIntegerField(default=10)
    un_armor_mastery = models.CharField(
        max_length=10,
        choices=MasteryLevels.choices,
        default=MasteryLevels.ABSENT,
    )
    light_armor_mastery = models.CharField(
        max_length=10,
        choices=MasteryLevels.choices,
        default=MasteryLevels.ABSENT,
    )
    medium_armor_mastery = models.CharField(
        max_length=10,
        choices=MasteryLevels.choices,
        default=MasteryLevels.ABSENT,
    )
    heavy_armor_mastery = models.CharField(
        max_length=10,
        choices=MasteryLevels.choices,
        default=MasteryLevels.ABSENT,
    )
    attack_class = models.SmallIntegerField(default=0)
    damage_bonus = models.SmallIntegerField(default=0)
    max_health = models.IntegerField(default=1)
    health = models.IntegerField(default=0)
    initiative = models.SmallIntegerField(default=0)
    fortitude_saving = models.SmallIntegerField(default=0)
    fortitude_mastery = models.CharField(
        max_length=10,
        choices=MasteryLevels.choices,
        default=MasteryLevels.ABSENT,
    )
    reflex_saving = models.SmallIntegerField(default=0)
    reflex_mastery = models.CharField(
        max_length=10,
        choices=MasteryLevels.choices,
        default=MasteryLevels.ABSENT,
    )
    will_saving = models.SmallIntegerField(default=0)
    will_mastery = models.CharField(
        max_length=10,
        choices=MasteryLevels.choices,
        default=MasteryLevels.ABSENT,
    )

    def __str__(self):
        return f"{self.character}'s Secondary Stats"


class CharacterSkillList(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='character_skills')

    def __str__(self):
        return f"{self.character}'s Skill List"


class CharacterSkill(models.Model):
    skill_list = models.ForeignKey(CharacterSkillList, on_delete=models.CASCADE, related_name='skill_list')
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE)
    mastery_level = models.CharField(
        max_length=10,
        choices=MasteryLevels.choices,
        default=MasteryLevels.ABSENT,
    )

    class Meta:
        unique_together = ['skill_list', 'skill', 'mastery_level']

    def __str__(self):
        return f"{self.skill_list.character} - {self.skill} - {self.mastery_level}"


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
