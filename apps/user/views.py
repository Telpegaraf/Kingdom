from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from apps.user.serialziers import GoogleSerializer
from apps.user.services import SocialService


class GoogleView(GenericAPIView):
    """ Google authenticate and register """

    serializer_class = GoogleSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = SocialService.get_social(serializer)

            return Response(user, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({f"error {e}"}, status=status.HTTP_400_BAD_REQUEST)
