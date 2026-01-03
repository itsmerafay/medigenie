from operator import index
from django.http import StreamingHttpResponse

from docmind.utilities.process_and_query_rag import ask_with_rag
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from core.models import Message, Session
from docmind.serializers import MessageSerializer


from django.http import StreamingHttpResponse
from docmind.utilities.process_and_query_rag import ask_with_rag
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.models import Message, Session

class RagMessageCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        session_id = request.data.get("session")
        content = request.data.get("content")
        role = Message.ROLECHOICES.USER

        if not session_id or not content:
            return StreamingHttpResponse(
                "data: {\"error\": \"session or content is missing\"}\n\n",
                content_type="text/event-stream"
            )
    
        try:
            session = Session.objects.get(id=session_id, user=user)
        except Session.DoesNotExist:
            return StreamingHttpResponse(
                "data: {\"error\": \"No session found for the given id\"}\n\n",
                content_type="text/event-stream"
            )
        
        Message.objects.create(
            session=session,
            content=content,
            role=role,
        )

        def event_stream():
            from research.utils import clean_markdown
            answer_text = ""
            
            for chunk in ask_with_rag(
                index_dir=session.index_dir, 
                query=content, 
                embedding_model=session.embedding_model
            ):
                answer_text += chunk
                # Stream the original chunk (with formatting) to frontend
                yield f"data: {chunk}\n\n"

            # Clean markdown before saving to database
            cleaned_answer = clean_markdown(answer_text)
            Message.objects.create(
                session=session,
                content=cleaned_answer,
                role=Message.ROLECHOICES.ASSISTANT
            )

        return StreamingHttpResponse(event_stream(), content_type="text/event-stream")


