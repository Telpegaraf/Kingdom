from django.urls import path
from apps.player_class.views import FeatureListView, SpellFeatureListView

urlpatterns = [
    path('feature-list/<int:class_player_id>/', FeatureListView.as_view(), name='feature-list'),
    path('spell-feature-list/<int:class_player_id>/', SpellFeatureListView.as_view(), name='spell-feature-list'),
]
