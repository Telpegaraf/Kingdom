from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import GodOverallSerializer
from .models import God


class GodOverallView(APIView):
    """ Show all gods """
    permission_classes = [IsAuthenticated]
    serializer_class = GodOverallSerializer

    def get(self, request, *args, **kwargs):
        gods = God.objects.prefetch_related('domain').all()
        serializer = self.serializer_class(gods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
