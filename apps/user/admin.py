from django.contrib import admin
from apps.user.apps import CustomUser

admin.site.register(CustomUser, admin.ModelAdmin)
