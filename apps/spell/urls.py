from django.urls import path
from apps.spell.views import SpellListView, SpellDetailView


urlpatterns = [
    path('spell-list', SpellListView.as_view(), name='spell-list'),
    path('spell-detail/', SpellDetailView.as_view(), name='spell-detail')
]
