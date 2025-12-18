"""
Hnadles Vision + Text Chat 
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

    def encode_image(self, image_file):
        """Convert image file to base64"""
        return base64.b64encode(image_file.read()).decode("utf-8")
    

    def multimodal_chat(self, query, image_file):
        """Send text + image to groq multimodal model and return response"""

        encoded_image = self.encode_image(image_file)
        
        messages = [
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text", 
                        "text": query
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}
                    }
                ]
            }
        ]

        response = self.client.chat.completions.create(
            messages=messages,
            model="meta-llama/llama-4-maverick-17b-128e-instruct",
            stream=True
        )

        # return response.choices[0].message.content
        
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta and getattr(delta, "content", None):
                yield delta.content 
            


