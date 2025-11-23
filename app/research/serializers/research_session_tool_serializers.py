from rest_framework import serializers

from core.models import Session, Message
from research.services.research_tool_services import ResearchService

from core.serializers import BaseSessionSerializer, BaseMessageSerializer

class ResearchSessionToolSerializer(BaseSessionSerializer):

    session_type = Session.SessionType.RESEARCH

    def create(self, validated_data):
        user = self.context['request'].user
        title = validated_data.get("title")

        session = Session.objects.create(
            user=user,
            title=title,
            session_type=self.session_type,
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        )
        return session
    
