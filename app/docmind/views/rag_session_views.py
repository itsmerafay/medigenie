from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from docmind.models import RagSession, RagMessage
from docmind.services import gemini
from docmind.serializers import RagSessionSerializer
from docmind.queryset_mixins import RagSessionQuerySetMixin

class RagSessionCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RagSessionSerializer
    queryset = RagSession.objects.all()
    

class RagSessionRetrieveAPIView(RagSessionQuerySetMixin, generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RagSessionSerializer
    queryset = RagSession.objects.all()


class RagSessionListAPIView(RagSessionQuerySetMixin, generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RagSessionSerializer
    queryset = RagSession.objects.all()
    

class RagSessionUpdateAPIView(RagSessionQuerySetMixin, generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RagSessionSerializer
    queryset = RagSession.objects.all()


class RagSessionDeleteAPIView(RagSessionQuerySetMixin, generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RagSessionSerializer
    queryset = RagSession.objects.all()
