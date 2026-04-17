"""
vision.py — GPT-4o Vision receipt analysis.
Single responsibility: take image bytes, return structured JSON.
"""

import base64
import json
import re
from openai import OpenAI

# ---------------------------------------------------------------------------
# System prompt — the core AI "contract" for consistent JSON output
# ---------------------------------------------------------------------------
RECEIPT_SYSTEM_PROMPT = """
You are a receipt analysis AI for HomeBrain, a household inventory management system.

TASK: Analyze the receipt image and extract every purchased item with full metadata.

SHELF LIFE ESTIMATION RULES (apply these to every item):
- Fresh produce (fruits, vegetables): 3–7 days
- Dairy (milk, yogurt, cheese): 7–14 days
- Meat & Fish (fresh/refrigerated): 1–3 days
- Bakery & Bread: 3–5 days
- Frozen foods: 60–180 days
- Canned goods: 365–730 days
- Dry pantry goods (pasta, rice, cereal, flour): 180–365 days
- Beverages (juice, soda): 7–14 days (opened), 180+ (sealed)
- Eggs: 21–35 days
- Cleaning & Household supplies: 730 days
- Personal care products: 365 days
- Snacks (chips, cookies): 30–90 days
- Condiments & Sauces: 30–180 days (opened), 365 (sealed)

CATEGORY TAXONOMY — use ONLY these values:
Produce | Dairy | Meat & Fish | Bakery | Frozen | Pantry | Beverages | Snacks | Household | Personal Care | Other

OUTPUT RULES (CRITICAL):
1. Return ONLY valid JSON — no markdown fences, no explanation, no wrapper text.
2. Every item MUST have all fields populated.
3. Normalize quantity strings: "2 lbs", "1 pack", "6 count", "500ml", "1 gallon".
4. If a price is unclear, set unit_price to null.
5. If a date is unclear, set purchase_date to null.
6. If an item is ambiguous, set confidence to "low".

EXACT OUTPUT SCHEMA:
{
  "store_name": "string or null",
  "purchase_date": "YYYY-MM-DD or null",
  "currency": "USD",
  "total_amount": float or null,
  "items": [
    {
      "product_name": "string (clean, title-cased, no abbreviations)",
      "category": "string (from taxonomy above)",
      "quantity": "string",
      "unit_price": float or null,
      "shelf_life_days": integer,
      "confidence": "high" | "medium" | "low"
    }
  ]
}
""".strip()


def _encode_image(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")


def _extract_json(text: str) -> dict:
    """Strip any accidental markdown fences and parse JSON."""
    clean = re.sub(r"```(?:json)?", "", text).strip()
    return json.loads(clean)


def analyze_receipt(image_bytes: bytes, client: OpenAI) -> dict:
    """
    Send receipt image to GPT-4o Vision.
    Returns parsed dict matching the schema above, or raises on failure.
    """
    b64 = _encode_image(image_bytes)

    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": RECEIPT_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64}",
                            "detail": "high",
                        },
                    },
                    {
                        "type": "text",
                        "text": "Please analyze this receipt and return the JSON inventory.",
                    },
                ],
            },
        ],
        max_tokens=2000,
        temperature=0.1,  # Low temp for consistent structured output
    )

    raw = response.choices[0].message.content
    return _extract_json(raw)
