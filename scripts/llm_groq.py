import os
os.environ.pop("SSL_CERT_FILE", None)

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

def chat_with_groq(messages, model="llama3-70b-8192"):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 500
    }

    response = httpx.post(GROQ_BASE_URL, headers=headers, json=payload)

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        print("Error:", e.response.text)
        raise

    return response.json()["choices"][0]["message"]["content"]
