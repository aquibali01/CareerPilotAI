from services.resume_parser import extract_text_from_pdf
from services.grok import call_grok_json
from prompts.prompts import CV_ANALYSIS_PROMPT
import json

# Dummy CV text simulation for test
sample_cv_text = """
Aquib Ali
Master of Financial Engineering | Bachelor of Chemical Engineering
Skills: Python, SQL, Git, Financial Modeling, Power BI
Experience: Built automated trading algorithms using Python and Bitget API.
Projects: CareerPilot AI - AI Career Advisor using Streamlit & xAI Grok API.
"""

print("1. Testing Grok Structured CV Extraction...")
prompt = CV_ANALYSIS_PROMPT.format(cv_text=sample_cv_text)
structured_data = call_grok_json(prompt)

print("\n--- EXTRACTED CV JSON ---")
print(json.dumps(structured_data, indent=2))
print("--------------------------\n")