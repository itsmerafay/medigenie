from rest_framework import serializers
from core.models import Message, Session
from core.serializers import BaseMessageSerializer
from dermai.services.vision_and_transcription import GroqService


# class DermMessageSerializer(BaseMessageSerializer):
#     """
#     DermAI – Vision + Text medical chat
#     """

#     session = serializers.UUIDField(write_only=True)
#     image = serializers.FileField(write_only=True)

#     class Meta(BaseMessageSerializer.Meta):
#         fields = BaseMessageSerializer.Meta.fields + ("image",)

#     def validate_session(self, value):
#         request = self.context["request"]
#         try:
#             session = Session.objects.get(id=value, user=request.user)
#         except Session.DoesNotExist:
#             raise serializers.ValidationError("Invalid session")
#         return session

#     def create(self, validated_data):
#         session = validated_data.pop("session")
#         image = validated_data.pop("image")
#         content = validated_data.get("content")

#         Message.objects.create(
#             session=session,
#             role=Message.ROLECHOICES.USER,
#             content=content,
#         )

#         groq_service = GroqService()
#         assistant_response = groq_service.multimodal_chat(
#             query=content,
#             image_file=image,
#         )

#         assistant_message = Message.objects.create(
#             session=session,
#             role=Message.ROLECHOICES.ASSISTANT,
#             content=assistant_response,
#         )

#         return assistant_message


class DermMessageSerializer(BaseMessageSerializer):
    session = serializers.UUIDField(write_only=True)
    image = serializers.FileField(write_only=True)

    class Meta(BaseMessageSerializer.Meta):
        fields = BaseMessageSerializer.Meta.fields + ("image",)

    def validate_session(self, value):
        request = self.context["request"]
        try:
            return Session.objects.get(id=value, user=request.user)
        except Session.DoesNotExist:
            raise serializers.ValidationError("Invalid session")

    def create_user_message(self, session, content):
        return Message.objects.create(
            session=session,
            role=Message.ROLECHOICES.USER,
            content=content,
        )

    def create_assistant_message(self, session, content):
        return Message.objects.create(
            session=session,
            role=Message.ROLECHOICES.ASSISTANT,
            content=content,
        )

