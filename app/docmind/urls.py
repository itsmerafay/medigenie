from django.urls import path, include
from .views import *


RAG_SESSION_URL_PATTERNS = [    
   path(
        'create/', RagSessionCreateAPIView.as_view(),
        name='rag-session-create'
    ),

]

RAG_MESSAGE_URL_PATTERNS = [    
   path(
        'create/', RagMessageCreateAPIView.as_view(),
        name='rag-session-create'
    ),


]


urlpatterns = [
    path('rag/session/', include(RAG_SESSION_URL_PATTERNS)),
    path('rag/message/', include(RAG_MESSAGE_URL_PATTERNS))
]
