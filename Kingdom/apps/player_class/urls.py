from django.urls import path
from apps.player_class.views import FeatureListView

urlpatterns = [
    path('feature-list/', FeatureListView.as_view(), name='feature-list'),
]