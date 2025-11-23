from rest_framework import serializers
from rest_framework.exceptions import NotFound

from core.models import Message, Session
from docmind.utilities import ask_with_rag


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ("id", "session", "role", "content")
        read_only_fields = ("id", )

    def create(self, validated_data):
        user = self.context['request'].user
        session = validated_data.get("session")
        content = validated_data.get("content")
        role = Message.ROLECHOICES.USER

        # ✅ Check if session belongs to user
        if session:
            try:
                session = Session.objects.get(id=session.id, user=user)
            except Session.DoesNotExist:
                raise NotFound({"session": "No session found for the given id"})

        # ✅ Store the user message first
        Message.objects.create(
            session=session,
            content=content,
            role=role,
        )

        # ✅ Collect streamed answer in chunks (safe memory usage)
        final_answer = ""
        for chunk in ask_with_rag(
            index_dir=session.index_dir,
            query=content,
            embedding_model=session.embedding_model
        ):
            final_answer += chunk


        # ✅ Store assistant response
        assistant_message = Message.objects.create(
            session=session,
            content=final_answer,
            role=Message.ROLECHOICES.ASSISTANT
        )

        return assistant_message


