"""
product_images.py — Maps product names to emoji + gradient background.
No external CDN — always loads instantly.
"""

# ── Gradient backgrounds per category ────────────────────────
CATEGORY_GRADIENTS: dict[str, str] = {
    "Produce":      "linear-gradient(135deg,#86efac,#4ade80)",
    "Dairy":        "linear-gradient(135deg,#bae6fd,#60a5fa)",
    "Meat & Fish":  "linear-gradient(135deg,#fca5a5,#f87171)",
    "Bakery":       "linear-gradient(135deg,#fde68a,#f59e0b)",
    "Frozen":       "linear-gradient(135deg,#c7d2fe,#818cf8)",
    "Pantry":       "linear-gradient(135deg,#fed7aa,#fb923c)",
    "Beverages":    "linear-gradient(135deg,#a5f3fc,#22d3ee)",
    "Snacks":       "linear-gradient(135deg,#f9a8d4,#ec4899)",
    "Household":    "linear-gradient(135deg,#d1d5db,#9ca3af)",
    "Personal Care":"linear-gradient(135deg,#e9d5ff,#c084fc)",
    "Other":        "linear-gradient(135deg,#e2e8f0,#94a3b8)",
}

# ── Per-product emoji map (keyword → emoji) ───────────────────
_PRODUCT_EMOJIS: dict[str, str] = {
    # Dairy
    "milk":          "🥛", "whole milk":    "🥛", "almond milk":   "🥛",
    "oat milk":      "🥛", "soy milk":      "🥛",
    "egg":           "🥚", "eggs":          "🥚",
    "yogurt":        "🫙", "greek yogurt":  "🫙",
    "cheese":        "🧀", "cheddar":       "🧀", "mozzarella":    "🧀",
    "butter":        "🧈", "cream":         "🧈",
    # Produce
    "sweet potato":  "🍠", "yam":           "🍠",
    "tomato":        "🍅", "tomatoes":      "🍅", "cherry tomato": "🍅",
    "avocado":       "🥑",
    "banana":        "🍌", "bananas":       "🍌",
    "apple":         "🍎", "apples":        "🍎",
    "orange":        "🍊",
    "lemon":         "🍋", "lime":          "🍋",
    "strawberry":    "🍓", "strawberries":  "🍓",
    "grapes":        "🍇",
    "watermelon":    "🍉",
    "pineapple":     "🍍",
    "mango":         "🥭",
    "peach":         "🍑", "pear":          "🍐",
    "blueberry":     "🫐", "blueberries":   "🫐",
    "broccoli":      "🥦",
    "carrot":        "🥕", "carrots":       "🥕",
    "corn":          "🌽",
    "pepper":        "🌶", "bell pepper":   "🫑",
    "cucumber":      "🥒",
    "lettuce":       "🥬", "spinach":       "🥬", "baby spinach":  "🥬",
    "garlic":        "🧄",
    "onion":         "🧅",
    "potato":        "🥔", "potatoes":      "🥔",
    "mushroom":      "🍄", "mushrooms":     "🍄",
    "eggplant":      "🍆",
    "zucchini":      "🥒",
    # Meat & Fish
    "chicken":       "🍗", "chicken breast":"🍗",
    "beef":          "🥩", "steak":         "🥩", "ground beef":   "🥩",
    "pork":          "🥩", "lamb":          "🥩",
    "salmon":        "🐟", "tuna":          "🐟", "fish":          "🐟",
    "shrimp":        "🍤",
    # Bakery
    "bread":         "🍞", "sourdough":     "🍞", "pita":          "🫓",
    "bagel":         "🥯", "croissant":     "🥐", "muffin":        "🧁",
    # Pantry
    "pasta":         "🍝", "penne":         "🍝", "spaghetti":     "🍝",
    "fusilli":       "🍝",
    "rice":          "🍚",
    "olive oil":     "🫒", "oil":           "🫒",
    "honey":         "🍯",
    "salt":          "🧂",
    "tomato sauce":  "🥫", "crushed tomato":"🥫", "canned tomato": "🥫",
    "ketchup":       "🍅",
    "peanut butter": "🥜",
    "chocolate":     "🍫",
    "sugar":         "🍬",
    "flour":         "🌾",
    "oats":          "🌾", "cereal":        "🌾",
    "tahini":        "🫙",
    # Frozen
    "peas":          "🫛", "frozen peas":   "🫛",
    "ice cream":     "🍦",
    # Beverages
    "orange juice":  "🍊", "juice":         "🧃",
    "coffee":        "☕", "tea":           "🍵",
    "water":         "💧",
    "soda":          "🥤", "cola":          "🥤",
    "beer":          "🍺", "wine":          "🍷",
    # Snacks
    "chips":         "🥔", "crackers":      "🫙",
    "nuts":          "🥜", "almonds":       "🥜",
    "popcorn":       "🍿",
    # Household / Personal Care
    "soap":          "🧼", "dish soap":     "🧼",
    "shampoo":       "🧴", "toothpaste":    "🪥",
    "tissue":        "🧻", "paper towel":   "🧻",
}

# ── Category fallback emojis ──────────────────────────────────
_CATEGORY_EMOJI: dict[str, str] = {
    "Produce":      "🥬", "Dairy":        "🥛", "Meat & Fish":  "🥩",
    "Bakery":       "🍞", "Frozen":       "🧊", "Pantry":       "🫙",
    "Beverages":    "🧃", "Snacks":       "🍪", "Household":    "🧹",
    "Personal Care":"🧴", "Other":        "📦",
}


def get_product_image(product_name: str, category: str = "") -> str | None:
    """Returns an HTML string for the thumbnail (emoji + gradient bg), never None."""
    name_lower = product_name.lower().strip()

    # Exact match
    emoji = _PRODUCT_EMOJIS.get(name_lower)

    # Keyword match (longest key wins)
    if not emoji:
        best_key = ""
        for key in _PRODUCT_EMOJIS:
            if key in name_lower and len(key) > len(best_key):
                best_key = key
        if best_key:
            emoji = _PRODUCT_EMOJIS[best_key]

    # Category fallback
    if not emoji:
        emoji = _CATEGORY_EMOJI.get(category, "📦")

    gradient = CATEGORY_GRADIENTS.get(category, CATEGORY_GRADIENTS["Other"])
    return f'<div class="item-thumb item-thumb-emoji" style="background:{gradient}">{emoji}</div>'
