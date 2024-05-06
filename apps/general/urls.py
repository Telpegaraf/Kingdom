from django.urls import path
from apps.general.apps import SkillListView

urlpatterns = [
    path('skill-list/', SkillListView.as_view(), name='skill-list'),
    path('weapon-mastery-list/', SkillListView.as_view(), name='weapon-mastery-list'),
]
