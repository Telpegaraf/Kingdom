import math
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db.models import Sum, DecimalField, F
from django.db.models.signals import post_save, m2m_changed, pre_save, post_delete
from django.dispatch import receiver
from .models import CharacterStats, CharacterBag, InventoryItems, SecondaryStats, DefenceAndVulnerabilityDamage,\
     Character, EquippedItems
from apps.player_class.models import ClassFeature
from apps.general.models import DamageType


# @receiver(pre_save, sender=Character)
# def character_level_changed(sender, instance, **kwargs):
#     if instance.level == 1:
#         return
#     character = Character.objects.prefetch_related('secondary_stats', 'character_stats').get(id=instance.id)
#     character_stats = instance.character_stats.first()
#     health_by_constitution = math.floor((character_stats.constitution/2) - 5)
#     secondary_stats = instance.secondary_stats.first()
#     character_class = character.class_player
#     level = instance.level
#     feature = ClassFeature.objects.select_related('class_player').get(level=level, class_player=character_class)
#     health = feature.class_player.health_by_level + health_by_constitution
#     instance.stat_count += feature.stats_boost
#     instance.class_feat_count += feature.class_feat_count
#     instance.general_feat_count += feature.general_feat_count
#     instance.background_feat_count += feature.background_feat_count
#     instance.skill_count += feature.skill_count
#     secondary_stats.max_health += health
#     secondary_stats.health += health
#     secondary_stats.save()


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


@receiver(post_save, sender=CharacterStats)
def set_max_capacity(sender, instance, **kwargs):
    """ Set capacity character's bag"""
    capacity = math.floor(instance.strength/2)+5
    bag = instance.character.character_bag.first()

    if bag:
        bag.max_capacity = capacity
        bag.save()
    else:
        CharacterBag.objects.create(character=instance.character, max_capacity=capacity)


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


@receiver(post_save, sender=InventoryItems)
def set_current_capacity(sender, instance, **kwargs):
    """ Set current capacity, when inventory updated """
    inventory = instance.inventory
    total_weight = inventory.inventory.aggregate(
        total_weight=Sum(F('item__weight') * F('quantity'), output_field=DecimalField())
    )['total_weight'] or Decimal('0.0')
    inventory.capacity = total_weight
    inventory.save()


@receiver(post_save, sender=CharacterBag)
def set_speed(sender, instance, **kwargs):
    """ Set character's speed by current capacity """
    character_stats = instance.character.character_stats.first()
    if instance.capacity > instance.max_capacity:
        character_stats.speed = 0
    elif instance.capacity >= (instance.max_capacity/2):
        character_stats.speed = character_stats.speed/2
    else:
        character_stats.speed = character_stats.max_speed
    CharacterStats.objects.filter(character_id=instance.character.id).update(speed=character_stats.speed)


@receiver(m2m_changed, sender=DefenceAndVulnerabilityDamage.immunity.through)
@receiver(m2m_changed, sender=DefenceAndVulnerabilityDamage.resistance.through)
@receiver(m2m_changed, sender=DefenceAndVulnerabilityDamage.weakness.through)
def validate_unique_damage_types(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "pre_add":
        all_damage_types = set(instance.immunity.all()) | set(instance.resistance.all()) | set(instance.weakness.all())
        new_damage_types = set(DamageType.objects.filter(pk__in=pk_set))
        if len(all_damage_types.intersection(new_damage_types)) > 0:
            raise ValidationError("Damage cannot be present in more than one field.")


@receiver(m2m_changed, sender=EquippedItems.worn_items.through)
def check_max_worn_items(sender, instance, action, reverse, model, pk_set, **kwargs):
    max_worn_items = 10

    if action == 'pre_add' and len(pk_set) + instance.worn_items.count() > max_worn_items:
        raise ValidationError(f"Adding more than {max_worn_items} worn items is not allowed.")
