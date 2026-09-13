import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI
from prompts.prompts import SYSTEM_JSON_PROMPT

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


def parse_grok_json(raw_text: str) -> dict:
    """Strips markdown code blocks if present and parses JSON cleanly."""
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_text.strip(), flags=re.MULTILINE)
    return json.loads(cleaned)


def call_grok_json(prompt: str, retries: int = 2) -> dict:
    """
    Calls Grok with system prompt enforcing JSON output and defensive parsing.
    Automatically retries on JSON parse failure (truncated/malformed output).
    """
    last_error = None
    last_raw_content = None

    try:
        client = get_groq_client()
    except Exception as e:
        print(f"[call_grok_json] Client init failed: {e}")
        return {
            "candidate_name": None,
            "education": "Not detected",
            "skills": [],
            "projects": [],
            "experience_years": 0,
            "certifications": []
        }

    for attempt in range(retries + 1):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": SYSTEM_JSON_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=6000,
            )
            raw_content = response.choices[0].message.content
            return parse_grok_json(raw_content)

        except Exception as e:
            last_error = e
            last_raw_content = locals().get("raw_content")
            print(f"[call_grok_json] Attempt {attempt + 1}/{retries + 1} failed: {e}")
            if last_raw_content:
                print(f"[call_grok_json] Raw model output was: {last_raw_content!r}")

    print(f"[call_grok_json] All {retries + 1} attempts failed. Last error: {last_error}")

    return {
        "candidate_name": None,
        "education": "Not detected",
        "skills": [],
        "projects": [],
        "experience_years": 0,
        "certifications": []
    }
