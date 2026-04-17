"""
vision.py — All AI input parsing for HomeBrain.
Three modes: receipt image, free text, voice recording.
"""

import json
import io
from PIL import Image
from google import genai
from google.genai import types

# ── Shared shelf-life + category rules (reused across all prompts) ──────────
_SHARED_RULES = """
SHELF LIFE ESTIMATION RULES:
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

OUTPUT SCHEMA (return ONLY this JSON, nothing else):
{
  "items": [
    {
      "product_name": "string (title-cased, clean name)",
      "category": "string (from taxonomy)",
      "quantity": "string (e.g. '1 liter', '6 count', '2 packs')",
      "shelf_life_days": integer,
      "confidence": "high" | "medium" | "low"
    }
  ]
}
""".strip()

# ── Receipt image prompt ─────────────────────────────────────────────────────
RECEIPT_SYSTEM_PROMPT = f"""
You are a receipt analysis AI for HomeBrain, a household inventory management system.
Analyze the receipt image and extract every purchased item.
{_SHARED_RULES}
Also extract: "store_name", "purchase_date" (YYYY-MM-DD), "total_amount" (float), "currency".
Add those fields at the top level of the JSON alongside "items".
""".strip()

# ── Free text prompt ─────────────────────────────────────────────────────────
TEXT_SYSTEM_PROMPT = f"""
You are a grocery list parser for HomeBrain.
The user will give you a free-text list of items — in any language, any format.
Examples: "חלב, לחם, 6 ביצים, עגבניות 1 קג" or "milk x2, bread, eggs dozen, tomatoes"
Extract each product with its quantity (infer if not stated).
{_SHARED_RULES}
""".strip()

# ── Voice / audio prompt ─────────────────────────────────────────────────────
AUDIO_SYSTEM_PROMPT = f"""
You are a voice grocery list parser for HomeBrain.
The user recorded a voice message listing products they want to add to their pantry.
The message may be in Hebrew, English, or mixed.
Transcribe the audio mentally, then extract each product mentioned.
{_SHARED_RULES}
""".strip()


def _make_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)


def _base_config(temperature: float = 0.1) -> types.GenerateContentConfig:
    return types.GenerateContentConfig(
        response_mime_type="application/json",
        temperature=temperature,
    )


# ── Public functions ─────────────────────────────────────────────────────────

def analyze_receipt(image_bytes: bytes, api_key: str) -> dict:
    """Receipt image → full JSON with store_name, items, etc."""
    client = _make_client(api_key)
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


def parse_text_to_items(text: str, api_key: str) -> list[dict]:
    """Free-text grocery list → list of items."""
    client = _make_client(api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Parse this grocery list into products:\n\n{text}",
        config=types.GenerateContentConfig(
            system_instruction=TEXT_SYSTEM_PROMPT,
            response_mime_type="application/json",
            temperature=0.1,
        ),
    )
    return json.loads(response.text).get("items", [])


def parse_audio_to_items(audio_bytes: bytes, api_key: str) -> list[dict]:
    """Voice recording (WAV/WEBM bytes) → list of items."""
    client = _make_client(api_key)
    audio_part = types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[audio_part, "Extract the grocery products mentioned in this recording."],
        config=types.GenerateContentConfig(
            system_instruction=AUDIO_SYSTEM_PROMPT,
            response_mime_type="application/json",
            temperature=0.1,
        ),
    )
    return json.loads(response.text).get("items", [])
