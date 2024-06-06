from django.urls import path
from .views import GodOverallView


urlpatterns = [
    path('overall/', GodOverallView.as_view(), name='overall')
]
