"""
planner.py — "Chaos" Meal Planner using Gemini.
"""

import json
from google import genai
from google.genai import types

PLANNER_SYSTEM_PROMPT = """
You are a creative home chef AI for HomeBrain.

TASK: Suggest exactly 2 practical recipes using ONLY the ingredients provided.
These ingredients are about to expire — use as many as possible.

RULES:
1. Every recipe MUST use at least 2 of the listed ingredients.
2. Assume the family has: salt, pepper, oil, water, basic spices.
3. Weeknight friendly — under 30 minutes.
4. Return ONLY valid JSON — no markdown, no extra text.

OUTPUT SCHEMA:
{
  "recipes": [
    {
      "name": "string",
      "uses_ingredients": ["ingredient names from input"],
      "prep_time_minutes": integer,
      "instructions": ["step 1", "step 2", "step 3"],
      "tip": "string"
    }
  ]
}
""".strip()


def suggest_meals(expiring_items: list[dict], api_key: str) -> list[dict]:
    """Return 2 recipe suggestions based on expiring inventory items."""
    if not expiring_items:
        return []

    ingredient_list = "\n".join(
        f"- {i['product_name']} ({i['category']}, {i['days_remaining']} days left)"
        for i in expiring_items
    )

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Ingredients about to expire:\n{ingredient_list}\n\nSuggest 2 recipes.",
        config=types.GenerateContentConfig(
            system_instruction=PLANNER_SYSTEM_PROMPT,
            response_mime_type="application/json",
            temperature=0.7,
        ),
    )
    return json.loads(response.text).get("recipes", [])
