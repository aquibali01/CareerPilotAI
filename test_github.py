import json
from services.github import fetch_github_user_data
from services.grok import call_grok_json
from prompts.prompts import SKILL_VERIFICATION_PROMPT

# Test with a known username or your own
test_github_username = "aquibali01"  # Or your personal GitHub handle
sample_cv_skills = ["C", "Git", "Linux", "Python", "React"]

print(f"1. Fetching GitHub data for user: '{test_github_username}'...")
github_data = fetch_github_user_data(test_github_username)

print("2. Verifying skills with Grok...")
prompt = SKILL_VERIFICATION_PROMPT.format(
    cv_skills=json.dumps(sample_cv_skills),
    github_data=json.dumps(github_data)
)

verified_profile = call_grok_json(prompt)

print("\n--- VERIFIED SKILL PROFILE MATRIX ---")
print(json.dumps(verified_profile, indent=2))
print("------------------------------------\n")