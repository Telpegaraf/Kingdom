from django.urls import path
from apps.equipment.apps import ItemView, ItemDetailView


urlpatterns = [
    path('items/<str:item_type>/', ItemView.as_view(), name='items'),
    path('items/<str:item_type>/<int:pk>/', ItemDetailView.as_view(), name='item')
]
