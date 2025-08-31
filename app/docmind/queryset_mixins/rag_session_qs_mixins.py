from docmind.models import RagSession

class RagSessionQuerySetMixin:

    def get_object(self):
            user = self.request.user
            rag_session_id = self.kwargs.get("id")
            rag_session = RagSession.objects.get(user=user, id=rag_session_id)
            return rag_session
    
    def get_queryset(self):
        user = self.request.user
        rag_sessions = RagSession.objects.select_related("user").filter(user=user)  
        return rag_sessions