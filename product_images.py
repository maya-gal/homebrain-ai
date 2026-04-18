"""
product_images.py — Maps product names and categories to food photo URLs.
Uses Spoonacular's free ingredient CDN (no API key needed).
"""

_BASE = "https://spoonacular.com/cdn/ingredients_100x100/"

# ── Per-product overrides (keyword → filename) ────────────────
_PRODUCT_MAP: dict[str, str] = {
    # Dairy
    "milk":         "milk.jpg",
    "whole milk":   "milk.jpg",
    "eggs":         "egg.jpg",
    "egg":          "egg.jpg",
    "yogurt":       "plain-yogurt.jpg",
    "greek yogurt": "plain-yogurt.jpg",
    "cheddar":      "cheddar-cheese.jpg",
    "cheese":       "cheddar-cheese.jpg",
    "butter":       "butter.jpg",
    "cream":        "heavy-cream.jpg",
    "sour cream":   "sour-cream.jpg",
    # Produce
    "sweet potato":  "sweet-potato.jpg",
    "sweet potatoes":"sweet-potato.jpg",
    "yam":           "sweet-potato.jpg",
    "corn":          "corn.jpg",
    "celery":        "celery.jpg",
    "cabbage":       "cabbage.jpg",
    "eggplant":      "eggplant.jpg",
    "cauliflower":   "cauliflower.jpg",
    "asparagus":     "asparagus.jpg",
    "blueberry":     "blueberries.jpg",
    "blueberries":   "blueberries.jpg",
    "grapes":        "grapes.jpg",
    "watermelon":    "watermelon.jpg",
    "pineapple":     "pineapple.jpg",
    "mango":         "mango.jpg",
    "peach":         "peach.jpg",
    "pear":          "pear.jpg",
    "spinach":      "spinach.jpg",
    "baby spinach": "spinach.jpg",
    "tomato":       "tomato.jpg",
    "tomatoes":     "tomatoes.jpg",
    "roma tomato":  "tomatoes.jpg",
    "cherry tomato":"cherry-tomatoes.jpg",
    "avocado":      "avocado.jpg",
    "banana":       "bananas.jpg",
    "bananas":      "bananas.jpg",
    "carrot":       "carrots.jpg",
    "carrots":      "carrots.jpg",
    "onion":        "white-onion.jpg",
    "garlic":       "garlic.jpg",
    "potato":       "russet-potatoes.jpg",
    "potatoes":     "russet-potatoes.jpg",
    "lettuce":      "romaine-lettuce.jpg",
    "cucumber":     "cucumber.jpg",
    "bell pepper":  "bell-pepper-red.jpg",
    "lemon":        "lemon.jpg",
    "lime":         "lime.jpg",
    "apple":        "apple.jpg",
    "apples":       "apple.jpg",
    "orange":       "navel-oranges.jpg",
    "strawberry":   "strawberries.jpg",
    "strawberries": "strawberries.jpg",
    "broccoli":     "broccoli.jpg",
    "zucchini":     "zucchini.jpg",
    "mushroom":     "mushrooms.jpg",
    "mushrooms":    "mushrooms.jpg",
    # Meat & Fish
    "chicken":      "chicken-breasts.jpg",
    "chicken breast":"chicken-breasts.jpg",
    "ground beef":  "ground-beef.jpg",
    "beef":         "beef-cubes-raw.jpg",
    "salmon":       "salmon.jpg",
    "tuna":         "canned-tuna.jpg",
    "shrimp":       "shrimp.jpg",
    "turkey":       "turkey-breast.jpg",
    "lamb":         "lamb-chops.jpg",
    # Bakery
    "bread":        "bread.jpg",
    "sourdough":    "bread.jpg",
    "pita":         "pita-bread.jpg",
    "bagel":        "bagel.jpg",
    "croissant":    "croissant.jpg",
    "muffin":       "blueberry-muffins.jpg",
    # Pantry
    "pasta":        "penne-pasta.jpg",
    "penne":        "penne-pasta.jpg",
    "spaghetti":    "spaghetti.jpg",
    "fusilli":      "penne-pasta.jpg",
    "rice":         "uncooked-white-rice.jpg",
    "flour":        "flour.jpg",
    "sugar":        "sugar.jpg",
    "olive oil":    "olive-oil.jpg",
    "salt":         "salt.jpg",
    "pepper":       "pepper.jpg",
    "honey":        "honey.jpg",
    "ketchup":      "ketchup.jpg",
    "mustard":      "dijon-mustard.jpg",
    "crushed tomato":"tomato-sauce.jpg",
    "tomato sauce": "tomato-sauce.jpg",
    "canned tomato":"tomato-sauce.jpg",
    "oats":         "rolled-oats.jpg",
    "cereal":       "granola.jpg",
    # Frozen
    "frozen peas":  "peas.jpg",
    "peas":         "peas.jpg",
    "frozen corn":  "corn.jpg",
    "ice cream":    "vanilla-ice-cream.jpg",
    # Beverages
    "orange juice": "orange-juice.jpg",
    "juice":        "orange-juice.jpg",
    "coffee":       "coffee.jpg",
    "tea":          "tea-bags.jpg",
    "water":        "water.jpg",
    "almond milk":  "almond-milk.jpg",
    "oat milk":     "oat-milk.jpg",
    "soy milk":     "soy-milk.jpg",
    # Snacks
    "chips":        "potato-chips.jpg",
    "crackers":     "crackers.jpg",
    "nuts":         "mixed-nuts.jpg",
    "almonds":      "almonds.jpg",
    "peanut butter":"peanut-butter.jpg",
    "chocolate":    "dark-chocolate.jpg",
    # Condiments / Extra
    "mayonnaise":   "mayonnaise.jpg",
    "vinegar":      "white-wine-vinegar.jpg",
    "soy sauce":    "soy-sauce.jpg",
    "tahini":       "tahini.jpg",
}

# ── Category fallbacks ────────────────────────────────────────
_CATEGORY_MAP: dict[str, str] = {
    "Dairy":        "milk.jpg",
    "Produce":      "mixed-vegetables.jpg",
    "Meat & Fish":  "chicken-breasts.jpg",
    "Bakery":       "bread.jpg",
    "Frozen":       "peas.jpg",
    "Pantry":       "olive-oil.jpg",
    "Beverages":    "orange-juice.jpg",
    "Snacks":       "potato-chips.jpg",
    "Household":    None,
    "Personal Care":None,
    "Other":        None,
}


def get_product_image(product_name: str, category: str = "") -> str | None:
    """
    Return a Spoonacular CDN image URL for the product, or None for non-food items.
    Tries exact match → keyword match → category fallback.
    """
    name_lower = product_name.lower().strip()

    # Exact match
    if name_lower in _PRODUCT_MAP:
        return _BASE + _PRODUCT_MAP[name_lower]

    # Keyword match (longest keyword wins)
    best_key = ""
    for key in _PRODUCT_MAP:
        if key in name_lower and len(key) > len(best_key):
            best_key = key
    if best_key:
        return _BASE + _PRODUCT_MAP[best_key]

    # Category fallback
    filename = _CATEGORY_MAP.get(category)
    return (_BASE + filename) if filename else None
