from operator import index
from django.http import StreamingHttpResponse

from docmind.utilities.process_and_query_rag import ask_with_rag
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from core.models import Message, Session
from docmind.serializers import MessageSerializer

class RagMessageCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        session_id = request.data.get("session")
        content = request.data.get("content")
        role = Message.ROLECHOICES.USER

        if not session_id or not content:
            return StreamingHttpResponse({
                "field": "session or content is missing"
            })
    

        try:
            session = Session.objects.get(id=session_id, user=user)
        
        except Session.DoesNotExist:
            return StreamingHttpResponse({
                "session": "No session found for the given id"
            })
        
        Message.objects.create(
            session=session,
            content=content,
            role=role,
        )

        def event_stream():
            answer_text = ""
            for chunk in ask_with_rag(index_dir=session.index_dir, query=content, embedding_model=session.embedding_model):
                answer_text += chunk
                yield f"data: {chunk}\n\n"


            Message.objects.create(
                session=session,
                content=answer_text,
                role=Message.ROLECHOICES.ASSISTANT
            )

        return StreamingHttpResponse(event_stream(), content_type="text/event-stream")


