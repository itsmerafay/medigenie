from django.conf import settings

from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from drf_spectacular.utils import extend_schema

from core.serializers import RegisterUserSerializer
from core.views.custom_registration_views import CustomRegisterView


class UserRegistrationAPIView(CustomRegisterView):
    serializer_class = RegisterUserSerializer
    @extend_schema(
        responses={
            200: {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "example": "ok"},
                    "message": {"type": "string", "example": "Please check your email for the verification code."}
                }
            }
        }
    )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["role"] = "User"           
        return context