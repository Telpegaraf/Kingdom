from django.contrib import admin
from apps.player_class.models import ClassCharacter, Feat, ClassFeature, ClassSpellFeature, Background


class ClassFeatureAdmin(admin.ModelAdmin):
    ordering = ('class_player__name', 'level')


class ClassSpellFeatureAdmin(admin.ModelAdmin):
    ordering = ('class_player__name', 'class_level')


model_list = [ClassCharacter, Feat, Background]

admin.site.register(ClassFeature, ClassFeatureAdmin)
admin.site.register(ClassSpellFeature, ClassSpellFeatureAdmin)

for model in model_list:
    admin.site.register(model, admin.ModelAdmin)
