"""
planner.py — "Chaos" Meal Planner using GPT-4o.
Suggests 2 recipes from expiring + low-stock pantry items.
"""

import json
from openai import OpenAI

PLANNER_SYSTEM_PROMPT = """
You are a creative home chef AI for HomeBrain.

TASK: Suggest exactly 2 practical recipes using ONLY the ingredients provided.
These ingredients are either about to expire or running low — use as many as possible.

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
    """Return 2 recipe suggestions based on expiring + low-stock inventory items."""
    if not expiring_items:
        return []

    ingredient_list = "\n".join(
        f"- {i['product_name']} ({i['category']}, {i['days_remaining']} days left, status: {i.get('status', 'expiring')})"
        for i in expiring_items
    )

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        temperature=0.7,
        messages=[
            {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
            {"role": "user", "content": f"Ingredients about to expire or running low:\n{ingredient_list}\n\nSuggest 2 recipes."},
        ],
    )
    return json.loads(response.choices[0].message.content).get("recipes", [])
