"""
Career Advisor Module (PRD Section 3.2 / Step 3)

Pipeline:
    verified_skills (from Member 2's GitHub verification step)
        -> compute_career_matches()   [deterministic, no LLM]
        -> get_match_explanation()    [Grok, prose]
        -> get_skill_gap()            [deterministic, no LLM]
        -> get_roadmap()              [Grok, prose]

Input shape expected for `verified_skills` (comes from the shared pipeline):
{
    "Python": "High",
    "Java": "High",
    "SQL": "Medium",
    "AI": "Low"
}
"""

import json
import os
from services.groq import call_groq as call_grok

CONFIDENCE_WEIGHTS = {"High": 1.0, "Medium": 0.6, "Low": 0.3}

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "career_requirements.json")


def load_career_requirements() -> dict:
    with open(DATA_PATH, "r") as f:
        return json.load(f)


# ---------------------------------------------------------------------
# Step 11 — Deterministic scoring logic (NOT sent to Grok, kept reliable)
# ---------------------------------------------------------------------
def compute_career_matches(verified_skills: dict) -> list:
    """
    Returns a ranked list of career matches:
    [
        {
            "role": "Software Developer",
            "match_percent": 72,
            "matched_skills": ["Python", "Java", "Git"],
            "missing_skills": ["SQL", "OOP", "APIs"]
        },
        ...
    ]
    """
    careers = load_career_requirements()
    results = []

    for role, info in careers.items():
        required = info["required_skills"]
        total_weight = 0.0
        matched_skills = []
        missing_skills = []

        for skill in required:
            confidence = verified_skills.get(skill)
            weight = CONFIDENCE_WEIGHTS.get(confidence, 0.0)
            total_weight += weight
            if weight > 0:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

        match_percent = round((total_weight / len(required)) * 100) if required else 0

        results.append({
            "role": role,
            "match_percent": match_percent,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
        })

    # highest match first
    results.sort(key=lambda x: x["match_percent"], reverse=True)
    return results


# ---------------------------------------------------------------------
# Step 12 — Grok generates ONLY the natural-language explanation
# ---------------------------------------------------------------------
def get_match_explanation(role: str, match_percent: int, matched_skills: list, missing_skills: list) -> str:
    prompt = f"""In 1-2 short sentences, explain why this candidate is a {match_percent}% match
for the role of {role}. Be encouraging and specific.

Skills they have that are relevant: {", ".join(matched_skills) if matched_skills else "none yet"}
Skills they are missing: {", ".join(missing_skills) if missing_skills else "none"}

Write only the explanation text, no preamble, no headers."""

    try:
        return call_grok(prompt).strip()
    except Exception:
        return f"Your current skillset gives you a {match_percent}% match for {role}."


# ---------------------------------------------------------------------
# Step 13a — Skill gap comparison (deterministic, reuses matched/missing)
# ---------------------------------------------------------------------
def get_skill_gap(target_role: str, verified_skills: dict) -> dict:
    careers = load_career_requirements()
    if target_role not in careers:
        raise ValueError(f"Unknown role: {target_role}")

    required = careers[target_role]["required_skills"]
    gap = {"have": [], "partial": [], "missing": []}

    for skill in required:
        confidence = verified_skills.get(skill)
        if confidence == "High":
            gap["have"].append(skill)
        elif confidence in ("Medium", "Low"):
            gap["partial"].append(skill)
        else:
            gap["missing"].append(skill)

    return gap


# ---------------------------------------------------------------------
# Step 13b — Roadmap generation (Grok, prose is fine, no JSON needed)
# ---------------------------------------------------------------------
def get_roadmap(target_role: str, skill_gap: dict) -> str:
    prompt = f"""Create a 4-month, month-by-month learning roadmap for someone
aiming to become a {target_role}.

Skills they already have (High confidence): {", ".join(skill_gap["have"]) or "none"}
Skills they partially have: {", ".join(skill_gap["partial"]) or "none"}
Skills they are missing: {", ".join(skill_gap["missing"]) or "none"}

Format as:
Month 1: ...
Month 2: ...
Month 3: ...
Month 4: ...

Keep each month to 2-3 short bullet points. No extra commentary before or after."""

    try:
        return call_grok(prompt).strip()
    except Exception:
        return "Roadmap generation is temporarily unavailable. Please try again."


# ---------------------------------------------------------------------
# Quick manual test — run this file directly to sanity-check the pipeline
# ---------------------------------------------------------------------
if __name__ == "__main__":
    sample_verified_skills = {
        "Python": "High",
        "Java": "High",
        "Git": "High",
        "SQL": "Medium",
        "AI": "Low",
        "Machine Learning": "Low",
    }

    matches = compute_career_matches(sample_verified_skills)
    print("=== Career Matches ===")
    for m in matches:
        print(f"{m['role']}: {m['match_percent']}% match")

    top = matches[0]
    print("\n=== Explanation for top match (requires GROK_API_KEY) ===")
    try:
        explanation = get_match_explanation(
            top["role"], top["match_percent"], top["matched_skills"], top["missing_skills"]
        )
        print(explanation)
    except Exception as e:
        print(f"(Skipped Grok call in test: {e})")

    print("\n=== Skill Gap for top match ===")
    gap = get_skill_gap(top["role"], sample_verified_skills)
    print(gap)
