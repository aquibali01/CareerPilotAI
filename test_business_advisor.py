"""Local test harness for M4 Business Advisor.

Run from the repository root:
    python test_business_advisor.py

By default this uses a mocked LLM response so structure validation can be
checked without consuming API quota. Set BUSINESS_ADVISOR_LIVE=1 to run the
real Groq call as well.
"""

from __future__ import annotations

import json
import os
import sys
import types

# The M4 tests are deliberately runnable even when optional runtime packages
# (OpenAI client, Streamlit) are not installed on the test machine.
if "openai" not in sys.modules:
    fake_openai = types.ModuleType("openai")

    class _FakeOpenAI:
        def __init__(self, *args, **kwargs):
            pass

    fake_openai.OpenAI = _FakeOpenAI
    sys.modules["openai"] = fake_openai

import modules.business_advisor as business_advisor


SAMPLE_PROFILE = {
    "verified_skills": [
        {
            "skill": "Python",
            "confidence": "High",
            "evidence": "Multiple public repositories contain Python projects and automation code.",
        },
        {
            "skill": "SQL",
            "confidence": "High",
            "evidence": "Repository projects include SQL/database work.",
        },
        {
            "skill": "Financial Modeling",
            "confidence": "Medium",
            "evidence": "Project descriptions reference financial analysis/modeling workflows.",
        },
        {
            "skill": "React",
            "confidence": "Low",
            "evidence": "Limited repository evidence.",
        },
    ]
}


MOCK_RESULT = {
    "ideas": [
        {
            "title": "Automated Financial Reporting Service",
            "target_audience": "Small investment and accounting teams",
            "problem": "Teams spend too much time manually consolidating recurring financial reports.",
            "solution": "A Python/SQL automation service that ingests recurring data and produces standardized management reports.",
            "revenue_model": "One-time setup fee plus monthly reporting/maintenance subscription.",
            "skill_fit": "High-confidence Python and SQL evidence directly supports data automation and reporting workflows.",
            "budget_fit": "The initial version can be delivered with existing open-source tools and low infrastructure cost.",
            "first_30_days": [
                "Days 1-7: Interview 5-10 target users and define one recurring reporting workflow.",
                "Days 8-14: Build a narrow prototype using sample or customer-provided data.",
                "Days 15-21: Pilot the workflow with one user and measure time saved.",
                "Days 22-30: Package the service, pricing, onboarding, and first customer offer.",
            ],
        }
    ]
}


def run_structure_test() -> None:
    original = business_advisor.call_grok_json
    try:
        business_advisor.call_grok_json = lambda prompt: MOCK_RESULT
        result = business_advisor.generate_business_ideas(
            SAMPLE_PROFILE,
            budget="PKR 100,000",
            interest="financial automation",
        )
        assert result["status"] == "ok"
        assert len(result["ideas"]) == 1
        assert result["ideas"][0]["first_30_days"]
        print("PASS: mocked Business Advisor response validated.")
    finally:
        business_advisor.call_grok_json = original


def run_fallback_test() -> None:
    original = business_advisor.call_grok_json
    try:
        business_advisor.call_grok_json = lambda prompt: {"ideas": "not-a-list"}
        result = business_advisor.generate_business_ideas(
            SAMPLE_PROFILE,
            budget=100000,
            interest="financial automation",
        )
        assert result["ideas"] == []
        assert result["status"] == "empty"
        print("PASS: malformed LLM output falls back safely.")
    finally:
        business_advisor.call_grok_json = original


def run_missing_skill_test() -> None:
    result = business_advisor.generate_business_ideas(
        {"verified_skills": []},
        budget=100000,
        interest="software",
    )
    assert result["status"] == "missing_verified_skills"
    assert result["ideas"] == []
    print("PASS: missing verified skills handled safely.")


def run_live_test() -> None:
    result = business_advisor.generate_business_ideas(
        SAMPLE_PROFILE,
        budget="PKR 100,000",
        interest="financial automation",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run_structure_test()
    run_fallback_test()
    run_missing_skill_test()

    if os.getenv("BUSINESS_ADVISOR_LIVE") == "1":
        print("\nLIVE API TEST")
        run_live_test()
