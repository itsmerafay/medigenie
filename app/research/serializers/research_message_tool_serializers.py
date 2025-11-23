from rest_framework import serializers

from core.models import Session, Message
from research.services.research_tool_services import ResearchService

from core.serializers import BaseMessageSerializer

class ResearchMessageToolSerializer(BaseMessageSerializer):

    class Meta:
        model = Message
        fields = ("id", "session", "role", "content")
        read_only_fields = ("id", )

    def create(self, validated_data):
        user = self.context['request'].user
        session = validated_data.get("session")
        content = validated_data.get("content")

        if not session or session.user != user:
            raise serializers.ValidationError({"session": "Invalid session."})
        
        Message.objects.create(
            session=session,
            content=content,
            role=Message.ROLECHOICES.USER
        )

        service = ResearchService()
        service.process_user_query(session, content)

        assistant_message = Message.objects.filter(
            session=session,
            role=Message.ROLECHOICES.ASSISTANT
        ).latest("created_at")

        return assistant_message
    
