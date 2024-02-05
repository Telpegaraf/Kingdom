import math
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from apps.character.models import CharacterStats, CharacterBag, SecondaryStats, DefenceAndVulnerabilityDamage,\
     Character, EquippedItems, CharacterFeatList, SpellList, WeaponList, CharacterSkillList, CharacterSkillMastery,\
     CharacterWeaponMastery, CharacterCurrency
from apps.general.models import Skills, WeaponMastery
from apps.equipment.models import Currency


@receiver(post_save, sender=Character)
def set_mastery(sender, instance, created, **kwargs):
    """ Set general when character created """
    if created:
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
            perception_mastery=perception,
            fortitude_mastery=fortitude,
            reflex_mastery=reflex,
            will_mastery=will,
            unarmed_mastery=unarmed_mastery,
            light_armor_mastery=light_armor_mastery,
            medium_armor_mastery=medium_armor_mastery,
            heavy_armor_mastery=heavy_armor_mastery
        )


@receiver(post_save, sender=Character)
def create_list(sender, instance, created, **kwargs):
    """ create skill, feat, spell, weapon_mastery lists, when created character """
    if created:
        CharacterFeatList.objects.create(character=instance)
        CharacterSkillList.objects.create(character=instance)
        WeaponList.objects.create(character=instance)
        SpellList.objects.create(character=instance)
        DefenceAndVulnerabilityDamage.objects.create(character=instance)

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
def set_max_capacity(sender, instance, created, **kwargs):
    """ Set capacity character's bag"""
    if created:
        CharacterBag.objects.create(character=instance.character)


@receiver(post_save, sender=CharacterBag)
def set_max_capacity(sender, instance, created, **kwargs):
    """ Set capacity character's bag"""
    if created:
        EquippedItems.objects.create(equipped_items=instance)

        all_currency = Currency.objects.all()
        for currency in all_currency:
            CharacterCurrency.objects.create(
                character=instance,
                currency=currency
            )


@receiver(post_save, sender=CharacterStats)
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


@receiver(m2m_changed, sender=EquippedItems.worn_items.through)
def check_max_worn_items(sender, instance, action, reverse, model, pk_set, **kwargs):
    max_worn_items = 10

    if action == 'pre_add' and len(pk_set) + instance.worn_items.count() > max_worn_items:
        raise ValidationError(f"Adding more than {max_worn_items} worn items is not allowed.")
