from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.player_class.serializers import FeatureListSerializer
from apps.player_class.models import ClassFeature
from rest_framework import status
from rest_framework.response import Response


class FeatureListView(APIView):
    """ Display all class's features """

    permission_classes = [IsAuthenticated]
    serializer_class = FeatureListSerializer

    def get(self, request):
        class_feature = ClassFeature.objects.all().select_related('class_player').prefetch_related('feats')
        serializer = self.serializer_class(class_feature, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
