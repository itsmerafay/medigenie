from rest_framework import serializers
from rest_framework.exceptions import NotFound

from core.models import Message, Session
from docmind.utilities import ask_with_rag

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            "id", "session", "role", "content" 
        )
        read_only_fields = ("id", )

        
    def create(self, validated_data):
        user = self.context['request'].user
        session = validated_data.get("session")
        content = validated_data.get("content")
        session_type = validated_data.get("session_type")
        role = Message.ROLECHOICES.USER

        if session:
            try:
                session = Message.objects.get(id=session.id, user=user)
            
            except Message.DoesNotExist:
               raise NotFound({
                "session": "No session found for the given id"
            })

        Message.objects.create(
            session=session,
            content=content,
            role=role,
        )

        answer = ask_with_rag(
            index_dir=session.index_dir,
            query=content,
            embedding_model=session.embedding_model
        )

        assistant_message = Message.objects.create(
            session=session,
            content=answer,
            role=Message.ROLECHOICES.ASSISTANT
        )

        return assistant_message
