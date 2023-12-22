from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CharacterOverallSerializer, CharacterDetailSerializer
from .models import Character


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


class LevelUpView(APIView):
    """ Increase character's level by id """
    permission_classes = [IsAuthenticated]

    def post(self, request, character_id):
        try:
            character = Character.objects.get(pk=character_id)
            character.level += 1
            character.save()
            return Response({'message': 'Level increased successfully'}, status=status.HTTP_200_OK)
        except Character.DoesNotExist:
            return Response({'error': 'Character not found'}, status=status.HTTP_404_NOT_FOUND)


