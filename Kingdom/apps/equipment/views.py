from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ItemSerializer, PlateArmorSerializer, WeaponSerializer, WornItemsSerializer,\
    PlateArmorDetailSerializer, WeaponDetailSerializer, WornItemsDetailSerializer
from .models import Item, Weapon, PlateArmor, WornItems


class ItemView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    ITEM_TYPE_MAPPING = {
        'armor': (PlateArmorSerializer, PlateArmor.objects.all()),
        'weapon': (WeaponSerializer, Weapon.objects.all()),
        'worn_items': (WornItemsSerializer, WornItems.objects.all()),
        'all': (ItemSerializer, Item.objects.all()),
    }

    def get_serializer_class(self):
        item_type = self.kwargs.get('item_type', 'all')
        serializer_class, _ = self.ITEM_TYPE_MAPPING.get(item_type, (ItemSerializer, None))
        return serializer_class

    def get_queryset(self):
        item_type = self.kwargs.get('item_type', 'all')
        _, queryset = self.ITEM_TYPE_MAPPING.get(item_type, (ItemSerializer, Item.objects.all()))
        return queryset


class ItemDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    ITEM_TYPE_MAPPING = {
        'armor': PlateArmorDetailSerializer,
        'weapon': WeaponDetailSerializer,
        'worn_items': WornItemsDetailSerializer,
    }

    def get_serializer_class(self):
        item_type = self.kwargs.get('item_type')
        return self.ITEM_TYPE_MAPPING.get(item_type, ItemSerializer)

    def get_queryset(self):
        item_type = self.kwargs.get('item_type')
        if item_type == 'armor':
            return PlateArmor.objects.all()
        elif item_type == 'weapon':
            return Weapon.objects.all()
        elif item_type == 'worn_items':
            return WornItems.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        item_type = self.kwargs.get('item_type')
        item_id = self.kwargs.get('pk')

        if item_type == 'armor':
            return get_object_or_404(queryset, pk=item_id)
        elif item_type == 'weapon':
            return get_object_or_404(queryset, pk=item_id)
        elif item_type == 'worn_items':
            return get_object_or_404(queryset, pk=item_id)
        elif item_type == 'all':
            return get_object_or_404(queryset, pk=item_id)
        else:
            return None




