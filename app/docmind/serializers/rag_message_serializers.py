from rest_framework import serializers
from rest_framework.exceptions import NotFound

from docmind.models import RagMessage, RagSession
from docmind.utilities import ask_with_rag

class RagMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = RagMessage
        fields = (
            "id", "session", "role", "content" 
        )
        read_only_fields = ("id", )

        
    def create(self, validated_data):
        user = self.context['request'].user
        session = validated_data.get("session")
        content = validated_data.get("content")
        role = RagMessage.ROLECHOICES.USER

        if session:
            try:
                session = RagSession.objects.get(id=session.id, user=user)
            
            except RagMessage.DoesNotExist:
               raise NotFound({
                "session": "No session found for the given id"
            })

        RagMessage.objects.create(
            session=session,
            content=content,
            role=role,
        )

        answer = ask_with_rag(
            index_dir=session.index_dir,
            query=content,
            embedding_model=session.embedding_model
        )

        assistant_message = RagMessage.objects.create(
            session=session,
            content=answer,
            role=RagMessage.ROLECHOICES.ASSISTANT
        )

        return assistant_message
