from django.urls import path
from apps.user.views import GoogleView


urlpatterns = [
    path('google-auth/', GoogleView.as_view(), name='google-auth')
]
