from django.contrib import admin
from apps.god.apps import God, Domains

admin.site.register(God, admin.ModelAdmin)
admin.site.register(Domains, admin.ModelAdmin)
