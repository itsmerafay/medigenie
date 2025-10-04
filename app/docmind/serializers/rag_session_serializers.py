from rest_framework import serializers

from core.models import Message, Session
from docmind.utilities import build_index_from_pdf

class SessionSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    file = serializers.FileField(write_only=True)
    recent_messages = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = (
            "id", "user", "title", "file", "index_dir",
            "embedding_model", "recent_messages", 
            "session_type", 
        )
        read_only_fields = ("id", "user", )

    def get_recent_messages(self, obj):
        user = self.context["request"].user
        recent_messages = Message.objects.filter(session=obj, session__user=user).order_by("-created_at")[:5]
        return [
            {
                "id": message.id,
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at
            }

            for message in recent_messages
        ]


    def get_user(self, obj):
        user = obj.user
        if user:
            return {
                "id": user.id,
                "email": user.email,
                "full_name": user.userprofile.name if user.userprofile.name else None,
                "image": user.userprofile.image.url if user.userprofile.image else None
            }
        
    def create(self, validated_data):
        user = self.context['request'].user
        title = validated_data.get("title") or "New Rag Session"
        session_type = Session.SessionType.RAG
        file = validated_data.get("file")
        

        if not file:
            raise serializers.ValidationError({
                "file": "You must provide a file to create a rag session"
            })
    
        session = Session.objects.create(
            user=user,
            title=title,
            session_type=session_type,
        )

        session.file.save(file.name, file, save=True)

        idx_dir = f"indexes/{user.id}/{session.id}"
        build_index_from_pdf(session.file.path, idx_dir, session.embedding_model)

        session.index_dir = idx_dir
        session.save()            
        
        return session
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        instance.title = validated_data.get("title", instance.title)
        if instance.user != user:
            raise serializers.ValidationError({
                "user":"You cannot change the user of a rag session"
            })
        
        if instance.file != validated_data.get("file", instance.file):
            raise serializers.ValidationError({
                "file":"You cannot change the file of a rag session. Instead create a new session"
            })

        instance.save()

        return instance