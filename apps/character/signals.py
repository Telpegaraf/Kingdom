import math
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from apps.character.models import CharacterStats, CharacterBag, SecondaryStats, DefenceAndVulnerabilityDamage, \
    Character, EquippedItems, CharacterFeatList, SpellList, WeaponList, CharacterSkillList, CharacterSkillMastery, \
    CharacterWeaponMastery, CharacterCurrency, CharacterPoints
from apps.character.models import Skills, WeaponMastery
from apps.character.models import Currency
from apps.utils import disable_for_loaddata
from apps.general.models import DamageType, Race
from django.core.exceptions import ValidationError


@receiver(post_save, sender=Character)
@disable_for_loaddata
def create_list(sender, instance, created, **kwargs):
    """ create skill, feat, spell, weapon_mastery lists, when created character """
    if created:
        CharacterFeatList.objects.create(character=instance)
        CharacterSkillList.objects.create(character=instance)
        WeaponList.objects.create(character=instance)
        SpellList.objects.create(character=instance)
        DefenceAndVulnerabilityDamage.objects.create(character=instance)
        race = Race.objects.get(name=instance.race)
        character_points = CharacterPoints.objects.create(
            character=instance,
            strength=race.strength,
            dexterity=race.dexterity,
            constitution=race.constitution,
            intelligence=race.intelligence,
            wisdom=race.wisdom,
            charisma=race.charisma,
            free=race.free,
        )

        perception = instance.class_player.perception_mastery
        fortitude = instance.class_player.fortitude_mastery
        reflex = instance.class_player.reflex_mastery
        will = instance.class_player.will_mastery
        unarmed_mastery = instance.class_player.unarmed_mastery
        light_armor_mastery = instance.class_player.light_armor_mastery
        medium_armor_mastery = instance.class_player.medium_armor_mastery
        heavy_armor_mastery = instance.class_player.heavy_armor_mastery

        CharacterStats.objects.create(
            character=instance,
            strength=10+character_points.strength,
            dexterity=10+character_points.dexterity,
            constitution=10+character_points.constitution,
            intelligence=10+character_points.intelligence,
            wisdom=10+character_points.wisdom,
            charisma=10+character_points.charisma,
            perception_mastery=perception,
            fortitude_mastery=fortitude,
            reflex_mastery=reflex,
            will_mastery=will,
            unarmed_mastery=unarmed_mastery,
            light_armor_mastery=light_armor_mastery,
            medium_armor_mastery=medium_armor_mastery,
            heavy_armor_mastery=heavy_armor_mastery
        )

        existing_skills = Skills.objects.all()
        for skill in existing_skills:
            CharacterSkillMastery.objects.create(
                skill_list=instance.skill_list,
                skill=skill,
            )

        existing_weapon_mastery = WeaponMastery.objects.all()
        for weapon_mastery in existing_weapon_mastery:
            CharacterWeaponMastery.objects.create(
                weapon_list=instance.weapon_list,
                weapon=weapon_mastery,
            )


@receiver(post_save, sender=CharacterStats)
@disable_for_loaddata
def set_max_capacity(sender, instance, created, **kwargs):
    """ Set capacity character's bag"""
    if created:
        CharacterBag.objects.create(character=instance.character)


@receiver(post_save, sender=CharacterBag)
@disable_for_loaddata
def set_max_capacity(sender, instance, created, **kwargs):
    """ Set capacity character's bag"""
    if created:
        EquippedItems.objects.create(bag=instance)

        all_currency = Currency.objects.all()
        for currency in all_currency:
            CharacterCurrency.objects.create(
                bag=instance,
                currency=currency
            )


@receiver(post_save, sender=CharacterStats)
@disable_for_loaddata
def set_secondary_stats(sender, instance, created, **kwargs):
    """ set secondary stats, when created character """
    level = instance.character.level
    class_health = instance.character.class_player.health_by_level
    health = math.floor((instance.constitution/2)-5)*level+(class_health*level)

    if created:
        SecondaryStats.objects.create(
            character=instance.character,
            max_health=health,
            health=health
        )


@receiver(m2m_changed, sender=DefenceAndVulnerabilityDamage.immunity.through)
@receiver(m2m_changed, sender=DefenceAndVulnerabilityDamage.resistance.through)
@receiver(m2m_changed, sender=DefenceAndVulnerabilityDamage.weakness.through)
def validate_unique_damage_types(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "pre_add":
        all_damage_types = set(instance.immunity.all()) | set(instance.resistance.all()) | set(instance.weakness.all())
        new_damage_types = set(DamageType.objects.filter(pk__in=pk_set))
        if len(all_damage_types.intersection(new_damage_types)) > 0:
            raise ValidationError("Damage cannot be present in more than one field.")
