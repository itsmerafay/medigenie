from core.models import Session

from core.serializers import BaseSessionSerializer

class DermSessionSerializer(BaseSessionSerializer):

    session_type = Session.SessionType.DERMAI

    def create(self, validated_data):
        user = self.context['request'].user
        title = validated_data.get("title")

        session = Session.objects.create(
            user=user,
            title=title,
            session_type=self.session_type,
            embedding_model="",
        )
        return session
    