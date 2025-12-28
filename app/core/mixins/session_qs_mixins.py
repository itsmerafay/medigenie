from core.models import Session

class SessionQuerySetMixin:

    def get_object(self):
            user = self.request.user
            session_id = self.kwargs.get("id")
            session = Session.objects.get(user=user, id=session_id)
            return session
    
    def get_queryset(self):
        user = self.request.user
        session_type = (self.kwargs.get("session_type")).upper()
        if session_type in ("RAG", "RESEARCH", "DERMAI", "PSYCHAI"):
            sessions = Session.objects.select_related("user").filter(user=user, session_type=session_type)  
        return sessions