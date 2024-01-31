from django.urls import path
from apps.character.views import CharacterOverallView, CharacterDetailView, CharacterCreateView,\
    AddItemView, EquipItemView, ChangeStatsView, LevelUpView, SetStatsView


urlpatterns = [
    path('overall/', CharacterOverallView.as_view(), name='character-overall'),
    path('detail/<int:character_id>/', CharacterDetailView.as_view(), name='character-detail'),
    path('create/', CharacterCreateView.as_view(), name='character-create'),
    path('add-item/', AddItemView.as_view(), name='add_item'),
    path('equip_item/', EquipItemView.as_view(), name='equip-item'),
    path('change-stats/<int:pk>/', ChangeStatsView.as_view(), name='change-stats'),
    path('level-up/<int:pk>/', LevelUpView.as_view(), name='level-up'),
    path('set-stats/<int:character_id>/', SetStatsView.as_view(), name='set-stats')
]
