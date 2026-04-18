"""
product_images.py — Real product photos (Unsplash CDN) with emoji fallback.
"""

_BASE = "https://images.unsplash.com/photo-{}?w=200&h=200&fit=crop&auto=format&q=80"

# ── Real photo URLs per keyword ───────────────────────────────
_PRODUCT_PHOTOS: dict[str, str] = {
    # Dairy
    "milk":           _BASE.format("1550583724-b2692b85b150"),
    "whole milk":     _BASE.format("1550583724-b2692b85b150"),
    "almond milk":    _BASE.format("1550583724-b2692b85b150"),
    "oat milk":       _BASE.format("1550583724-b2692b85b150"),
    "eggs":           _BASE.format("1582722872445-44dc5f7e3c8f"),
    "egg":            _BASE.format("1582722872445-44dc5f7e3c8f"),
    "cheese":         _BASE.format("1486297678162-eb2a19b0a32d"),
    "cheddar":        _BASE.format("1486297678162-eb2a19b0a32d"),
    "mozzarella":     _BASE.format("1486297678162-eb2a19b0a32d"),
    "butter":         _BASE.format("1589985270826-4b7bb135bc9d"),
    "yogurt":         _BASE.format("1488477181946-6428a0291777"),
    "greek yogurt":   _BASE.format("1488477181946-6428a0291777"),
    # Produce
    "apple":          _BASE.format("1567306226416-28f0efdc88ce"),
    "apples":         _BASE.format("1567306226416-28f0efdc88ce"),
    "banana":         _BASE.format("1571771894821-ce9b6c11b08e"),
    "bananas":        _BASE.format("1571771894821-ce9b6c11b08e"),
    "orange":         _BASE.format("1557800636-894a64c1696f"),
    "oranges":        _BASE.format("1557800636-894a64c1696f"),
    "lemon":          _BASE.format("1590502160462-58efa1e22d62"),
    "lemons":         _BASE.format("1590502160462-58efa1e22d62"),
    "strawberry":     _BASE.format("1464965911861-746a04b4bca6"),
    "strawberries":   _BASE.format("1464965911861-746a04b4bca6"),
    "blueberry":      _BASE.format("1498557850523-fd3d118b962e"),
    "blueberries":    _BASE.format("1498557850523-fd3d118b962e"),
    "avocado":        _BASE.format("1523049673857-eb18f1d7b578"),
    "tomato":         _BASE.format("1546069901-ba9599a7e63c"),
    "tomatoes":       _BASE.format("1546069901-ba9599a7e63c"),
    "cherry tomato":  _BASE.format("1546069901-ba9599a7e63c"),
    "broccoli":       _BASE.format("1459411621453-7b03977f4bfc"),
    "carrot":         _BASE.format("1598170845058-32b9d6a5da37"),
    "carrots":        _BASE.format("1598170845058-32b9d6a5da37"),
    "spinach":        _BASE.format("1540420773420-3350e52aae6e"),
    "lettuce":        _BASE.format("1540420773420-3350e52aae6e"),
    "baby spinach":   _BASE.format("1540420773420-3350e52aae6e"),
    "potato":         _BASE.format("1518977676767-9c21b83cf7d2"),
    "potatoes":       _BASE.format("1518977676767-9c21b83cf7d2"),
    "onion":          _BASE.format("1587049352851-8d4be89cf6ea"),
    "onions":         _BASE.format("1587049352851-8d4be89cf6ea"),
    "garlic":         _BASE.format("1615478166193-1f62ac3c50db"),
    "cucumber":       _BASE.format("1449300079674-5a87db1b3168"),
    "mushroom":       _BASE.format("1504674900247-0877df9cc836"),
    "mushrooms":      _BASE.format("1504674900247-0877df9cc836"),
    "mango":          _BASE.format("1553279243-4ec44082c1f3"),
    "grapes":         _BASE.format("1537640538966-cf1a0b9e6e58"),
    "watermelon":     _BASE.format("1587049352851-8d4be89cf6ea"),
    "corn":           _BASE.format("1601493700631-2b16ec4b4716"),
    "bell pepper":    _BASE.format("1563565453-00e02add09e2"),
    "pepper":         _BASE.format("1563565453-00e02add09e2"),
    "sweet potato":   _BASE.format("1596097635121-14b38c5d3a52"),
    # Meat & Fish
    "chicken":        _BASE.format("1587593810167-a84920ea0781"),
    "chicken breast": _BASE.format("1587593810167-a84920ea0781"),
    "beef":           _BASE.format("1529694157872-4e29e5e735f4"),
    "steak":          _BASE.format("1529694157872-4e29e5e735f4"),
    "ground beef":    _BASE.format("1529694157872-4e29e5e735f4"),
    "salmon":         _BASE.format("1499125562588-29fb8a56b5d5"),
    "fish":           _BASE.format("1499125562588-29fb8a56b5d5"),
    "tuna":           _BASE.format("1499125562588-29fb8a56b5d5"),
    # Bakery
    "bread":          _BASE.format("1509440159596-0249088772ff"),
    "sourdough":      _BASE.format("1509440159596-0249088772ff"),
    "whole wheat bread": _BASE.format("1509440159596-0249088772ff"),
    "bagel":          _BASE.format("1509440159596-0249088772ff"),
    "croissant":      _BASE.format("1555507036-ab794f575b4b"),
    # Pantry
    "pasta":          _BASE.format("1551462147-ff29053bfc14"),
    "spaghetti":      _BASE.format("1551462147-ff29053bfc14"),
    "penne":          _BASE.format("1551462147-ff29053bfc14"),
    "rice":           _BASE.format("1586201375761-83865001e31c"),
    "olive oil":      _BASE.format("1474979078840-989bcd8c4715"),
    "coffee":         _BASE.format("1495474472287-4d71bcdd2085"),
    "orange juice":   _BASE.format("1600271886742-f049cd451bba"),
    "juice":          _BASE.format("1600271886742-f049cd451bba"),
    "chocolate":      _BASE.format("1481391319815-a35a7a3e5b5b"),
    "peanut butter":  _BASE.format("1612929633738-8fe44f7ec841"),
    "honey":          _BASE.format("1587049352851-8d4be89cf6ea"),
    "oats":           _BASE.format("1614961233688-6c0ba63c2b96"),
    "cereal":         _BASE.format("1614961233688-6c0ba63c2b96"),
    "flour":          _BASE.format("1574323347407-f5e1ad6d020b"),
    "sugar":          _BASE.format("1574323347407-f5e1ad6d020b"),
}

# ── Emoji fallbacks ───────────────────────────────────────────
_PRODUCT_EMOJIS: dict[str, str] = {
    "milk": "🥛", "whole milk": "🥛", "almond milk": "🥛", "oat milk": "🥛", "soy milk": "🥛",
    "egg": "🥚", "eggs": "🥚",
    "yogurt": "🫙", "greek yogurt": "🫙",
    "cheese": "🧀", "cheddar": "🧀", "mozzarella": "🧀",
    "butter": "🧈", "cream": "🧈",
    "sweet potato": "🍠", "yam": "🍠",
    "tomato": "🍅", "tomatoes": "🍅", "cherry tomato": "🍅",
    "avocado": "🥑",
    "banana": "🍌", "bananas": "🍌",
    "apple": "🍎", "apples": "🍎",
    "orange": "🍊", "oranges": "🍊",
    "lemon": "🍋", "lime": "🍋",
    "strawberry": "🍓", "strawberries": "🍓",
    "grapes": "🍇",
    "watermelon": "🍉",
    "pineapple": "🍍",
    "mango": "🥭",
    "peach": "🍑", "pear": "🍐",
    "blueberry": "🫐", "blueberries": "🫐",
    "broccoli": "🥦",
    "carrot": "🥕", "carrots": "🥕",
    "corn": "🌽",
    "pepper": "🌶", "bell pepper": "🫑",
    "cucumber": "🥒",
    "lettuce": "🥬", "spinach": "🥬", "baby spinach": "🥬",
    "garlic": "🧄",
    "onion": "🧅",
    "potato": "🥔", "potatoes": "🥔",
    "mushroom": "🍄", "mushrooms": "🍄",
    "eggplant": "🍆",
    "chicken": "🍗", "chicken breast": "🍗",
    "beef": "🥩", "steak": "🥩", "ground beef": "🥩",
    "pork": "🥩", "lamb": "🥩",
    "salmon": "🐟", "tuna": "🐟", "fish": "🐟",
    "shrimp": "🍤",
    "bread": "🍞", "sourdough": "🍞", "pita": "🫓",
    "bagel": "🥯", "croissant": "🥐", "muffin": "🧁",
    "pasta": "🍝", "penne": "🍝", "spaghetti": "🍝",
    "rice": "🍚",
    "olive oil": "🫒", "oil": "🫒",
    "honey": "🍯",
    "salt": "🧂",
    "tomato sauce": "🥫", "ketchup": "🍅",
    "peanut butter": "🥜",
    "chocolate": "🍫",
    "sugar": "🍬",
    "flour": "🌾",
    "oats": "🌾", "cereal": "🌾",
    "tahini": "🫙",
    "peas": "🫛",
    "ice cream": "🍦",
    "orange juice": "🍊", "juice": "🧃",
    "coffee": "☕", "tea": "🍵",
    "water": "💧",
    "soda": "🥤", "cola": "🥤",
    "beer": "🍺", "wine": "🍷",
    "chips": "🥔", "nuts": "🥜", "almonds": "🥜",
    "popcorn": "🍿",
    "soap": "🧼", "dish soap": "🧼",
    "shampoo": "🧴", "toothpaste": "🪥",
    "tissue": "🧻", "paper towel": "🧻",
}

_CATEGORY_EMOJI: dict[str, str] = {
    "Produce": "🥬", "Dairy": "🥛", "Meat & Fish": "🥩",
    "Bakery": "🍞", "Frozen": "🧊", "Pantry": "🫙",
    "Beverages": "🧃", "Snacks": "🍪", "Household": "🧹",
    "Personal Care": "🧴", "Other": "📦",
}

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


def _lookup(name_lower: str, mapping: dict) -> str | None:
    if name_lower in mapping:
        return mapping[name_lower]
    best_key = max(
        (k for k in mapping if k in name_lower),
        key=len, default=""
    )
    return mapping[best_key] if best_key else None


def get_product_image(product_name: str, category: str = "") -> str:
    """Returns an HTML thumbnail — real photo if available, emoji+gradient fallback."""
    name_lower = product_name.lower().strip()
    photo_url  = _lookup(name_lower, _PRODUCT_PHOTOS)

    if photo_url:
        emoji    = _lookup(name_lower, _PRODUCT_EMOJIS) or _CATEGORY_EMOJI.get(category, "📦")
        gradient = CATEGORY_GRADIENTS.get(category, CATEGORY_GRADIENTS["Other"])
        fallback = f"this.outerHTML='<div class=\\'item-thumb item-thumb-emoji\\' style=\\'background:{gradient}\\'>{emoji}</div>'"
        return (
            f'<img class="item-thumb" src="{photo_url}" alt="{product_name}" '
            f'onerror="{fallback}">'
        )

    # Emoji fallback
    emoji    = _lookup(name_lower, _PRODUCT_EMOJIS) or _CATEGORY_EMOJI.get(category, "📦")
    gradient = CATEGORY_GRADIENTS.get(category, CATEGORY_GRADIENTS["Other"])
    return f'<div class="item-thumb item-thumb-emoji" style="background:{gradient}">{emoji}</div>'
