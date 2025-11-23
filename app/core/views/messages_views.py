from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from core.models import Message, Session
from docmind.serializers import MessageSerializer
from core.pagination import RecordsPagination


class MessageListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    pagination_class = RecordsPagination

    def get_queryset(self):
        user = self.request.user
        session_id = self.kwargs.get("session_id")
        if session_id is None:
            raise ValidationError({
                "session_id": "Session id is missing"
            })

        try:
            session = Session.objects.get(id=session_id, user=user)
        
        except Session.DoesNotExist:
            raise ValidationError({
                "session_id": "No session found for the given id"
            })

        return Message.objects.select_related("session").filter(session=session).order_by("-created_at")    
