
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from core.models import Session, Message
from docmind.services import gemini
from docmind.serializers import SessionSerializer
from core.mixins import SessionQuerySetMixin
from core.pagination import RecordsPagination

from core.mixins import SessionQuerySetMixin

class SessionRetrieveAPIView(SessionQuerySetMixin, generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SessionSerializer
    queryset = Session.objects.all()


class SessionListAPIView(SessionQuerySetMixin, generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SessionSerializer
    queryset = Session.objects.all()
    pagination_class = RecordsPagination
    

class SessionUpdateAPIView(SessionQuerySetMixin, generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SessionSerializer
    queryset = Session.objects.all()


class SessionDeleteAPIView(SessionQuerySetMixin, generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SessionSerializer
    queryset = Session.objects.all()
