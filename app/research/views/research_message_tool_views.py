from django.http import StreamingHttpResponse

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from research.serializers import ResearchMessageToolSerializer
from core.models import Message, Session
from research.services import ResearchService


from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from asgiref.sync import sync_to_async
import asyncio


class ResearchMessageCreateAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def post(self, request):
        user = request.user
        session_id = request.data.get("session")
        content = request.data.get("content")
        
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return Response({"error": "Invalid session."}, status=400)
        
        if session.user != user:
            return Response({"error": "Invalid session."}, status=400)
        
        Message.objects.create(
            session=session,
            content=content,
            role=Message.ROLECHOICES.USER
        )
        
        service = ResearchService()
        
        def stream():
            full_text = ""
            
            try:
                # Create new event loop for this request
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                async def async_stream():
                    nonlocal full_text
                    
                    graph = service._build_graph()
                    
                    # Use astream_events for token-level streaming
                    async for event in graph.astream_events(
                        {"messages": [{"role": "user", "content": content}]},
                        version="v2"
                    ):
                        kind = event.get("event")
                        
                        # Token-by-token streaming from LLM
                        if kind == "on_chat_model_stream":
                            chunk = event.get("data", {}).get("chunk")
                            if chunk and hasattr(chunk, "content") and chunk.content:
                                token = chunk.content
                                full_text += token
                                yield f"data: {token}\n\n"
                        
                        # Tool execution status
                        elif kind == "on_tool_start":
                            tool_name = event.get("name", "unknown")
                            yield f"data: [Using {tool_name}...]\n\n"
                    
                    # Save final message using sync_to_async
                    if full_text.strip():
                        await sync_to_async(Message.objects.create)(
                            session=session,
                            content=full_text.strip(),
                            role=Message.ROLECHOICES.ASSISTANT,
                        )
                    
                    yield "data: [DONE]\n\n"
                
                # Run the async generator
                async_gen = async_stream()
                
                try:
                    while True:
                        try:
                            chunk = loop.run_until_complete(async_gen.__anext__())
                            yield chunk
                        except StopAsyncIteration:
                            break
                finally:
                    loop.close()
                    
            except Exception as e:
                import traceback
                error_detail = traceback.format_exc()
                print(f"Streaming error: {error_detail}")
                yield f"data: ERROR: {str(e)}\n\n"
        
        return StreamingHttpResponse(stream(), content_type="text/event-stream")



class ResearchMessageListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ResearchMessageToolSerializer
    queryset = Message.objects.all()

    


