from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
#from .serializers import EquipmentOverallSerializer
from .models import Equipment


# class EquipmentOverall(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = EquipmentOverallSerializer
#
#     def get(self, request, *args, **kwargs):
#         equipment = Equipment.objects.all()
#         serializer = self.serializer_class(equipment, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
