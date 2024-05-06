from django.urls import path, include
from .views import CityOverallView

urlpatterns = [
    path('overall/', CityOverallView.as_view(), name='overall'),
]
