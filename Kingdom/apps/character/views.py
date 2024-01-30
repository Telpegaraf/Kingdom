from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.character.serializers import CharacterOverallSerializer, CharacterDetailSerializer, CharacterSerializer,\
    AddItemSerializer, EquipItemSerializer, SecondaryStatsSerializer, LevelUpSerializer
from apps.character.models import Character, SecondaryStats


class CharacterOverallView(APIView):
    """ Show all characters """
    permission_classes = [IsAuthenticated]
    serializer_class = CharacterOverallSerializer

    def get(self, request, *args, **kwargs):
        character = Character.objects.all()
        serializer = self.serializer_class(character, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CharacterDetailView(APIView):
    """ Show detail info about character """
    permission_classes = [IsAuthenticated]
    serializer_class = CharacterDetailSerializer

    def get(self, request, character_id):
        character = get_object_or_404(Character, pk=character_id)
        serializer = self.serializer_class(character)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CharacterCreateView(APIView):
    """ Create new character """
    permission_classes = [IsAuthenticated]
    serializer_class = CharacterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AddItemView(APIView):
    """ Add new item in inventory """
    permission_classes = [IsAuthenticated]
    serializer_class = AddItemSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            inventory_item = serializer.save()
            return Response({"message": f"Item added to inventory. {inventory_item}"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EquipItemView(APIView):
    """ Equip Item from inventory """
    permission_classes = [IsAuthenticated]
    serializer_class = EquipItemSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        return Response({"message": f"{item} equipped"}, status=status.HTTP_200_OK)


class ChangeStatsView(APIView):
    """ Change characteristics (health and e.t.c) """

    permission_classes = [IsAuthenticated]
    serializer_class = SecondaryStatsSerializer

    def patch(self, request, pk):
        secondary_stats = get_object_or_404(SecondaryStats, pk=pk)
        serializer = self.serializer_class(secondary_stats, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class LevelUpView(APIView):
    """ Change character's level """

    permission_classes = [IsAuthenticated]
    serializer_class = LevelUpSerializer

    def patch(self, request, pk):
        character = get_object_or_404(Character, pk=pk)
        serializer = self.serializer_class(character, data=request.data, partial=True)
        new_level = serializer.initial_data.get('level')
        if new_level is not None and new_level == character.level + 1 and new_level <= 20:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid level value'}, status=status.HTTP_400_BAD_REQUEST)
