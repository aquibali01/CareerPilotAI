import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_groq_client() -> OpenAI:
    """
    Lazily fetches API key from os.environ or Streamlit Secrets (for Streamlit Cloud)
    and initializes the OpenAI client for Groq.
    """
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        try:
            import streamlit as st
            if "GROQ_API_KEY" in st.secrets:
                api_key = st.secrets["GROQ_API_KEY"]
        except Exception:
            pass

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not set. Please set GROQ_API_KEY in your .env file or Streamlit Cloud Secrets."
        )

    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )


def call_groq(prompt: str) -> str:
    """Calls Groq completion with lazy client initialization."""
    client = get_groq_client()
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content