"""
CareerPilot AI — Main Streamlit App
Owner: Member 5 (Streamlit / UI Engineer)

VISUAL REDESIGN ONLY.
All pipeline logic, function calls, session-state keys, and control flow
are unchanged from the working version of this file.
"""

import html
import streamlit as st

# ---------------------------------------------------------------------
# Imports from teammates' modules (UNCHANGED)
# ---------------------------------------------------------------------
from modules.career_advisor import (
    compute_career_matches,
    get_match_explanation,
    get_skill_gap,
    get_roadmap,
)

from modules.business_advisor import generate_business_ideas

# Uncomment once Member 2's shared pipeline functions are ready:
# from services.resume_parser import extract_cv_skills
# from services.github import verify_skills_from_github


st.set_page_config(page_title="CareerPilot AI", page_icon="🚀", layout="wide")

# =======================================================================
# DESIGN SYSTEM — Colors, Typography, Custom CSS (Dark Theme)
# =======================================================================
# Palette:
#   Primary accent      #6366F1  (indigo-500)
#   Primary hover       #818CF8  (indigo-400, brighter on dark)
#   Secondary accent    #38BDF8  (sky-400)
#   Page background     #0B1120  (near-navy, not pure black)
#   Secondary bg         #111827  (slate-900, sidebar/table headers)
#   Card background      #151F32  (elevated surface)
#   Input background     #0F172A  (recessed surface)
#   Border               #263145  (subtle slate-blue)
#   Main text            #E5E7EB  (soft light gray)
#   Heading text         #F8FAFC  (near white)
#   Muted text           #94A3B8  (slate-400)
#   Success   text #4ADE80 / bg #052e1a
#   Warning   text #FBBF24 / bg #3A2205
#   Error     text #F87171 / bg #3B0A0A
#   Info      text #60A5FA / bg #0C2A4E

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --cp-primary: #6366F1;
    --cp-primary-hover: #818CF8;
    --cp-secondary: #38BDF8;
    --cp-bg: #0B1120;
    --cp-bg-secondary: #111827;
    --cp-card: #151F32;
    --cp-border: #263145;
    --cp-text: #E5E7EB;
    --cp-heading: #F8FAFC;
    --cp-muted: #94A3B8;
    --cp-input-bg: #0F172A;
    --cp-success: #4ADE80;
    --cp-success-bg: #052e1a;
    --cp-warning: #FBBF24;
    --cp-warning-bg: #3A2205;
    --cp-error: #F87171;
    --cp-error-bg: #3B0A0A;
    --cp-info: #60A5FA;
    --cp-info-bg: #0C2A4E;
}

html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    color: var(--cp-text);
}

.stApp {
    background: var(--cp-bg);
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

section[data-testid="stSidebar"] {
    background: var(--cp-bg-secondary) !important;
}

/* ---- Native dropdown popover / options list (rendered outside main CSS scope) ---- */
div[data-baseweb="popover"] {
    background-color: var(--cp-card) !important;
}
ul[data-baseweb="menu"] {
    background-color: var(--cp-card) !important;
}
li[role="option"] {
    background-color: var(--cp-card) !important;
    color: var(--cp-text) !important;
}
li[role="option"]:hover {
    background-color: rgba(99, 102, 241, 0.18) !important;
}
div[data-baseweb="select"] span {
    color: var(--cp-text) !important;
}

/* ---- Hero header ---- */
.cp-hero {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 8px 0 4px 0;
}
.cp-hero-icon {
    font-size: 40px;
    line-height: 1;
}
.cp-hero-title {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--cp-heading);
    margin: 0;
}
.cp-hero-subtitle {
    font-size: 15px;
    color: var(--cp-muted);
    margin-top: 2px;
    font-weight: 500;
}
.cp-hero-divider {
    height: 1px;
    background: var(--cp-border);
    margin: 18px 0 28px 0;
    border: none;
}

/* ---- Section titles ---- */
.cp-section-title {
    font-size: 20px;
    font-weight: 700;
    color: var(--cp-heading);
    margin: 4px 0 14px 0;
    letter-spacing: -0.01em;
}
.cp-eyebrow {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--cp-primary);
    margin-bottom: 4px;
}

/* ---- Form / card container ---- */
div[data-testid="stForm"] {
    background: var(--cp-card);
    border: 1px solid var(--cp-border);
    border-radius: 16px;
    padding: 32px 32px 20px 32px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25), 0 4px 20px rgba(0, 0, 0, 0.2);
}

/* ---- Inputs ---- */
.stTextInput input, .stSelectbox div[data-baseweb="select"] > div, .stTextArea textarea {
    border-radius: 10px !important;
    border: 1.5px solid var(--cp-border) !important;
    background-color: var(--cp-input-bg) !important;
    color: var(--cp-text) !important;
    font-size: 14px !important;
    transition: border-color 0.15s ease;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--cp-primary) !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important;
}
.stTextInput label, .stSelectbox label, .stFileUploader label {
    font-weight: 600 !important;
    font-size: 13.5px !important;
    color: var(--cp-text) !important;
}

/* ---- File uploader ---- */
div[data-testid="stFileUploaderDropzone"] {
    background-color: var(--cp-input-bg) !important;
    border: 1.5px dashed var(--cp-border) !important;
    border-radius: 12px !important;
}
div[data-testid="stFileUploaderDropzone"] * {
    color: var(--cp-muted) !important;
}
div[data-testid="stFileUploaderFile"] {
    background-color: var(--cp-card) !important;
    color: var(--cp-text) !important;
}

/* ---- Buttons ---- */
.stButton button, .stFormSubmitButton button {
    background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
    color: #F8FAFC !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    font-weight: 600 !important;
    font-size: 14.5px !important;
    box-shadow: 0 2px 10px rgba(99, 102, 241, 0.35) !important;
    transition: transform 0.12s ease, box-shadow 0.12s ease !important;
}
.stButton button:hover, .stFormSubmitButton button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.5) !important;
    color: #F8FAFC !important;
}

/* ---- Tabs ---- */
div[data-testid="stTabs"] button[role="tab"] {
    font-weight: 600;
    font-size: 15px;
    color: var(--cp-muted);
    padding: 10px 4px;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--cp-primary) !important;
}
div[data-testid="stTabs"] div[data-baseweb="tab-highlight"] {
    background-color: var(--cp-primary) !important;
    height: 3px !important;
    border-radius: 3px;
}
div[data-testid="stTabs"] div[data-baseweb="tab-border"] {
    background-color: var(--cp-border) !important;
}

/* ---- Expanders (career match cards) ---- */
div[data-testid="stExpander"] {
    border: 1px solid var(--cp-border) !important;
    border-radius: 14px !important;
    background: var(--cp-card) !important;
    margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
    overflow: hidden;
}
div[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 14px 18px !important;
    color: var(--cp-text) !important;
}
div[data-testid="stExpander"] svg {
    fill: var(--cp-muted) !important;
}

/* ---- Metrics ---- */
div[data-testid="stMetric"] {
    background: var(--cp-card);
    border: 1px solid var(--cp-border);
    border-radius: 14px;
    padding: 16px 18px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}
div[data-testid="stMetricValue"] {
    color: var(--cp-primary) !important;
    font-weight: 800 !important;
}
div[data-testid="stMetricLabel"] {
    color: var(--cp-muted) !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    font-size: 11.5px !important;
    letter-spacing: 0.06em;
}

/* ---- Alerts ---- */
div[data-testid="stAlertContainer"] {
    border-radius: 12px !important;
    font-size: 14px !important;
    border-width: 1px !important;
    border-style: solid !important;
    background: var(--cp-card) !important;
}
div[data-testid="stAlertContainer"] p {
    color: var(--cp-text) !important;
}
div[data-testid="stAlertContentSuccess"] { color: var(--cp-success) !important; }
div[data-testid="stAlertContentWarning"] { color: var(--cp-warning) !important; }
div[data-testid="stAlertContentInfo"] { color: var(--cp-info) !important; }
div[data-testid="stAlertContentError"] { color: var(--cp-error) !important; }

/* ---- Native bordered containers (roadmap / business results) ---- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 16px !important;
    border-color: var(--cp-border) !important;
    background: var(--cp-card) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] * {
    color: var(--cp-text);
}

/* ---- Custom skill table ---- */
.cp-skill-table {
    width: 100%;
    border-collapse: collapse;
    background: var(--cp-card);
    border: 1px solid var(--cp-border);
    border-radius: 14px;
    overflow: hidden;
    font-size: 14px;
}
.cp-skill-table th {
    text-align: left;
    background: var(--cp-bg-secondary);
    color: var(--cp-muted);
    font-weight: 700;
    text-transform: uppercase;
    font-size: 11.5px;
    letter-spacing: 0.06em;
    padding: 12px 18px;
    border-bottom: 1px solid var(--cp-border);
}
.cp-skill-table td {
    padding: 12px 18px;
    border-bottom: 1px solid var(--cp-border);
    font-weight: 500;
}
.cp-skill-table tr:last-child td {
    border-bottom: none;
}

/* ---- Confidence / status badges ---- */
.cp-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 999px;
    font-size: 12.5px;
    font-weight: 700;
}
.cp-badge-high { background: var(--cp-success-bg); color: var(--cp-success); }
.cp-badge-medium { background: var(--cp-warning-bg); color: var(--cp-warning); }
.cp-badge-low { background: var(--cp-error-bg); color: var(--cp-error); }
.cp-badge-neutral { background: #EEF2FF; color: var(--cp-primary); }

/* ---- Progress bar for match % ---- */
.cp-progress-track {
    width: 100%;
    height: 8px;
    background: var(--cp-bg-secondary);
    border-radius: 999px;
    overflow: hidden;
    margin: 6px 0 2px 0;
}
.cp-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #6366F1, #38BDF8);
    border-radius: 999px;
}

/* ---- Match card header row inside expander body ---- */
.cp-match-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
}
.cp-match-pct {
    font-weight: 800;
    color: var(--cp-primary);
    font-size: 14px;
}

/* ---- Skill pill lists ---- */
.cp-pill-group { margin: 6px 0 2px 0; }
.cp-pill {
    display: inline-block;
    padding: 3px 10px;
    margin: 2px 4px 2px 0;
    border-radius: 8px;
    font-size: 12.5px;
    font-weight: 600;
}
.cp-pill-matched { background: var(--cp-success-bg); color: var(--cp-success); }
.cp-pill-missing { background: var(--cp-error-bg); color: var(--cp-error); }

/* ---- Business idea card ---- */
.cp-idea-card {
    background: var(--cp-card);
    border: 1px solid var(--cp-border);
    border-radius: 16px;
    padding: 22px 24px;
    margin-bottom: 18px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25);
}
.cp-idea-title {
    font-size: 19px;
    font-weight: 800;
    color: var(--cp-heading);
    margin-bottom: 10px;
}
.cp-idea-field {
    margin-bottom: 8px;
    font-size: 14px;
    line-height: 1.5;
}
.cp-idea-label {
    font-weight: 700;
    color: var(--cp-primary);
    margin-right: 4px;
}
.cp-idea-phase {
    font-size: 13.5px;
    padding: 4px 0 4px 14px;
    border-left: 2px solid var(--cp-border);
    margin-left: 2px;
    color: var(--cp-text);
}

/* ---- Footer ---- */
.cp-footer {
    text-align: center;
    color: var(--cp-muted);
    font-size: 12.5px;
    margin-top: 48px;
    padding-top: 18px;
    border-top: 1px solid var(--cp-border);
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def confidence_class(level: str) -> str:
    normalized = (level or "").strip().lower()
    if normalized == "high":
        return "cp-badge-high"
    if normalized == "medium":
        return "cp-badge-medium"
    if normalized == "low":
        return "cp-badge-low"
    return "cp-badge-neutral"


def render_skill_table(skills: dict) -> str:
    rows = ""
    for skill, confidence in skills.items():
        badge_cls = confidence_class(confidence)
        rows += (
            "<tr>"
            f"<td>{html.escape(str(skill))}</td>"
            f"<td><span class='cp-badge {badge_cls}'>{html.escape(str(confidence))}</span></td>"
            "</tr>"
        )
    return (
        "<table class='cp-skill-table'>"
        "<thead><tr><th>Skill</th><th>Confidence</th></tr></thead>"
        f"<tbody>{rows}</tbody>"
        "</table>"
    )


def render_pill_group(items, kind: str) -> str:
    if not items:
        return "<span class='cp-badge cp-badge-neutral'>None</span>"
    pill_cls = "cp-pill-matched" if kind == "matched" else "cp-pill-missing"
    pills = "".join(
        f"<span class='cp-pill {pill_cls}'>{html.escape(str(item))}</span>" for item in items
    )
    return f"<div class='cp-pill-group'>{pills}</div>"


# =======================================================================
# HEADER
# =======================================================================
st.markdown(
    """
    <div class="cp-hero">
        <div class="cp-hero-icon">🚀</div>
        <div>
            <p class="cp-hero-title">CareerPilot AI</p>
            <p class="cp-hero-subtitle">Your AI Career &amp; Business Advisor</p>
        </div>
    </div>
    <hr class="cp-hero-divider" />
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------
# Step 1 — User Profile Intake (UNCHANGED LOGIC)
# ---------------------------------------------------------------------
with st.form("profile_form"):
    st.markdown("<p class='cp-eyebrow'>Step 1</p>", unsafe_allow_html=True)
    st.markdown("<p class='cp-section-title'>👤 Your Profile</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
        education = st.text_input("Education (e.g. Computer Science)")
        github_username = st.text_input("GitHub Username")
    with col2:
        interests = st.text_input("Interests (e.g. AI, Web Development)")
        goal = st.text_input("Career Goal (e.g. AI Engineer)")
        cv_file = st.file_uploader("Upload your CV (PDF)", type=["pdf"])

    submitted = st.form_submit_button("Analyze My Profile")

# ---------------------------------------------------------------------
# Step 2 — Run the pipeline once the form is submitted (UNCHANGED LOGIC)
# ---------------------------------------------------------------------
if submitted:
    if not cv_file or not github_username:
        st.warning("Please upload a CV and enter a GitHub username to continue.")
        st.stop()

    with st.spinner("Analyzing your CV and GitHub projects..."):
        verified_skills = {
            "Python": "High",
            "Java": "High",
            "SQL": "Medium",
            "AI": "Low",
        }

    st.success("Analysis complete!")

    st.session_state["verified_skills"] = verified_skills
    st.session_state["interests"] = interests

# ---------------------------------------------------------------------
# Step 3 — Show results in tabs (UNCHANGED LOGIC, redesigned presentation)
# ---------------------------------------------------------------------
if "verified_skills" in st.session_state:
    verified_skills = st.session_state["verified_skills"]
    interests = st.session_state.get("interests", "")

    tab_career, tab_business = st.tabs(["🎯 Career Advisor", "💼 Business Advisor"])

    # ---------------- Career Advisor Tab ----------------
    with tab_career:
        st.markdown("<p class='cp-section-title'>Verified Skills</p>", unsafe_allow_html=True)
        st.markdown(render_skill_table(verified_skills), unsafe_allow_html=True)

        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        st.markdown("<p class='cp-section-title'>Career Matches</p>", unsafe_allow_html=True)
        matches = compute_career_matches(verified_skills)

        for m in matches:
            with st.expander(f"{m['role']} — {m['match_percent']}% match"):
                st.markdown(
                    f"""
                    <div class="cp-progress-track">
                        <div class="cp-progress-fill" style="width:{m['match_percent']}%;"></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown("<b>Matched skills</b>", unsafe_allow_html=True)
                st.markdown(render_pill_group(m['matched_skills'], "matched"), unsafe_allow_html=True)
                st.markdown("<b>Missing skills</b>", unsafe_allow_html=True)
                st.markdown(render_pill_group(m['missing_skills'], "missing"), unsafe_allow_html=True)

        top = matches[0]
        with st.spinner("Generating explanation..."):
            explanation = get_match_explanation(
                top["role"], top["match_percent"], top["matched_skills"], top["missing_skills"]
            )
        st.info(f"**Why {top['role']} is your top match:** {explanation}")

        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        st.markdown("<p class='cp-section-title'>Skill Gap &amp; Roadmap</p>", unsafe_allow_html=True)
        target_role = st.selectbox(
            "Choose a target role for your roadmap:",
            [m["role"] for m in matches],
        )
        gap = get_skill_gap(target_role, verified_skills)

        colA, colB, colC = st.columns(3)
        colA.metric("Have", len(gap["have"]))
        colB.metric("Partial", len(gap["partial"]))
        colC.metric("Missing", len(gap["missing"]))

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        if st.button("Generate Roadmap"):
            with st.spinner("Building your roadmap..."):
                roadmap = get_roadmap(target_role, gap)
            with st.container(border=True):
                st.markdown(roadmap)

    # ---------------- Business Advisor Tab ----------------
    with tab_business:
        st.markdown(
            "<p class='cp-section-title'>Business Ideas Based on Your Skills</p>",
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            budget = st.selectbox("Budget", ["Low", "Medium", "High"])
        with col2:
            business_interest = st.text_input(
                "Business Interest (e.g. Education, Health)", value=interests
            )

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("Generate Business Ideas"):
            with st.spinner("Thinking of business ideas..."):
                business_profile = {
                    "verified_skills": [
                        {"skill": k, "confidence": v, "evidence": ""}
                        for k, v in verified_skills.items()
                    ]
                }
                result = generate_business_ideas(business_profile, budget, business_interest)

            if result.get("status") == "ok" and result.get("ideas"):
                for idea in result["ideas"]:
                    phases_html = "".join(
                        f"<div class='cp-idea-phase'>{html.escape(str(phase))}</div>"
                        for phase in idea["first_30_days"]
                    )
                    st.markdown(
                        f"""
                        <div class="cp-idea-card">
                            <div class="cp-idea-title">{html.escape(str(idea['title']))}</div>
                            <div class="cp-idea-field"><span class="cp-idea-label">Target audience:</span>{html.escape(str(idea['target_audience']))}</div>
                            <div class="cp-idea-field"><span class="cp-idea-label">Problem:</span>{html.escape(str(idea['problem']))}</div>
                            <div class="cp-idea-field"><span class="cp-idea-label">Solution:</span>{html.escape(str(idea['solution']))}</div>
                            <div class="cp-idea-field"><span class="cp-idea-label">Revenue model:</span>{html.escape(str(idea['revenue_model']))}</div>
                            <div class="cp-idea-field"><span class="cp-idea-label">Why you fit:</span>{html.escape(str(idea['skill_fit']))}</div>
                            <div class="cp-idea-field"><span class="cp-idea-label">Budget fit:</span>{html.escape(str(idea['budget_fit']))}</div>
                            <div class="cp-idea-field" style="margin-top:10px;"><span class="cp-idea-label">First 30 days</span></div>
                            {phases_html}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.warning("No business idea could be generated. Try different inputs.")

# ---------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------
st.markdown(
    "<div class='cp-footer'>CareerPilot AI — AI Career &amp; Business Advisor</div>",
    unsafe_allow_html=True,
)