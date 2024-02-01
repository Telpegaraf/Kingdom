from django.urls import path
from apps.character.views import CharacterOverallView, CharacterDetailView, CharacterCreateView,\
    AddItemView, EquipItemView, SetSecondaryStatsView, LevelUpView, SetStatsView, SetSpeedView, SetMasteryView,\
    SecondaryStatsView, SetSkillsView, SetSkillMasteryView

urlpatterns = [
    path('overall/', CharacterOverallView.as_view(), name='character-overall'),
    path('detail/<int:character_id>/', CharacterDetailView.as_view(), name='character-detail'),
    path('create/', CharacterCreateView.as_view(), name='character-create'),
    path('add-item/', AddItemView.as_view(), name='add_item'),
    path('equip_item/', EquipItemView.as_view(), name='equip-item'),
    path('level-up/<int:character_id>/', LevelUpView.as_view(), name='level-up'),
    path('set-stats/<int:character_id>/', SetStatsView.as_view(), name='set-stats'),
    path('set-speed/<int:character_id>/', SetSpeedView.as_view(), name='set-speed'),
    path('set-mastery/<int:character_id>/', SetMasteryView.as_view(), name='set-mastery'),
    path('secondary-stats/<int:character_id>/', SecondaryStatsView.as_view(), name='secondary-stats'),
    path('set-secondary-stats/<int:character_id>/', SetSecondaryStatsView.as_view(), name='change-stats'),
    path('set-skills/<int:character_id>/', SetSkillsView.as_view(), name='set-skills'),
    path('set-skill-mastery/<int:skill_id>/', SetSkillMasteryView.as_view(), name='set-skill-mastery'),
]
