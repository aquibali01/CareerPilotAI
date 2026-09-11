from services.groq import call_groq


response = call_groq(
    "Say hello to CareerPilot AI and explain in one sentence what you can do."
)

print(response)