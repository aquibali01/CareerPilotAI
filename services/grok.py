import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI
from prompts.prompts import SYSTEM_JSON_PROMPT

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def parse_grok_json(raw_text: str) -> dict:
    """Strips markdown code blocks if present and parses JSON cleanly."""
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_text.strip(), flags=re.MULTILINE)
    return json.loads(cleaned)

def call_grok_json(prompt: str) -> dict:
    """
    Calls Grok with system prompt enforcing JSON output and defensive parsing with fallback.
    """
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": SYSTEM_JSON_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        raw_content = response.choices[0].message.content
        return parse_grok_json(raw_content)
    except Exception as e:
        print(f"Error or JSON parse failure: {e}")
        # Same-shape fallback per PRD 4.4d
        return {
            "candidate_name": None,
            "education": "Not detected",
            "skills": [],
            "projects": [],
            "experience_years": 0,
            "certifications": []
        }