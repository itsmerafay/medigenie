from django.urls import path, include
from .views import ResearchMessageCreateAPIView, ResearchSessionCreateAPIView


RESEARCH_MESSAGE_URL_PATTERNS = [    
   path(
        'create/', ResearchMessageCreateAPIView.as_view(),
        name='research-message-create'
    ),
]

RESEARCH_SESSION_URL_PATTERNS = [
   path(
        'create/', ResearchSessionCreateAPIView.as_view(),
        name='research-session-create'
    ),
]

urlpatterns = [
    path('research/message/', include(RESEARCH_MESSAGE_URL_PATTERNS)),
    path('research/session/', include(RESEARCH_SESSION_URL_PATTERNS)),
]
