SYSTEM_JSON_PROMPT = """You are a JSON-only API. Respond with ONLY valid JSON.
No markdown code fences (e.g. do not wrap in ```json), no explanations, no text before or after the JSON.
If a value is unknown, use null or an empty array [] — never omit a required key.
Your entire response must be parseable by json.loads() with no modification."""

CV_ANALYSIS_PROMPT = """Analyze the following resume text and extract key structured information.

Resume Text:
{cv_text}

Return a JSON object with EXACTLY this structure:
{{
  "candidate_name": "Full Name or null",
  "education": "Degree and Institution summary",
  "skills": ["Skill1", "Skill2", "Skill3"],
  "projects": [
    {{
      "title": "Project Name",
      "technologies": ["Tech1", "Tech2"],
      "description": "Brief summary"
    }}
  ],
  "experience_years": 2.5,
  "certifications": ["Cert1", "Cert2"]
}}
"""

SKILL_VERIFICATION_PROMPT = """You are an expert technical evaluator. Compare the user's claimed skills from their CV against their actual GitHub evidence.

CV Claimed Skills:
{cv_skills}

GitHub Profile Summary:
{github_data}

For each claimed skill, evaluate the actual GitHub evidence and assign a confidence rating:
- High: Clear repository evidence, major language usage, or relevant project code/descriptions.
- Medium: Secondary evidence, listed in topics/descriptions, or indirect project usage.
- Low: No relevant repository, language, or project evidence found on GitHub.

Return ONLY a JSON object formatted as follows:
{{
  "verified_skills": [
    {{
      "skill": "Python",
      "confidence": "High",
      "evidence": "Multiple repositories using Python as primary language."
    }},
    {{
      "skill": "Docker",
      "confidence": "Low",
      "evidence": "No Dockerfiles or Docker configuration found in public repositories."
    }}
  ]
}}
"""