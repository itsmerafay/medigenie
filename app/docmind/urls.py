from django.urls import path, include
from .views import *


RAG_SESSION_URL_PATTERNS = [    
   path(
        'create/', RagSessionCreateAPIView.as_view(),
        name='rag-session-create'
    ),
   path(
        '<uuid:id>/retrieve/', RagSessionRetrieveAPIView.as_view(),
        name='rag-session-retrieve'
    ),
   path(
        '<uuid:id>/update/', RagSessionUpdateAPIView.as_view(),
        name='rag-session-update'
    ),
   path(
        '<uuid:id>/delete/', RagSessionDeleteAPIView.as_view(),
        name='rag-session-delete'
    ),
   path(
        'list/', RagSessionListAPIView.as_view(),
        name='rag-session-list'
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
