from django.urls import path
from apps.character.views import CharacterOverallView, CharacterDetailView, CharacterCreateView, \
    AddItemView, EquipItemView, SetSecondaryStatsView, LevelUpView, SetStatsView, SetSpeedView, SetMasteryView, \
    SecondaryStatsView, SetSkillsView, SetSkillMasteryView, SetFeatView, SetSpellView, SetCondition, \
    UnEquipArmorView, UnEquipFirstWeaponView, UnEquipSecondWeaponView, DeleteWornItemView, RemoveItemView

urlpatterns = [
    path('add-item/<int:character_id>/', AddItemView.as_view(), name='add-item'),
    path('create/', CharacterCreateView.as_view(), name='character-create'),
    path('detail/<int:character_id>/', CharacterDetailView.as_view(), name='character-detail'),
    path('equip-item/', EquipItemView.as_view(), name='equip-item'),
    path('level-up/<int:character_id>/', LevelUpView.as_view(), name='level-up'),
    path('remove-item/<int:item_id>/', RemoveItemView.as_view(), name='remove-item'),
    path('secondary-stats/<int:character_id>/', SecondaryStatsView.as_view(), name='secondary-stats'),
    path('set-condition/<int:character_id>/', SetCondition.as_view(), name='set-condition'),
    path('set-feat/<int:character_id>/', SetFeatView.as_view(), name='set-feat'),
    path('set-mastery/<int:character_id>/', SetMasteryView.as_view(), name='set-mastery'),
    path('set-secondary-stats/<int:character_id>/', SetSecondaryStatsView.as_view(), name='set-secondary-stats'),
    path('set-skill/<int:character_id>/', SetSkillsView.as_view(), name='set-skills'),
    path('set-skill-mastery/<int:skill_id>/', SetSkillMasteryView.as_view(), name='set-skill-mastery'),
    path('set-stats/<int:character_id>/', SetStatsView.as_view(), name='set-stats'),
    path('set-speed/<int:character_id>/', SetSpeedView.as_view(), name='set-speed'),
    path('set-spell/<int:character_id>/', SetSpellView.as_view(), name='set-spell'),
    path('overall/', CharacterOverallView.as_view(), name='character-overall'),
    path('un-equip-armor/<int:character_id>/', UnEquipArmorView.as_view(), name='un-equip-armor'),
    path('un-equip-first/<int:character_id>/', UnEquipFirstWeaponView.as_view(), name='un-equip-first'),
    path('un-equip-second/<int:character_id>/', UnEquipSecondWeaponView.as_view(), name='un-equip-second'),
    path('un-equip-worn/<int:character_id>/<int:item_id>/', DeleteWornItemView.as_view(), name='un-equip-worn'),
]
