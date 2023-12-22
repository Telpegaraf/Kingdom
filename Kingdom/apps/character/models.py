from django.db import models
from apps.god.models import God, Domains
from apps.mastery.models import MasteryLevels, DamageType, MoralIntentions, Skills, Race
from apps.equipment.models import Item, PlateArmor, Weapon, WornItems


class Title(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ClassCharacter(models.Model):
    name = models.CharField(max_length=50)
    health_by_level = models.PositiveSmallIntegerField(default=6)
    perception_mastery = models.CharField(
        max_length=10,
        choices=MasteryLevels.choices,
        default=MasteryLevels.ABSENT
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
    size = models.PositiveSmallIntegerField(null=True, blank=True)
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


class SecondaryStats(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='secondary_stats')
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


class CharacterSkill(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='skill_list')
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE)
    mastery_level = models.CharField(
        max_length=10,
        choices=MasteryLevels.choices,
        default=MasteryLevels.ABSENT,
    )

    class Meta:
        unique_together = ['character', 'skill']

    def __str__(self):
        return f"{self.character} - {self.skill} - {self.mastery_level}"


class CharacterBag(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='character_bag')
    max_capacity = models.IntegerField(default=0)
    capacity = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.character}'s Bag"


class InventoryItems(models.Model):
    inventory = models.ForeignKey(CharacterBag, on_delete=models.CASCADE, related_name='inventory')
    quantity = models.IntegerField(default=1)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item')

    def __str__(self):
        return f"{self.item.__str__()}({self.quantity})"


class EquippedItems(models.Model):
    equipped_items = models.ForeignKey(CharacterBag, on_delete=models.CASCADE, related_name='equipped_items')
    plate_armor = models.ForeignKey(
        InventoryItems,
        on_delete=models.CASCADE,
        related_name='plate_armor',
        null=True,
        blank=True,
        limit_choices_to={
            'pk__in': PlateArmor.objects.all().values_list('id', flat=True)}
    )
    first_weapon = models.ForeignKey(
        InventoryItems,
        on_delete=models.CASCADE,
        related_name='first_weapon',
        null=True,
        blank=True,
        limit_choices_to={
            'pk__in': Weapon.objects.all().values_list('id', flat=True)}
    )
    second_weapon = models.ForeignKey(
        InventoryItems,
        on_delete=models.CASCADE,
        related_name='second_weapon',
        null=True,
        blank=True,
        limit_choices_to={
            'pk__in': Weapon.objects.filter(two_hands=False).values_list('id', flat=True)}
    )
    worn_items = models.ManyToManyField(
        InventoryItems,
        related_name='worn_items',
        blank=True,
        limit_choices_to={
            'pk__in': WornItems.objects.all().values_list('id', flat=True)}
    )

    def __str__(self):
        return f"{self.equipped_items}'s equipped items"


class DefenceAndVulnerabilityDamage(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='defence_and_vulnerability')
    immunity = models.ManyToManyField(DamageType, related_name='immunity', blank=True)
    resistance = models.ManyToManyField(DamageType, related_name='resistance', blank=True)
    weakness = models.ManyToManyField(DamageType, related_name='weakness', blank=True)

    def __str__(self):
        return f"{self.character}'s defences and vulnerabilities"
