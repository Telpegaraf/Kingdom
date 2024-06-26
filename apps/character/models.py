from django.db import models
from django.core.exceptions import ValidationError

from apps.god.models import God, Domains
from apps.general.models import MasteryLevels, DamageType, Skills, Race, WeaponMastery
from apps.equipment.models import Item, Currency
from apps.player_class.models import ClassCharacter, Feat
from apps.spell.models import Spell
from apps.user.models import CustomUser


class Title(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CharacterNPC(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='character_race')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    alias = models.CharField(max_length=100, null=True, blank=True)
    class_character = models.ForeignKey(ClassCharacter, related_name='character_class', on_delete=models.CASCADE)
    god = models.ForeignKey(God, related_name='character_god', on_delete=models.CASCADE)
    domain = models.ForeignKey(Domains, related_name='character_domain', on_delete=models.CASCADE, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    level = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(max_length=1000, null=True, blank=True)

    class Meta:
        unique_together = ['first_name', 'last_name']

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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='character')
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='player_race')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    alias = models.CharField(max_length=200, null=True, blank=True)
    class_player = models.ForeignKey(ClassCharacter, related_name='player_class', on_delete=models.CASCADE)
    god = models.ForeignKey(God, related_name='player_god', on_delete=models.CASCADE)
    domain = models.ForeignKey(Domains, related_name='player_domain', on_delete=models.CASCADE, null=True, blank=True)
    age = models.IntegerField()
    size = models.PositiveSmallIntegerField(null=True, blank=True)
    level = models.PositiveSmallIntegerField(default=1)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.class_player} {self.first_name} {self.last_name}"


class CharacterStats(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='character_stats')
    strength = models.PositiveSmallIntegerField(default=10)
    dexterity = models.PositiveSmallIntegerField(default=10)
    constitution = models.PositiveSmallIntegerField(default=10)
    intelligence = models.PositiveSmallIntegerField(default=10)
    wisdom = models.PositiveSmallIntegerField(default=10)
    charisma = models.PositiveSmallIntegerField(default=10)
    max_speed = models.PositiveSmallIntegerField(default=30)
    speed = models.PositiveSmallIntegerField(default=30)
    perception_mastery = models.CharField(
        max_length=10,
        choices=MasteryLevels.choices,
        default=MasteryLevels.ABSENT
    )
    unarmed_mastery = models.CharField(
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
    fortitude_mastery = models.CharField(
        max_length=10,
        choices=MasteryLevels.choices,
        default=MasteryLevels.ABSENT,
    )
    reflex_mastery = models.CharField(
        max_length=10,
        choices=MasteryLevels.choices,
        default=MasteryLevels.ABSENT,
    )
    will_mastery = models.CharField(
        max_length=10,
        choices=MasteryLevels.choices,
        default=MasteryLevels.ABSENT,
    )

    def __str__(self):
        return f"{self.character}'s Stats"


class CharacterPoints(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='character_stat_points')
    strength = models.PositiveSmallIntegerField(default=0)
    dexterity = models.PositiveSmallIntegerField(default=0)
    constitution = models.PositiveSmallIntegerField(default=0)
    intelligence = models.PositiveSmallIntegerField(default=0)
    wisdom = models.PositiveSmallIntegerField(default=0)
    charisma = models.PositiveSmallIntegerField(default=0)
    free = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.character}'s Stat Points"


class SecondaryStats(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='secondary_stats')
    perception = models.SmallIntegerField(default=0)
    armor_class = models.SmallIntegerField(default=10)
    attack_class = models.SmallIntegerField(default=0)
    damage_bonus = models.SmallIntegerField(default=0)
    max_health = models.IntegerField(default=1)
    health = models.IntegerField(default=0)
    initiative = models.SmallIntegerField(default=0)
    fortitude_saving = models.SmallIntegerField(default=0)
    reflex_saving = models.SmallIntegerField(default=0)
    will_saving = models.SmallIntegerField(default=0)

    def __str__(self):
        return f"{self.character}'s Secondary Stats"


class CharacterFeatList(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='feat_list')
    feat_class = models.ManyToManyField(Feat, related_name='character_feat', blank=True)

    def __str__(self):
        return f"{self.character}'s Feats"


class CharacterSkillList(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='skill_list')
    skill = models.ManyToManyField(Skills, blank=True, related_name='character_skill_list')

    def __str__(self):
        return f"{self.character}'s Skill List'"


class CharacterSkillMastery(models.Model):
    skill_list = models.ForeignKey(CharacterSkillList, on_delete=models.CASCADE, related_name='character_skill')
    skill = models.ForeignKey(
        Skills,
        on_delete=models.CASCADE,
        related_name='character_skill_mastery',
    )
    mastery_level = models.CharField(
        max_length=10,
        choices=MasteryLevels.choices,
        default=MasteryLevels.ABSENT,
    )

    class Meta:
        unique_together = ['skill_list', 'skill']

    def __str__(self):
        return f"{self.skill_list.character} - {self.skill} - {self.mastery_level}"


class WeaponList(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='weapon_list')
    weapon = models.ManyToManyField(WeaponMastery, blank=True, related_name='character_weapon_list')

    def __str__(self):
        return f"{self.character}'s Weapon Mastery List"


class CharacterWeaponMastery(models.Model):
    weapon_list = models.ForeignKey(WeaponList, on_delete=models.CASCADE, related_name='character_weapon')
    weapon = models.ForeignKey(
        WeaponMastery,
        on_delete=models.CASCADE,
        related_name='character_weapon_mastery',
    )
    mastery_level = models.CharField(
        max_length=10,
        choices=MasteryLevels.choices,
        default=MasteryLevels.ABSENT
    )

    class Meta:
        unique_together = ['weapon_list', 'weapon']

    def __str__(self):
        return f"{self.weapon_list.character} - {self.weapon} - {self.mastery_level}"


class SpellList(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='character_spell_list')
    spell = models.ManyToManyField(Spell, blank=True, related_name='character_spell')

    def __str__(self):
        return f"{self.character}'s Spell List"


class CharacterBag(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='character_bag')
    max_capacity = models.IntegerField(default=0)
    capacity = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.character}'s Bag"


class CharacterCurrency(models.Model):
    bag = models.ForeignKey(CharacterBag, on_delete=models.CASCADE, related_name='character_currency')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='currency')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.bag}'s currency"


class InventoryItems(models.Model):
    bag = models.ForeignKey(CharacterBag, on_delete=models.CASCADE, related_name='inventory')
    quantity = models.PositiveIntegerField(default=1)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item')

    def __str__(self):
        return f"{self.bag} - {self.item}({self.quantity})"


class EquippedItems(models.Model):
    bag = models.OneToOneField(CharacterBag, on_delete=models.CASCADE, related_name='equipped_items')
    plate_armor = models.ForeignKey(
        InventoryItems,
        on_delete=models.CASCADE,
        related_name='plate_armor',
        null=True,
        blank=True,
    )
    first_weapon = models.ForeignKey(
        InventoryItems,
        on_delete=models.CASCADE,
        related_name='first_weapon',
        null=True,
        blank=True,
    )
    second_weapon = models.ForeignKey(
        InventoryItems,
        on_delete=models.CASCADE,
        related_name='second_weapon',
        null=True,
        blank=True,
    )
    worn_items = models.ManyToManyField(
        InventoryItems,
        related_name='worn_items',
        blank=True,
    )

    def __str__(self):
        return f"{self.bag}'s equipped items"


class DefenceAndVulnerabilityDamage(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='defence_and_vulnerability')
    immunity = models.ManyToManyField(DamageType, related_name='immunity', blank=True)
    resistance = models.ManyToManyField(DamageType, related_name='resistance', blank=True)
    weakness = models.ManyToManyField(DamageType, related_name='weakness', blank=True)

    def __str__(self):
        return f"{self.character}'s defences and vulnerabilities"
