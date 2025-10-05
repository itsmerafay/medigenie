import os
from django.conf import settings
from django.apps import AppConfig


class DocmindConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'docmind'

    def ready(self):
        from docmind.utilities import load_index_fast
        
        index_dir = os.path.join(settings.MEDIA_ROOT, "default_index")
        if os.path.exists(index_dir):
            load_index_fast("default_index", "sentence-transformers/all-MiniLM-L6-v2")
        else:
            print("⚠️ Skipping FAISS preload — index not found yet")