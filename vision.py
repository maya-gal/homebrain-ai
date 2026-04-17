"""
vision.py — Gemini Vision receipt analysis.
Uses the google-genai SDK (google.genai).
"""

import json
import io
from PIL import Image
from google import genai
from google.genai import types

RECEIPT_SYSTEM_PROMPT = """
You are a receipt analysis AI for HomeBrain, a household inventory management system.

TASK: Analyze the receipt image and extract every purchased item with full metadata.

SHELF LIFE ESTIMATION RULES (apply to every item):
- Fresh produce (fruits, vegetables): 3–7 days
- Dairy (milk, yogurt, cheese): 7–14 days
- Meat & Fish (fresh/refrigerated): 1–3 days
- Bakery & Bread: 3–5 days
- Frozen foods: 60–180 days
- Canned goods: 365–730 days
- Dry pantry goods (pasta, rice, cereal, flour): 180–365 days
- Beverages: 7–14 days (opened), 180+ (sealed)
- Eggs: 21–35 days
- Cleaning & Household: 730 days
- Personal care: 365 days
- Snacks: 30–90 days

CATEGORY TAXONOMY — use ONLY these values:
Produce | Dairy | Meat & Fish | Bakery | Frozen | Pantry | Beverages | Snacks | Household | Personal Care | Other

RULES:
1. Return ONLY valid JSON — no markdown, no explanation.
2. Every item MUST have all fields.
3. Normalize quantity: "2 lbs", "1 pack", "6 count", "500ml".
4. Set unit_price/purchase_date to null if unclear.
5. Set confidence to "low" if ambiguous.

OUTPUT SCHEMA:
{
  "store_name": "string or null",
  "purchase_date": "YYYY-MM-DD or null",
  "currency": "USD",
  "total_amount": float or null,
  "items": [
    {
      "product_name": "string (title-cased, no abbreviations)",
      "category": "string",
      "quantity": "string",
      "unit_price": float or null,
      "shelf_life_days": integer,
      "confidence": "high" | "medium" | "low"
    }
  ]
}
""".strip()


def analyze_receipt(image_bytes: bytes, api_key: str) -> dict:
    """Send receipt image to Gemini Vision, return structured dict."""
    client = genai.Client(api_key=api_key)
    image  = Image.open(io.BytesIO(image_bytes))

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=["Analyze this receipt and return the JSON inventory.", image],
        config=types.GenerateContentConfig(
            system_instruction=RECEIPT_SYSTEM_PROMPT,
            response_mime_type="application/json",
            temperature=0.1,
        ),
    )
    return json.loads(response.text)
