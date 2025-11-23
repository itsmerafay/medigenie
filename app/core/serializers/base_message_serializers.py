from django.conf import settings
from rest_framework import serializers

from core.models import Message



class BaseMessageSerializer(serializers.ModelSerializer):
    """
    Base serializer for handling messages (both user & assistant).
    """

    class Meta:
        model = Message
        fields = ("id", "session", "role", "content")
        read_only_fields = ("id",)
