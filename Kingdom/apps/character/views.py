from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CharacterOverallSerializer
from .models import Character


class CharacterOverallView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CharacterOverallSerializer

    def get(self, request, *args, **kwargs):
        character = Character.objects.select_related('race', 'class_player', 'god', 'domain').\
            prefetch_related('intentions').all()
        serializer = self.serializer_class(character, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
