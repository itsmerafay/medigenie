from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.models import Session
from psychai.serializers import TherapistSessionSerializer

class TherapistSessionCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = TherapistSessionSerializer
    queryset = Session.objects.all()


