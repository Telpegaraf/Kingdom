from django.db.models import Prefetch
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import CityOverallSerializer
from .models import Kingdom, City, Region


class CityOverallView(APIView):
    """ Show all cities """
    permission_classes = [IsAuthenticated]
    serializer_class = CityOverallSerializer

    def get(self, request, *args, **kwargs):
        kingdoms = Kingdom.objects.select_related('form_of_government', 'ruler').prefetch_related(
            Prefetch('region', queryset=Region.objects.select_related('form_of_government', 'ruler').prefetch_related(
                Prefetch('city', queryset=City.objects.select_related('form_of_government', 'ruler').prefetch_related(
                    'temples'
                ))
            ))
        ).all()
        serializer = self.serializer_class(kingdoms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

