from django.urls import path
from apps.character import views

urlpatterns = [
    path('add-item/<int:character_id>/', views.AddItemView.as_view(), name='add-item'),
    path('create/', views.CharacterCreateView.as_view(), name='character-create'),
    path('detail/<int:character_id>/', views.CharacterDetailView.as_view(), name='character-detail'),
    path('equip-item/', views.EquipItemView.as_view(), name='equip-item'),
    path('level-up/<int:character_id>/', views.LevelUpView.as_view(), name='level-up'),
    path('remove-item/<int:item_id>/', views.RemoveItemView.as_view(), name='remove-item'),
    path('secondary-stats/<int:character_id>/', views.SecondaryStatsView.as_view(), name='secondary-stats'),
    path('set-condition/<int:character_id>/', views.SetCondition.as_view(), name='set-condition'),
    path('set-feat/<int:character_id>/', views.SetFeatView.as_view(), name='set-feat'),
    path('set-mastery/<int:character_id>/', views.SetMasteryView.as_view(), name='set-mastery'),
    path('set-secondary-stats/<int:character_id>/', views.SetSecondaryStatsView.as_view(), name='set-secondary-stats'),
    path('set-skill/<int:character_id>/', views.SetSkillsView.as_view(), name='set-skills'),
    path('set-skill-mastery/<int:skill_id>/', views.SetSkillMasteryView.as_view(), name='set-skill-mastery'),
    path('set-speed/', views.SetSpeedView.as_view(), name='set-speed'),
    path('set-spell/<int:character_id>/', views.SetSpellView.as_view(), name='set-spell'),
    path('set-stats/', views.ChangeStatView.as_view(), name='change-stats'),
    path('overall/', views.CharacterOverallView.as_view(), name='character-overall'),
    path('un-equip-armor/<int:character_id>/', views.UnEquipArmorView.as_view(), name='un-equip-armor'),
    path('un-equip-first/<int:character_id>/', views.UnEquipFirstWeaponView.as_view(), name='un-equip-first'),
    path('un-equip-second/<int:character_id>/', views.UnEquipSecondWeaponView.as_view(), name='un-equip-second'),
    path('un-equip-worn/<int:character_id>/<int:item_id>/', views.DeleteWornItemView.as_view(), name='un-equip-worn'),
]
