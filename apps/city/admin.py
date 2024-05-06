from django.contrib import admin
from apps.city.apps import Government, Kingdom, Region, City

models_list = [Government, Kingdom, Region, City]

for model in models_list:
    admin.site.register(model, admin.ModelAdmin)
