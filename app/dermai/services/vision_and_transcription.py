# """
# Hnadles Vision + Text Chat 
# """


# import base64
# from groq import Groq
# from django.conf import settings

# class GroqService:

#     MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"

#     SYSTEM_PROMPT = """        
#             You have to act as a professional doctor, i know you are not but this is for learning purpose. 
#             What's in this image?. Do you find anything wrong with it medically? 
#             If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
#             your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
#             Donot say 'In the image I see' but say 'With what I see, I think you have ....'
#             Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
#             Keep your answer concise (max 10 sentences). No preamble, start your answer right away please
#             """

#     def __init__(self):
#         self.client = Groq(api_key=settings.GROQ_API_KEY)

#     def encode_image(self, image_file):
#         """
#         Safe for:
#         - Uploaded files
#         - Stored FieldFile
#         - Missing files (gracefully handled)
#         """
#         try:
#             if hasattr(image_file, "path"):
#                 # FieldFile (stored image)
#                 with open(image_file.path, "rb") as f:
#                     data = f.read()
#             else:
#                 # Uploaded file
#                 data = image_file.read()

#             return base64.b64encode(data).decode("utf-8")

#         except Exception:
#             # ❌ file missing or unreadable
#             return None




#     def multimodal_chat(self, query, image_file=None, history=None):
#         messages = []

#         # ✅ include history
#         if history:
#             for msg in history:
#                 messages.append({
#                     "role": msg.role,
#                     "content": msg.content
#                 })

#         # ✅ text-only case
#         if image_file is None:
#             messages.append({
#                 "role": "user",
#                 "content": query
#             })
#         else:
#             encoded_image = self.encode_image(image_file)
#             messages.append({
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": query},
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             "url": f"data:image/jpeg;base64,{encoded_image}"
#                         }
#                     }
#                 ]
#             })

#         response = self.client.chat.completions.create(
#             messages=messages,
#             model="meta-llama/llama-4-maverick-17b-128e-instruct",
#             stream=True
#         )

#         # return response.choices[0].message.content
        
#         for chunk in response:
#             delta = chunk.choices[0].delta
#             if delta and getattr(delta, "content", None):
#                 yield delta.content 
            


"""
Handles Vision + Text Chat (Groq)
Production-safe version
"""

import base64
from groq import Groq
from django.conf import settings


class GroqService:
    MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"

    SYSTEM_PROMPT = """        
    You have to act as a professional doctor, i know you are not but this is for learning purpose. 
    What's in this image?. Do you find anything wrong with it medically? 
    If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
    your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
    Donot say 'In the image I see' but say 'With what I see, I think you have ....'
    Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
    Keep your answer concise (max 10 sentences). No preamble, start your answer right away please
    """

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    # ------------------------------------------------------------------
    # IMAGE HANDLING (SAFE)
    # ------------------------------------------------------------------
    def encode_image(self, image_file):
        """
        Supports:
        - InMemoryUploadedFile (new upload)
        - FieldFile (stored image)
        - Missing / broken files (returns None safely)
        """
        try:
            # Stored image (FieldFile)
            if hasattr(image_file, "path"):
                with open(image_file.path, "rb") as f:
                    data = f.read()

            # Newly uploaded image
            else:
                data = image_file.read()

            return base64.b64encode(data).decode("utf-8")

        except Exception:
            # File missing / unreadable
            return None

    # ------------------------------------------------------------------
    # MULTIMODAL CHAT (STREAMING)
    # ------------------------------------------------------------------
    def multimodal_chat(self, query, image_file=None, history=None):
        messages = []

        # ✅ system prompt
        messages.append({
            "role": "system",
            "content": self.SYSTEM_PROMPT.strip()
        })


        ROLE_MAP = {
            "USER": "user",
            "ASSISTANT": "assistant",
            "SYSTEM": "system"
        }

        for msg in history:
            role = ROLE_MAP.get(msg.role)
            if not role:
                continue

            messages.append({
                "role": role,
                "content": msg.content
            })


        # ✅ encode image (if exists)
        encoded_image = None
        if image_file:
            encoded_image = self.encode_image(image_file)

        # ✅ user message
        if encoded_image:
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    }
                ]
            })
        else:
            # fallback to text-only
            messages.append({
                "role": "user",
                "content": query
            })

        # ✅ single streaming call (IMPORTANT)
        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=messages,
            stream=True
        )

        for chunk in response:
            delta = chunk.choices[0].delta
            if delta and getattr(delta, "content", None):
                yield delta.content
