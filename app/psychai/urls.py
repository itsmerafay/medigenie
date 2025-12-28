from encodings.punycode import T
from django.urls import path, include
from psychai.views import *


THERAPIST_SESSION_URL_PATTERNS = [    
   path(
        'create/', TherapistSessionCreateAPIView.as_view(),
        name='therapist-session-create'
    ),

]

THERAPIST_MESSAGE_URL_PATTERNS = [    
   path(
        'create/', TherapistChatCreateAPIView.as_view(),
        name='therapist-session-create'
    ),


]


urlpatterns = [
    path('therapist/session/', include(THERAPIST_SESSION_URL_PATTERNS)),
    path('therapist/message/', include(THERAPIST_MESSAGE_URL_PATTERNS))
]
