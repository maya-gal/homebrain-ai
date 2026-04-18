"""
vision.py — All AI input parsing for HomeBrain.
Three modes: receipt image, free text, voice recording.
"""

import json
import io
import base64
from openai import OpenAI

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
Infer shelf_life_days from the product type — do NOT read expiry dates from the receipt.
""".strip()

# ── Free text prompt ─────────────────────────────────────────────────────────
TEXT_SYSTEM_PROMPT = f"""
You are a grocery list parser for HomeBrain.
The user will give you a free-text list of items — in any language, any format.
Examples: "חלב, לחם, 6 ביצים, עגבניות 1 קג" or "milk x2, bread, eggs dozen, tomatoes"
Extract each product with its quantity (infer if not stated).
{_SHARED_RULES}
""".strip()

# ── Voice / audio prompt (post-transcription) ─────────────────────────────────
AUDIO_SYSTEM_PROMPT = f"""
You are a voice grocery list parser for HomeBrain.
The user dictated a list of products they want to add to their pantry.
The message may be in Hebrew, English, or mixed.
Extract each product mentioned with its quantity (infer if not stated).
{_SHARED_RULES}
""".strip()


def _make_client(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key)


# ── Public functions ─────────────────────────────────────────────────────────

def analyze_receipt(image_bytes: bytes, api_key: str) -> dict:
    """Receipt image → full JSON with store_name, items, etc."""
    client = _make_client(api_key)
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        temperature=0.1,
        messages=[
            {"role": "system", "content": RECEIPT_SYSTEM_PROMPT},
            {"role": "user", "content": [
                {"type": "text", "text": "Analyze this receipt and return the JSON inventory."},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{b64}",
                    "detail": "high",
                }},
            ]},
        ],
    )
    return json.loads(response.choices[0].message.content)


def parse_text_to_items(text: str, api_key: str) -> list[dict]:
    """Free-text grocery list → list of items."""
    client = _make_client(api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        temperature=0.1,
        messages=[
            {"role": "system", "content": TEXT_SYSTEM_PROMPT},
            {"role": "user", "content": f"Parse this grocery list into products:\n\n{text}"},
        ],
    )
    return json.loads(response.choices[0].message.content).get("items", [])


def parse_audio_to_items(audio_bytes: bytes, api_key: str) -> list[dict]:
    """Voice recording (WAV/WEBM bytes) → list of items via Whisper + GPT-4o."""
    client = _make_client(api_key)

    # Step 1: transcribe with Whisper-1
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "recording.wav"
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
    )

    # Step 2: parse transcript with GPT-4o
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        temperature=0.1,
        messages=[
            {"role": "system", "content": AUDIO_SYSTEM_PROMPT},
            {"role": "user", "content": f"Extract grocery products from this transcript:\n\n{transcript.text}"},
        ],
    )
    return json.loads(response.choices[0].message.content).get("items", [])
