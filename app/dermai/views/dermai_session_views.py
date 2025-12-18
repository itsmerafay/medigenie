from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.models import Session
from dermai.serializers import DermSessionSerializer

class DermSessionCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = DermSessionSerializer
    queryset = Session.objects.all()


