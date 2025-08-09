import requests

# Gemini API key
GEMINI_API_KEY = "AIzaSyAKMtVR_GfkkNHC7uatGDEu6iu_olyf2yw"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# Example tasks already used this week
current_week_tasks = [
    "Use reusable water bottle",
    "Switch off lights when not in use",
    "Plant a tree",
    "Recycle plastic bottles",
    "Avoid single-use plastics"
]

# Construct prompt
prompt = f"""
You are an eco-awareness and sustainability assistant for a premium website called
"Leaflog".
Your job is to generate the daily eco-awareness plan.

Requirements:
- You will be given a list of eco tasks already generated this week:
{current_week_tasks}
- Generate exactly 5 **new unique eco tasks** that are **NOT** in the list above.
- For each task:
    - Give a short, clear, user-friendly description.
    - Assign **EcoCoins** for completion (between 5 and 50).
    - Provide measurable **impact** in one of the two formats:
        1. "CO₂ saved: X kg"
        2. "Water saved: X liters"
- Add a **daily eco-friendly inspiration quote** (short, motivational).
- Output must be **valid JSON** in the following exact structure:
{{
    "tasks": [
        {{
            "task": "string",
            "eco_coins": integer,
            "impact": "string"
        }}
    ],
    "quote": "string"
}}

Ensure:
- No repeated tasks from input list.
- All output is realistic, factually sound, and in plain English.
- Keep descriptions short, friendly, and easy to understand.
"""

# API request payload
payload = {
    "contents": [
        {
            "parts": [{"text": prompt}]
        }
    ]
}

# Call Gemini API
response = requests.post(
    f"{GEMINI_URL}?key={GEMINI_API_KEY}",
    json=payload,
    headers={"Content-Type": "application/json"}
)

# Handle response
if response.status_code != 200:
    print("Error:", response.text)
else:
    gemini_output = response.json()
    try:
        generated_text = gemini_output["candidates"][0]["content"]["parts"][0]["text"]
        print("Generated Output:\n", generated_text)
    except Exception as e:
        print("Error parsing Gemini response:", e)
