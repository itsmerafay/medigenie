import os
import requests
import json


import google.generativeai as genai


client = genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def gemini_llm_response(prompt: str):
    model = genai.GenerativeModel(model_name="gemini-2.5-flash")
    response = model.generate_content(prompt, stream=True)
    for chunk in response:
        if not chunk.candidates:
            continue

        candidate = chunk.candidates[0]
        if not candidate.content.parts:
            continue

        part = candidate.content.parts[0]
        if hasattr(part, "text") and part.text:
            yield part.text  



# using mistral model 
# mistralai/devstral-2512:free
# 123B parameters


import os
import requests
import json
import time

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"


def mistral_llm_response(prompt: str):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
    }

    payload = {
        "model": "mistralai/devstral-2512:free",
        "messages": [
            {"role": "system", "content": "You are an expert medical assistant."},
            {"role": "user", "content": prompt},
        ],
        "stream": True
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        stream=True,
        timeout=60
    )

    if response.status_code == 429:
        raise RuntimeError("Mistral rate limit exceeded")

    for line in response.iter_lines(decode_unicode=True):
        if not line:
            continue

        if line.strip() == "data: [DONE]":
            break

        if not line.startswith("data:"):
            continue

        try:
            data = json.loads(line.replace("data:", "").strip())
            delta = data["choices"][0]["delta"]

            if "content" in delta:
                yield delta["content"]

        except Exception:
            continue


def stream_llm_response(prompt: str):
    try:
        yielded = False
        for chunk in mistral_llm_response(prompt):
            yielded = True
            yield chunk 

        if yielded:
            return 
        else:
            raise RuntimeError("Mistral rate limit exceeded")

    except Exception:
        pass

    try:
        yielded = False
        for chunk in gemini_llm_response(prompt):
            yielded = True
            yield chunk

        if yielded:
            return
        
        else:
            raise RuntimeError("Gemini rate limit exceeded")

    except Exception:
        pass

    yield "\n⚠️ High load right now. Please try again in a few moments.\n"


