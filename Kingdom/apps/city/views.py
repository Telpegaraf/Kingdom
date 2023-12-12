from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import CityOverallSerializer
from .models import Kingdom


class CityOverallView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CityOverallSerializer

    def get(self, request, *args, **kwargs):
        kingdom = Kingdom.objects.all()
        serializer = self.serializer_class(kingdom, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
