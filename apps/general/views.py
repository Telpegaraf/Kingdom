from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.general.apps import Skills, WeaponMastery
from apps.general.apps import SkillListSerializer, WeaponMasteryListSerializer


class SkillListView(ListAPIView):
    queryset = Skills.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SkillListSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WeaponMasteryListView(ListAPIView):
    queryset = WeaponMastery.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = WeaponMasteryListSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
