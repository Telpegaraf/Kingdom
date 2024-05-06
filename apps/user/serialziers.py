from rest_framework import serializers
from apps.user.apps import Google


class GoogleSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)

        try:
            user_data['sub']
        except:
            raise serializers.ValidationError("invalid token")

        return {
            "email": user_data.get("email"),
        }
