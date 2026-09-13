"""
Skill Verification Pipeline — orchestrates pieces that already exist,
built by Aquib (Member 2):

    prompts/prompts.py    -> CV_ANALYSIS_PROMPT, SKILL_VERIFICATION_PROMPT
    services/grok.py      -> call_grok_json(prompt)
    services/github.py    -> fetch_github_user_data(username)
    services/resume_parser.py -> extract_text_from_pdf(pdf_file)

This file does NOT invent new prompts — it follows the exact same
pattern already demonstrated in test_cv.py and test_github.py, just
chained together into one pipeline that app.py can call.
"""

import json

from prompts.prompts import CV_ANALYSIS_PROMPT, SKILL_VERIFICATION_PROMPT
from services.grok import call_grok_json


def extract_cv_skills(cv_text: str) -> dict:
    """
    Step 1 (matches test_cv.py): send CV text through Aquib's
    CV_ANALYSIS_PROMPT to get structured candidate data.
    """
    if not cv_text or not cv_text.strip():
        return {
            "candidate_name": None,
            "education": "Not detected",
            "skills": [],
            "projects": [],
            "experience_years": 0,
            "certifications": [],
        }

    prompt = CV_ANALYSIS_PROMPT.format(cv_text=cv_text[:6000])  # cap length for safety
    return call_grok_json(prompt)


def build_verified_skill_profile(cv_profile: dict, github_data: dict) -> dict:
    """
    Step 2 (matches test_github.py): send CV-claimed skills + GitHub data
    through Aquib's SKILL_VERIFICATION_PROMPT to get confidence ratings.
    """
    claimed_skills = cv_profile.get("skills", [])

    if not claimed_skills:
        return {"verified_skills": []}

    prompt = SKILL_VERIFICATION_PROMPT.format(
        cv_skills=json.dumps(claimed_skills),
        github_data=json.dumps(github_data),
    )
    return call_grok_json(prompt)


def flatten_verified_skills(verified_profile: dict) -> dict:
    """
    Converts {"verified_skills": [{"skill","confidence","evidence"}, ...]}
    into the flat {skill: confidence} shape career_advisor.py expects.
    """
    flat = {}
    for item in verified_profile.get("verified_skills", []):
        skill = item.get("skill")
        confidence = item.get("confidence")
        if skill and confidence:
            flat[skill] = confidence
    return flat


def run_full_verification_pipeline(cv_text: str, github_username: str, github_data: dict) -> dict:
    """
    Convenience wrapper: CV text + GitHub data in, everything the UI
    needs out. This is the single function app.py calls.
    """
    cv_profile = extract_cv_skills(cv_text)
    verified_profile = build_verified_skill_profile(cv_profile, github_data)
    flat_skills = flatten_verified_skills(verified_profile)

    return {
        "cv_profile": cv_profile,
        "verified_profile": verified_profile,  # shape business_advisor.py expects
        "flat_skills": flat_skills,             # shape career_advisor.py expects
    }
