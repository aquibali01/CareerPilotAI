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


def call_grok_json(prompt: str, retries: int = 2) -> dict:
    """
    Calls Grok with system prompt enforcing JSON output and defensive parsing.
    Automatically retries on JSON parse failure (truncated/malformed output),
    since this happens intermittently with large structured responses.
    """
    last_error = None
    last_raw_content = None

    for attempt in range(retries + 1):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": SYSTEM_JSON_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=6000,  # raised further to reduce truncation odds
            )
            raw_content = response.choices[0].message.content
            return parse_grok_json(raw_content)

        except Exception as e:
            last_error = e
            last_raw_content = locals().get("raw_content")
            print(f"[call_grok_json] Attempt {attempt + 1}/{retries + 1} failed: {e}")
            if last_raw_content:
                print(f"[call_grok_json] Raw model output was: {last_raw_content!r}")
            # loop continues to retry if attempts remain

    # All attempts exhausted — log final failure and return the CV-shaped fallback.
    print(f"[call_grok_json] All {retries + 1} attempts failed. Last error: {last_error}")

    # NOTE: This fallback shape matches the CV-analysis contract
    # (services/resume_parser.py may depend on this exact shape).
    # Business Advisor callers should detect a mismatched shape
    # (missing "ideas" key) and handle it as their own error case
    # rather than passing this through as-is to the UI.
    return {
        "candidate_name": None,
        "education": "Not detected",
        "skills": [],
        "projects": [],
        "experience_years": 0,
        "certifications": []
    }
