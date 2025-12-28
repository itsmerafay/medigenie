from django.http import StreamingHttpResponse

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.models import Session, Message
from psychai.serializers import TherapistMessageSerializer
from psychai.agents import stream_therapist_response


class TherapistChatCreateAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TherapistMessageSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.user.userprofile.name if request.user.userprofile else request.user.email

        print(f"Username: {username}")

        user_text = serializer.validated_data["content"]
        session_id = request.data.get("session")
        
        if not session_id:
            return Response({"error": "Session ID is required in request body."}, status=400)

        session = Session.objects.get(id=session_id, user=request.user)

        Message.objects.create(
            session=session,
            role=Message.ROLECHOICES.USER,
            content=user_text
        )

        def event_stream():
            ai_full_response = ""

            for chunk in stream_therapist_response(user_text, username=username):
                ai_full_response += chunk
                yield f"data: {chunk}\n\n"
            
            yield "data: [DONE]\n\n"

            Message.objects.create(
                session=session,
                role=Message.ROLECHOICES.ASSISTANT,
                content=ai_full_response
            )

        return StreamingHttpResponse(
            event_stream(),
            content_type="text/event-stream"
        )
    

