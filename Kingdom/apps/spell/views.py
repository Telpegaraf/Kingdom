from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db.models import ObjectDoesNotExist

from apps.spell.serializers import SpellDetailSerializer, SpellListSerializer
from apps.spell.models import Spell


class SpellListView(APIView):

    """ Show all spells, and transferred values for possible filters """

    permission_classes = [IsAuthenticated]
    serializer_class = SpellListSerializer

    def get(self, request):
        spell = Spell.objects.all()
        serializer = self.serializer_class(spell, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SpellDetailView(APIView):

    """ Show all info about spell,
        id = required query param
     """

    permission_classes = [IsAuthenticated]
    serializer_class = SpellDetailSerializer

    def get(self, request):
        pk = request.query_params.get('id')
        try:
            spell = Spell.objects.select_related('school', 'cast').get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"message": "id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(spell)
        return Response(serializer.data, status=status.HTTP_200_OK)
