from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.spell.serializers import SpellOverallSerializer
from apps.spell.models import Spell


class SpellOverallView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SpellOverallSerializer
    queryset = Spell.objects.all()
