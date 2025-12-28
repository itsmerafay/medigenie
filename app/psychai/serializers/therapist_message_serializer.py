from rest_framework import serializers
from core.serializers import BaseMessageSerializer  

class TherapistMessageSerializer(BaseMessageSerializer):
    """
    Serializer for creating messages in Therapist Chat.
    Inherits base Message fields and only requires 'content' from user input.
    """

    class Meta(BaseMessageSerializer.Meta):
        fields = BaseMessageSerializer.Meta.fields
        read_only_fields = ("id", "role", "session")  
