from django.contrib import admin
from apps.god import models


@admin.register(models.God)
class GodAdmin(admin.ModelAdmin):
    ordering = ('name',)


@admin.register(models.Domains)
class DomainsAdmin(admin.ModelAdmin):
    ordering = ('name',)
