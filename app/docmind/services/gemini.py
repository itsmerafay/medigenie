import os

from sympy import false
import google.generativeai as genai

client = genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def gemini_llm_response(prompt: str):
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
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



# import os
# import requests

# client = os.getenv("OPENROUTER_API_KEY")

# def gemini_llm_response(prompt: str) -> str:
#     api_url = "https://openrouter.ai/api/v1/chat/completions"
#     headers = {
#         "Authorization": f"Bearer {client}",
#         "Content-Type": "application/json",
#     }
#     payload = {
#         "model": "qwen/qwen3-coder:free",
#         "messages": [
#             {"role": "system", "content": "You are a helpful coding assistant."},
#             {"role": "user", "content": prompt},
#         ],
#     }

#     response = requests.post(api_url, headers=headers, json=payload)
#     response_json = response.json()
#     text = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
#     return text
