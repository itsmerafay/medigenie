from docmind.models import Session

class RagSessionQuerySetMixin:

    def get_object(self):
            user = self.request.user
            rag_session_id = self.kwargs.get("id")
            rag_session = Session.objects.get(user=user, id=rag_session_id)
            return rag_session
    
    def get_queryset(self):
        user = self.request.user
        rag_sessions = Session.objects.select_related("user").filter(user=user)  
        return rag_sessions