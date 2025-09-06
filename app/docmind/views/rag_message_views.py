from operator import index
from django.http import StreamingHttpResponse

from docmind.utilities.process_and_query_rag import ask_with_rag
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from docmind.models import RagMessage, RagSession
from docmind.serializers import RagMessageSerializer

# class RagMessageCreateAPIView(generics.CreateAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = RagMessageSerializer
#     queryset = RagMessage.objects.all()


class RagMessageCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        session_id = request.data.get("session")
        content = request.data.get("content")
        role = RagMessage.ROLECHOICES.USER

        if not session_id or not content:
            return StreamingHttpResponse({
                "field": "session or content is missing"
            })
    

        try:
            session = RagSession.objects.get(id=session_id, user=user)
        
        except RagSession.DoesNotExist:
            return StreamingHttpResponse({
                "session": "No session found for the given id"
            })
        
        RagMessage.objects.create(
            session=session,
            content=content,
            role=role,
        )

        def event_stream():
            answer_text = ""
            for chunk in ask_with_rag(index_dir=session.index_dir, query=content, embedding_model=session.embedding_model):
                answer_text += chunk
                yield f"data: {chunk}\n\n"


            RagMessage.objects.create(
                session=session,
                content=answer_text,
                role=RagMessage.ROLECHOICES.ASSISTANT
            )

        return StreamingHttpResponse(event_stream(), content_type="text/event-stream")


class RagMessageListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RagMessageSerializer
    queryset = RagMessage.objects.all()

    def get_queryset(self):
        user = self.request.user
        session_id = self.kwargs.get("session_id")
        if session_id is None:
            raise ValidationError({
                "session_id": "Session id is missing"
            })

        try:
            session = RagSession.objects.get(id=session_id, user=user)
        
        except RagSession.DoesNotExist:
            raise ValidationError({
                "session_id": "No session found for the given id"
            })

        return RagMessage.objects.select_related("session").filter(session=session)

