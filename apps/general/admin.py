from django.contrib import admin
from apps.general import models


@admin.register(models.DamageType)
class DamageTypeAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(models.Skills)
class SkillsAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(models.WeaponMastery)
class WeaponMasteryAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(models.Race)
class RaceAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(models.Action)
class ActionAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(models.Prerequisite)
class PrerequisiteAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(models.FeatTrait)
class FeatTraitAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(models.Requirements)
class RequirementsAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(models.Trigger)
class TriggerAdmin(admin.ModelAdmin):
    ordering = ('name',)
