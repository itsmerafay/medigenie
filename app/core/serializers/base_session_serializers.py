# docmind/serializers/base_serializers.py
import os
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from core.models import Session, Message
from docmind.utilities import build_index_from_pdf_remote, unzip_index_if_needed


class BaseSessionSerializer(serializers.ModelSerializer):
    """
    Base serializer for any type of session (RAG, RESEARCH, etc.)
    """

    user = serializers.SerializerMethodField()
    file = serializers.FileField(write_only=True, required=False)
    recent_messages = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = (
            "id", "user", "title", "file", "index_dir",
            "embedding_model", "recent_messages", "session_type",
        )
        read_only_fields = ("id", "user",)

    def get_user(self, obj):
        user = obj.user
        if user:
            return {
                "id": user.id,
                "email": user.email,
                "full_name": getattr(user.userprofile, "name", None),
                "image": user.userprofile.image.url if getattr(user.userprofile, "image", None) else None,
            }

    def get_recent_messages(self, obj):
        user = self.context["request"].user
        recent_messages = Message.objects.filter(session=obj, session__user=user).order_by("-created_at")[:5]
        return [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at,
            }
            for msg in recent_messages
        ]

