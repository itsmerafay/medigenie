import os
from twilio.rest import Client
from huggingface_hub import InferenceClient

HF_API_TOKEN = os.environ.get("HF_API_TOKEN")
MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"

client = InferenceClient(token=HF_API_TOKEN)


def query_therapist(prompt: str) -> str:
    """
    Non-streaming call to HuggingFace for tool usage.
    Returns complete response.
    """
    system_prompt = """You are Dr. Emily Hartman, a warm and experienced clinical psychologist. 
    Respond to patients with:

    1. Emotional attunement ("I can sense how difficult this must be...")
    2. Gentle normalization ("Many people feel this way when...")
    3. Practical guidance ("What sometimes helps is...")
    4. Strengths-focused support ("I notice how you're...")

    Key principles:
    - Never use brackets or labels
    - Blend elements seamlessly
    - Vary sentence structure
    - Use natural transitions
    - Mirror the user's language level
    - Provide 2-3 sentences of support
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=messages,
        max_tokens=200,
        temperature=0.6,
        top_p=0.9,
        stream=False
    )
    
    return response.choices[0].message.content.strip()


def call_emergency(username: str):
    """Handle emergency situations"""

    # TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    # TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    # WHATSAPP_FROM = os.getenv("WHATSAPP_FROM")
    # WHATSAPP_TO = os.getenv("WHATSAPP_TO")

    # emergency_message = f"🚨 EMERGENCY ALERT 🚨\n\nUser: {username}\nStatus: In crisis - expressing suicidal thoughts or self-harm intent\nTime: {os.popen('date').read().strip()}\n\nImmediate intervention required. Please contact emergency services."

    # client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    # client.messages.create(
    #     body=emergency_message,
    #     from_=WHATSAPP_FROM,
    #     to=WHATSAPP_TO
    # )
    
    print(f"🚨 EMERGENCY TRIGGERED for {username}")
    pass