from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import TokenUsage, hash_token

class TokenManager:
    @staticmethod
    def generate_tokens(user: User) -> dict:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return {
            'refresh': str(refresh),
            'access': access_token,
        }

    @staticmethod
    def save_token_usage(user: User, access_token: str, ip_address: str = None) -> None:
        TokenUsage.objects.create(user=user,
                                  token_hash=hash_token(access_token),
                                  ip_address=ip_address
                                  )