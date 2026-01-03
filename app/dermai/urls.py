from django.urls import path, include
from dermai import views



DERM_SESSION_URL_PATTERNS = [    
   path(
        'create/', views.DermSessionCreateAPIView.as_view(),
        name='derm-session-create'
    ),

]



DERM_MESSAGE_URL_PATTERNS = [    
   path(
        'create/', views.DermMessageCreateAPIView.as_view(),
        name='derm-message-create'
    ),
   path(
        'createssss/testtttttt', views.DermMessageCreateAPIView.as_view(),
        name='derm-message-create'
    ),
]



urlpatterns = [
    path('derm/session/', include(DERM_SESSION_URL_PATTERNS)),
    path('derm/message/', include(DERM_MESSAGE_URL_PATTERNS)),
]
