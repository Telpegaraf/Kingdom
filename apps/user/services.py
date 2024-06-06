import json
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import generate_random_password


class SocialService:
    @staticmethod
    def register_social(email):
        User = get_user_model()
        filtered_by_email = User.objects.filter(email=email.lower())
        if filtered_by_email.exists():
            return filtered_by_email.first(), False
        else:
            user = {
                "email": email.lower(),
                "password": generate_random_password()
            }
            user = User.objects.create_user(**user)
            user.is_active = True
            user.save()
            return user, True

    @staticmethod
    def get_social(serializer):
        data = serializer.data.get("auth_token")
        data = data.replace("'", '"')
        user_data = json.loads(data)
        email = user_data.get('email')
        user, new_account = SocialService.register_social(email)
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "email": user.email,
        }
