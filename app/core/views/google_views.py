from django.conf import settings

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_REDIRECT_URL
    client_class = OAuth2Client

    def process_login(self):    
        self.user.role = "User"
        self.user.save()
        return super().process_login()