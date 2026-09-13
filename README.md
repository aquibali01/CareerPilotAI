# 🚀 CareerPilot AI

**Your AI Career & Business Advisor**

CareerPilot AI is an AI-powered platform that analyzes a user's resume and GitHub activity to deliver personalized, evidence-based career and business guidance. Rather than trusting self-reported skills, the platform verifies them against real project evidence, then generates a career-fit match, a skill-gap roadmap, and — for users interested in entrepreneurship — tailored business ideas built around their verified skillset.

> *"CareerPilot AI doesn't just ask what skills you have — it verifies what you've actually built, and shows you exactly what's next."*

Built in 48 hours for **Hackathon 2026**.

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Team](#-team)
- [Future Scope](#-future-scope)

---

## 🎯 Problem Statement

Most career advice tools rely entirely on self-reported skills and generic questionnaires. There is no way to verify what a candidate actually knows versus what they claim, and advice is rarely grounded in real, demonstrated work — leaving both candidates and recruiters with no reliable signal of true proficiency.

## 💡 Solution

CareerPilot AI verifies claimed skills against real GitHub repositories and code, then uses that verified profile to power two focused advisory modes: **Career Advisor** and **Business Advisor**. The core differentiator: guidance grounded in evidence, not self-report.

---

## ✨ Features

### 🔐 Skill Verification (Core Differentiator)
Parses the uploaded CV to extract claimed skills, then cross-references them against the user's public GitHub repositories, languages, and code. Each skill receives a confidence rating — **High**, **Medium**, or **Low** — based on real evidence rather than being taken at face value.

### 🎯 Career Advisor
- Ranks career-fit matches across multiple roles with a percentage score
- AI-generated, evidence-based explanation for the top match
- Skill-gap breakdown for any target role (have / partial / missing)
- Personalized month-by-month learning roadmap

### 💼 Business Advisor
- Generates evidence-grounded business ideas from the user's verified skills, budget, and interests
- Each idea includes target audience, problem, solution, revenue model, skill fit, and a 30-day launch plan
- Validated output schema ensures only complete, well-formed ideas reach the UI

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | [Streamlit](https://streamlit.io) | Rapid, pure-Python UI — file upload, tabs, forms, and results rendering |
| **Intelligence Layer** | [Groq API](https://groq.com) (OpenAI-compatible) | CV analysis, skill verification reasoning, career explanations, roadmap and business-idea generation |
| **Backend** | Python | CV parsing (PDF), GitHub REST API integration, JSON parsing and validation |
| **Data Source** | GitHub REST API | Fetches real repositories and code to verify claimed skills |

### Reliability Engineering

Because a live demo can't tolerate a broken AI call, every request to the intelligence layer follows defensive patterns:

- Strict system prompts enforcing JSON-only output for structured steps
- Defensive parsing that strips stray markdown fences before parsing JSON
- Automatic retries on parse failure, with a `max_tokens` ceiling raised to prevent response truncation
- Try/except wrapping on every AI call with a same-shape fallback, so a failed call degrades gracefully instead of crashing the UI
- Output schema validation on the Business Advisor module — malformed responses are filtered out before reaching the user

---

## 🏗 Architecture

```
User Inputs (CV + GitHub username)
            │
            ▼
      Streamlit UI
            │
            ▼
     Python Backend  ──────────►  GitHub REST API
   (resume_parser.py,                   │
      github.py)      ◄─────────────────┘
            │
            ▼
   Verified Skill Profile
   { skill, confidence, evidence }
            │
            ▼
        Groq API
   (reasoning & generation)
            │
    ┌───────┴────────┐
    ▼                ▼
Career Advisor   Business Advisor
(match %, gap,   (ideas + 30-day
 roadmap)         plan)
            │
            ▼
   Results render in
     Streamlit UI
```

---

## 📁 Project Structure

```
CareerPilotAI/
├── app.py                      # Streamlit UI — entry point
├── modules/
│   ├── career_advisor.py       # Scoring, explanation, skill gap, roadmap
│   └── business_advisor.py     # Idea generation, output validation
├── services/
│   ├── grok.py                 # AI API wrapper (Groq, OpenAI-compatible)
│   ├── github.py                # GitHub skill verification
│   └── resume_parser.py        # CV parsing
├── prompts/
│   └── prompts.py              # System & user prompt templates
├── data/
│   └── career_requirements.json # Static career-role requirement dataset
├── requirements.txt
└── README.md
```

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.10+
- A free [Groq API key](https://console.groq.com)

### Installation

```bash
# Clone the repository
git clone https://github.com/aquibali01/CareerPilotAI.git
cd CareerPilotAI

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

### Run the app

```bash
streamlit run app.py
```
The app will open automatically in your browser at http://localhost:8501.

Or use the live deployed app

CareerPilot AI is deployed on Streamlit Community Cloud — no installation needed:

🔗 Live App Link

https://careerpilotai-npi3s2sbx4uucmtx2vaip2.streamlit.app/
---

## 👥 Team

Built by a team of 5 in 48 hours for Hackathon 2026:

| Member | Role |
|---|---|
| **Anum Usman Khan** | Team Lead — Documentation, Presentation & Cross-Team Support |
| **Aquib Ali** | Shared Pipeline Engineer — CV + GitHub Verification |
| **Nimra Nadeem** | Career Advisor Engineer — Scoring, Gap & Roadmap |
| **Syed Ghulam Ahmed** | Business Advisor Engineer — Idea Generation & Validation |
| **Noor-ul-Ain** | Streamlit / UI Engineer — Application & Integration |

> **Note:** While Members 3, 4, and 5 owned their respective modules, Anum Usman Khan was directly involved in testing, debugging, and validating each of their components — including resolving dependency and environment errors, verifying live AI outputs, fixing import and integration issues, and confirming the Streamlit application ran end-to-end before submission.

---

## 🔮 Future Scope

- **Content Planner** module — helping users build a professional online presence aligned with verified skills
- **Cybersecurity Advisor** module — a defensive scan of a user's own repositories for common security issues
- Expanded career-role dataset beyond the current hardcoded set
- User accounts and saved progress over time

---

## 📄 License

This project was built for Hackathon 2026. Licensing details to be added.
