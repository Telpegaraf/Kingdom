from django.urls import path, include


urlpatterns = [
    path('city/', include('apps.city.urls')),
    path('character/', include('apps.character.urls')),
    path('equipment/', include('apps.equipment.urls')),
    path('god/', include('apps.god.urls')),
    path('user/', include('apps.user.urls')),
    path('spell/', include('apps.spell.urls')),
    path('class/', include('apps.player_class.urls')),
    path('general/', include('apps.general.urls')),
]
