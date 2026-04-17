"""
planner.py — "Chaos" Meal Planner.
Reads expiring items from the DB and asks GPT-4o for 2 recipes.
"""

from openai import OpenAI

PLANNER_SYSTEM_PROMPT = """
You are a creative home chef AI for HomeBrain.

TASK: Suggest exactly 2 practical recipes using ONLY the ingredients provided.
These ingredients are about to expire, so use as many of them as possible.

RULES:
1. Every recipe MUST use at least 2 of the listed ingredients.
2. You may assume the family has common pantry staples (salt, pepper, oil, water, basic spices).
3. Keep recipes simple — weeknight friendly, under 30 minutes.
4. Return ONLY valid JSON — no markdown, no extra text.

OUTPUT SCHEMA:
{
  "recipes": [
    {
      "name": "string",
      "uses_ingredients": ["list of matched ingredient names from input"],
      "prep_time_minutes": integer,
      "instructions": ["step 1", "step 2", "step 3"],
      "tip": "string (one helpful tip)"
    }
  ]
}
""".strip()


def suggest_meals(expiring_items: list[dict], client: OpenAI) -> list[dict]:
    """
    Given a list of expiring inventory items, return 2 recipe suggestions.
    Returns an empty list if there are no items or the API call fails.
    """
    if not expiring_items:
        return []

    ingredient_list = "\n".join(
        f"- {item['product_name']} ({item['category']}, {item['days_remaining']} days left)"
        for item in expiring_items
    )
    user_message = f"Ingredients about to expire:\n{ingredient_list}\n\nSuggest 2 recipes."

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            max_tokens=1200,
            temperature=0.7,  # A bit of creativity for recipes
        )
        import json
        data = json.loads(response.choices[0].message.content)
        return data.get("recipes", [])
    except Exception as e:
        raise RuntimeError(f"Meal planner failed: {e}") from e
