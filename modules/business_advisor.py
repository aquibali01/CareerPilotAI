"""Business Advisor module for CareerPilot AI.

M4 owns the business-opportunity generation layer.  The module consumes the
shared verified-skill profile plus a user's budget and business interest, asks
the LLM for up to two evidence-grounded opportunities, and validates the
response before returning it to the Streamlit UI.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List

from prompts.prompts import BUSINESS_ADVISOR_PROMPT
from services.grok import call_grok_json


MAX_IDEAS = 2


def _as_string(value: Any, default: str = "") -> str:
    """Return a safe string value for UI/prompt consumption."""
    if value is None:
        return default
    return str(value).strip()


def _normalise_confidence(value: Any) -> str:
    """Normalise confidence labels without inventing evidence."""
    text = _as_string(value).title()
    return text if text in {"High", "Medium", "Low"} else "Unknown"


def _normalise_profile(verified_profile: Any) -> Dict[str, Any]:
    """Convert the shared verification payload into a stable prompt shape.

    The current repository's verifier returns:
        {"verified_skills": [{"skill", "confidence", "evidence"}, ...]}

    The function also tolerates a list of skills as a defensive convenience,
    but it never manufactures confidence/evidence values.
    """
    if isinstance(verified_profile, dict):
        raw_skills = verified_profile.get("verified_skills", [])
        if not isinstance(raw_skills, list):
            raw_skills = []
        profile = {
            "verified_skills": [],
            "profile_status": _as_string(
                verified_profile.get("profile_status"), "available"
            ),
        }
    elif isinstance(verified_profile, list):
        raw_skills = verified_profile
        profile = {"verified_skills": [], "profile_status": "available"}
    else:
        raw_skills = []
        profile = {"verified_skills": [], "profile_status": "unavailable"}

    for item in raw_skills:
        if isinstance(item, str):
            skill = item.strip()
            if skill:
                profile["verified_skills"].append(
                    {"skill": skill, "confidence": "Unknown", "evidence": ""}
                )
            continue

        if not isinstance(item, dict):
            continue

        skill = _as_string(item.get("skill"))
        if not skill:
            continue

        profile["verified_skills"].append(
            {
                "skill": skill,
                "confidence": _normalise_confidence(item.get("confidence")),
                "evidence": _as_string(item.get("evidence")),
            }
        )

    return profile


def _normalise_plan(value: Any) -> List[str]:
    """Return a compact, UI-safe 30-day plan."""
    if isinstance(value, list):
        plan = [_as_string(item) for item in value]
    elif isinstance(value, str):
        plan = [value.strip()] if value.strip() else []
    else:
        plan = []

    return [item for item in plan if item][:4]


def _normalise_idea(raw: Any) -> Dict[str, Any] | None:
    """Validate one business idea while preserving the required schema."""
    if not isinstance(raw, dict):
        return None

    title = _as_string(raw.get("title"), "Untitled Business Idea")
    target_audience = _as_string(raw.get("target_audience"))
    problem = _as_string(raw.get("problem"))
    solution = _as_string(raw.get("solution"))
    revenue_model = _as_string(raw.get("revenue_model"))
    skill_fit = _as_string(raw.get("skill_fit"))
    budget_fit = _as_string(raw.get("budget_fit"))
    first_30_days = _normalise_plan(raw.get("first_30_days"))

    # A card is only useful if its core fields are present.
    required_text = (
        target_audience,
        problem,
        solution,
        revenue_model,
        skill_fit,
        budget_fit,
    )
    if not all(required_text) or len(first_30_days) < 1:
        return None

    return {
        "title": title,
        "target_audience": target_audience,
        "problem": problem,
        "solution": solution,
        "revenue_model": revenue_model,
        "skill_fit": skill_fit,
        "budget_fit": budget_fit,
        "first_30_days": first_30_days,
    }


def validate_business_result(result: Any) -> Dict[str, Any]:
    """Return a stable result shape for Streamlit, even on malformed output."""
    if not isinstance(result, dict):
        return {"ideas": [], "status": "empty"}

    raw_ideas = result.get("ideas", [])
    if not isinstance(raw_ideas, list):
        return {"ideas": [], "status": "empty"}

    ideas: List[Dict[str, Any]] = []
    for raw_idea in raw_ideas[:MAX_IDEAS]:
        idea = _normalise_idea(raw_idea)
        if idea is not None:
            ideas.append(idea)

    return {
        "ideas": ideas,
        "status": "ok" if ideas else "empty",
    }


def build_business_prompt(
    verified_profile: Any,
    budget: Any,
    interest: str,
) -> str:
    """Build the LLM prompt from the shared profile and user inputs."""
    profile = _normalise_profile(verified_profile)
    budget_text = _as_string(budget, "Not specified")
    interest_text = _as_string(interest, "Open to relevant opportunities")

    return BUSINESS_ADVISOR_PROMPT.format(
        verified_profile=json.dumps(profile, ensure_ascii=False),
        budget=budget_text,
        interest=interest_text,
    )


def generate_business_ideas(
    verified_profile: Any,
    budget: Any,
    interest: str,
) -> Dict[str, Any]:
    """Generate up to two evidence-grounded business ideas.

    Parameters
    ----------
    verified_profile:
        The shared M2 verification payload. Expected shape is
        {"verified_skills": [{"skill", "confidence", "evidence"}, ...]}.
    budget:
        User's available starting budget; string or numeric values are fine.
    interest:
        User's business/domain interest.

    Returns
    -------
    dict
        Stable UI contract: {"ideas": [...], "status": "ok"|"empty"}.
    """
    profile = _normalise_profile(verified_profile)

    if not profile["verified_skills"]:
        return {
            "ideas": [],
            "status": "missing_verified_skills",
        }

    prompt = build_business_prompt(profile, budget, interest)

    try:
        raw_result = call_grok_json(prompt)
    except Exception:
        # Keep the UI stable if the service itself raises instead of returning
        # its own fallback payload.
        return {"ideas": [], "status": "service_error"}

    return validate_business_result(raw_result)


def render_business_advisor(st, result: Dict[str, Any]) -> None:
    """Render validated business ideas in Streamlit.

    M5 can call this after obtaining ``result = generate_business_ideas(...)``.
    The function intentionally accepts the Streamlit module/object as an
    argument so the core business logic remains independently testable.
    """
    ideas = result.get("ideas", []) if isinstance(result, dict) else []

    if not ideas:
        status = result.get("status") if isinstance(result, dict) else "empty"
        if status == "missing_verified_skills":
            st.info("Business ideas require verified skills from the shared profile.")
        elif status in {"service_error", "empty"}:
            st.warning("No business idea could be generated from the available evidence.")
        else:
            st.info("No business ideas available.")
        return

    for index, idea in enumerate(ideas, start=1):
        st.subheader(f"Business Opportunity {index}: {idea['title']}")
        st.markdown(f"**Target audience:** {idea['target_audience']}")
        st.markdown(f"**Problem:** {idea['problem']}")
        st.markdown(f"**Solution:** {idea['solution']}")
        st.markdown(f"**Revenue model:** {idea['revenue_model']}")
        st.markdown(f"**Why you fit:** {idea['skill_fit']}")
        st.markdown(f"**Budget fit:** {idea['budget_fit']}")

        st.markdown("**First 30 days:**")
        for phase in idea["first_30_days"]:
            st.write(f"• {phase}")

        if index < len(ideas):
            st.divider()


# Alias for easy integration if the team prefers the PRD terminology.
def get_business_advice(
    verified_profile: Any,
    budget: Any,
    interest: str,
) -> Dict[str, Any]:
    return generate_business_ideas(verified_profile, budget, interest)
