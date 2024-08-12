from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from apps.god import models, resources


@admin.register(models.God)
class GodAdmin(ImportExportModelAdmin):
    ordering = ('name',)
    resource_class = resources.GodResource


@admin.register(models.Domains)
class DomainsAdmin(ImportExportModelAdmin):
    ordering = ('name',)
    resource_class = resources.DomainResources
