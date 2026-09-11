from services.grok import call_grok


response = call_grok(
    "Say hello to CareerPilot AI and explain in one sentence what you can do."
)

print(response)