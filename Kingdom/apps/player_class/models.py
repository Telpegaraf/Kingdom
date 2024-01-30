from django.db import models
from apps.general.models import MasteryLevels, Action, Prerequisite, FeatTrait, Requirements, Trigger
from apps.spell.models import SpellTradition


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
    tradition = models.ForeignKey(SpellTradition, on_delete=models.CASCADE, related_name='class_tradition',
                                  null=True, blank=True)

    def __str__(self):
        return self.name


class ClassFeat(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=600)
    class_character = models.ForeignKey(ClassCharacter, on_delete=models.CASCADE, related_name='feat',
                                        null=True, blank=True)
    level = models.PositiveSmallIntegerField(default=0)
    action = models.ForeignKey(Action, on_delete=models.CASCADE, related_name='action_feat',
                               null=True, blank=True)
    trigger = models.ForeignKey(Trigger, on_delete=models.CASCADE, related_name='trigger_feat',
                                null=True, blank=True)
    prerequisite = models.ForeignKey(Prerequisite, on_delete=models.CASCADE, related_name='prerequisite',
                                     null=True, blank=True)
    traits = models.ManyToManyField(FeatTrait, related_name='trait', blank=True)
    requirements = models.ForeignKey(Requirements, on_delete=models.CASCADE, related_name='requirements',
                                     null=True, blank=True)

    def __str__(self):
        return self.name


class ClassFeature(models.Model):
    class_player = models.ForeignKey(ClassCharacter, on_delete=models.CASCADE, related_name='feature')
    level = models.PositiveSmallIntegerField(default=1)
    feats = models.ManyToManyField(ClassFeat, blank=True, related_name='feats_feature')
    class_feat_count = models.PositiveSmallIntegerField(default=0)
    general_feat_count = models.PositiveSmallIntegerField(default=0)
    background_feat_count = models.PositiveSmallIntegerField(default=0)
    stats_boost = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.class_player} - {self.level}"
