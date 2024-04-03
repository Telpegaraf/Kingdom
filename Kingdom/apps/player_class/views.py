from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.player_class.serializers import FeatureListSerializer, SpellFeatureListSerializer
from apps.player_class.models import ClassFeature
from rest_framework import status
from rest_framework.response import Response


class FeatureListView(APIView):
    """ Display all class's features """

    permission_classes = [IsAuthenticated]
    serializer_class = FeatureListSerializer

    def get(self, request, class_player_id):
        class_feature = ClassFeature.objects.select_related('class_player').prefetch_related('feats').\
            filter(class_player_id=class_player_id).all()
        serializer = self.serializer_class(class_feature, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SpellFeatureListView(APIView):
    """ Display class's spell feature """

    permission_classes = [IsAuthenticated]
    serializer_class = SpellFeatureListSerializer

    def get(self, request, class_player_id):
        class_feature = ClassFeature.ClassFeature.objects.select_related('class_player').\
            filter(class_player_id=class_player_id)
        serializer = self.serializer_class(class_feature, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
