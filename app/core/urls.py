from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *


AUTH_URL_PATTERNS = [
    path('', include('dj_rest_auth.urls')),
    path(
        'token/refresh/', TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'log-in/', CustomLoginView.as_view(),
        name='custom-login'
    ),
    path(
        'verify-code/', VerificicationCodeAPIView.as_view(),
        name='verify-code'
    ),
    path('registration/', UserRegistrationAPIView.as_view(), 
        name="non-partner-registration" ),
    path(
        'password_reset/', 
        include('django_rest_passwordreset.urls',
        namespace='password_reset')
    ), 

]

GOOGLE_URL_PATTERNS = [
    path('', GoogleLogin.as_view(), name='socialaccount_signup'),
]


PROFILE_URL_PATTERNS = [    
    path(
        'retrieve/', ProfileRetrieveAPIView.as_view(),
        name='user-profile-retrieve'
    ),
   path(
        'update/', ProfileUpdateAPIView.as_view(),
        name='user-profile-retrieve'
    ),
   path(
        'delete/', ProfileDeleteAPIView.as_view(),
        name='user-profile-retrieve'
    ),

]

urlpatterns = [
    path('auth/', include(AUTH_URL_PATTERNS)),
    path('google/', include(GOOGLE_URL_PATTERNS)),
    path('profiles/', include(PROFILE_URL_PATTERNS))
]
