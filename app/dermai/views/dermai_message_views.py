from django.http import StreamingHttpResponse

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.models import Message
from dermai.serializers import DermMessageSerializer
from dermai.services import GroqService

# class DermMessageCreateAPIView(generics.CreateAPIView):
#     permission_classes = (IsAuthenticated, )
#     serializer_class = DermMessageSerializer
#     queryset = Message.objects.all()


# class DermMessageCreateAPIView(generics.GenericAPIView):
#     permission_classes = (IsAuthenticated, )
#     serializer_class = DermMessageSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         session = serializer.validated_data["session"]
#         content = serializer.validated_data["content"]
#         image = serializer.validated_data["image"]

#         serializer.create_user_message(session, content)

#         groq_service = GroqService()
#         full_response = []

#         def event_stream():
#             for token in groq_service.multimodal_chat(content, image):
#                 full_response.append(token)
#                 yield token
        
#             serializer.create_assistant_message(
#                 session=session,
#                 content="".join(full_response)
#             )
        
#         return StreamingHttpResponse(event_stream(), content_type="text/event-stream")


# class DermMessageCreateAPIView(generics.GenericAPIView):
#     permission_classes = (IsAuthenticated, )
#     serializer_class = DermMessageSerializer
    
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         session = serializer.validated_data["session"]
#         content = serializer.validated_data["content"]
#         image = serializer.validated_data["image"]
        
#         serializer.create_user_message(session, content)
        
#         groq_service = GroqService()
#         full_response = []
        
#         def event_stream():
#             try:
#                 for token in groq_service.multimodal_chat(content, image):
#                     full_response.append(token)
#                     # Format as SSE
#                     yield f"data: {token}\n\n"
                
#                 # Save complete response
#                 serializer.create_assistant_message(
#                     session=session,
#                     content="".join(full_response)
#                 )
                
#                 # Send done signal
#                 yield "data: [DONE]\n\n"
                
#             except Exception as e:
#                 yield f"data: Error: {str(e)}\n\n"
        
#         response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
#         response['Cache-Control'] = 'no-cache'
#         response['X-Accel-Buffering'] = 'no'  # Disable nginx buffering
#         return response


from django.http import StreamingHttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.models import Message
from dermai.serializers import DermMessageSerializer
from dermai.services import GroqService


class DermMessageCreateAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DermMessageSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session = serializer.validated_data["session"]
        content = serializer.validated_data["content"]
        image = serializer.validated_data.get("image")  # ✅ OPTIONAL

        # ✅ STEP 1: Agar image na ho → last image nikaalo
        if image is None:
            last_image_message = (
                Message.objects
                .filter(session=session, image__isnull=False)
                .order_by("-created_at")
                .first()
            )
            if last_image_message:
                image = last_image_message.image   # ✅ reuse image

        # ✅ STEP 2: Save user message (image ho ya na ho)
        serializer.create_user_message(
            session=session,
            content=content,
            image=image
        )

        groq_service = GroqService()
        full_response = []

        history = Message.objects.filter(session=session).order_by("created_at")

        def event_stream():
            try:
                for token in groq_service.multimodal_chat(
                    query=content,
                    image_file=image,     # ✅ always resolved
                    history=history
                ):
                    full_response.append(token)
                    yield f"data: {token}\n\n"

                serializer.create_assistant_message(
                    session=session,
                    content="".join(full_response)
                )

                yield "data: [DONE]\n\n"

            except Exception as e:
                yield f"data: Error: {str(e)}\n\n"

        response = StreamingHttpResponse(
            event_stream(),
            content_type="text/event-stream"
        )
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        return response




