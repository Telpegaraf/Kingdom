from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


# class EquipmentOverallView(APIView):
#     """ Show all equipment """
#     permission_classes = [IsAuthenticated]
#     serializer_class = EquipmentOverallSerializer
#
#     def get(self, request, *args, **kwargs):
#         equipment = Equipment.objects.all()
#         serializer = self.serializer_class(equipment, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class EquipmentDetailView(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = EquipmentDetailSerializer
#
#     def get(self, request, equipment_id):
#         equipment = get_object_or_404(Equipment, pk=equipment_id)
#         serializer = self.serializer_class(equipment)
#         return Response(serializer.data, status=status.HTTP_200_OK)
