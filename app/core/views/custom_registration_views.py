from dj_rest_auth.registration.views import RegisterView
from core.serializers import RegisterUserSerializer

class CustomRegisterView(RegisterView):
    serializer_class = RegisterUserSerializer

    def get_response_data(self, user, *args, **kwargs):
        return {
            "status": "ok",
            "message": "Please check your email for the verification code."
        }
