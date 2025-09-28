from django.db import models

from core.models import User
from core.model_mixins import UUIDBase
from docmind.utilities import pdf_upload_path

class Session(UUIDBase):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="New Rag Session")
    file = models.FileField(upload_to=pdf_upload_path, null=True, blank=True)
    index_dir = models.CharField(max_length=1024, blank=True)
    embedding_model = models.CharField(
            max_length=200, default="thenlper/gte-small"
        )

    def __str__(self):
        return self.title if self.title else ""


class Message(UUIDBase):

    class ROLECHOICES(models.TextChoices):
        USER = "User", ("User")
        ASSISTANT = "Assistant", ("Assistant")

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=25, choices=ROLECHOICES.choices, default=ROLECHOICES.USER)
    content = models.TextField()
    
    def __str__(self):
        return f"{self.role}: {self.content}"   
    