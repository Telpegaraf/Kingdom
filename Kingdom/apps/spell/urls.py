from django.urls import path
from apps.spell.views import SpellOverallView


urlpatterns = [
    path('spell-list', SpellOverallView.as_view(), name='spell-list')
]
