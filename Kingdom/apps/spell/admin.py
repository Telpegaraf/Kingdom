from django.contrib import admin
from apps.spell.models import Spell, SpellCast, SpellTrait, SpellComponent, SpellSchool, SpellTradition


admin.site.register(Spell)
admin.site.register(SpellCast)
admin.site.register(SpellTrait)
admin.site.register(SpellComponent)
admin.site.register(SpellSchool)
admin.site.register(SpellTradition)
