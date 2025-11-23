from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from core.models import Session
from docmind.serializers import SessionSerializer

class RagSessionCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SessionSerializer
    queryset = Session.objects.all()
    
