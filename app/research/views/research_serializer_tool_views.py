from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from research.serializers import ResearchSessionToolSerializer
from core.models import Session


class ResearchSessionCreateAPIView(generics.CreateAPIView):
    serializer_class = ResearchSessionToolSerializer
    permission_classes = [IsAuthenticated]
    queryset = Session.objects.all()