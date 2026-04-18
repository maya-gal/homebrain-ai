"""
demo_data.py — Mock data for Demo Mode (no API key needed).
Also seeds usage_log to demo the Smart Predictions feature.
"""

from datetime import date, timedelta

# ── Receipt Analysis Mock ─────────────────────────────────────

MOCK_RECEIPT_RESPONSE = {
    "store_name": "Whole Foods Market",
    "purchase_date": "2026-04-16",
    "currency": "USD",
    "total_amount": 67.43,
    "items": [
        {"product_name": "Organic Whole Milk",       "category": "Dairy",         "quantity": "1 gallon",    "unit_price": 5.99,  "shelf_life_days": 10, "confidence": "high"},
        {"product_name": "Free Range Eggs",           "category": "Dairy",         "quantity": "12 count",    "unit_price": 4.49,  "shelf_life_days": 28, "confidence": "high"},
        {"product_name": "Baby Spinach",              "category": "Produce",       "quantity": "5 oz bag",    "unit_price": 3.99,  "shelf_life_days": 5,  "confidence": "high"},
        {"product_name": "Roma Tomatoes",             "category": "Produce",       "quantity": "4 count",     "unit_price": 2.49,  "shelf_life_days": 6,  "confidence": "high"},
        {"product_name": "Boneless Chicken Breast",  "category": "Meat & Fish",   "quantity": "1.5 lbs",     "unit_price": 9.99,  "shelf_life_days": 2,  "confidence": "high"},
        {"product_name": "Atlantic Salmon Fillet",   "category": "Meat & Fish",   "quantity": "0.75 lbs",    "unit_price": 11.49, "shelf_life_days": 2,  "confidence": "high"},
        {"product_name": "Sourdough Bread",          "category": "Bakery",        "quantity": "1 loaf",      "unit_price": 4.99,  "shelf_life_days": 4,  "confidence": "high"},
        {"product_name": "Greek Yogurt",             "category": "Dairy",         "quantity": "32 oz",       "unit_price": 6.49,  "shelf_life_days": 14, "confidence": "high"},
        {"product_name": "Penne Pasta",              "category": "מזווה",        "quantity": "16 oz",       "unit_price": 2.29,  "shelf_life_days": 365,"confidence": "high"},
        {"product_name": "Crushed Tomatoes",         "category": "מזווה",        "quantity": "28 oz can",   "unit_price": 2.99,  "shelf_life_days": 730,"confidence": "high"},
        {"product_name": "Frozen Peas",              "category": "Frozen",        "quantity": "16 oz bag",   "unit_price": 2.79,  "shelf_life_days": 180,"confidence": "high"},
        {"product_name": "Orange Juice",             "category": "Beverages",     "quantity": "52 oz",       "unit_price": 5.49,  "shelf_life_days": 10, "confidence": "high"},
        {"product_name": "Avocado",                  "category": "Produce",       "quantity": "2 count",     "unit_price": 2.99,  "shelf_life_days": 3,  "confidence": "high"},
        {"product_name": "Cheddar Cheese",           "category": "Dairy",         "quantity": "8 oz block",  "unit_price": 5.49,  "shelf_life_days": 21, "confidence": "high"},
    ],
}


# ── Meal Planner Mock ─────────────────────────────────────────

MOCK_RECIPES = [
    {
        "name": "Pan-Seared Chicken with Spinach & Tomato",
        "uses_ingredients": ["Boneless Chicken Breast", "Baby Spinach", "Roma Tomatoes"],
        "prep_time_minutes": 20,
        "instructions": [
            "Season chicken breasts with salt, pepper, and garlic powder.",
            "Heat 2 tbsp olive oil in a skillet over medium-high heat.",
            "Sear chicken 6–7 min per side until golden. Remove and rest.",
            "In the same pan, sauté halved tomatoes 2 min, add spinach, wilt 1 min.",
            "Slice chicken, serve over the spinach and tomato mixture.",
        ],
        "tip": "Deglaze the pan with a splash of lemon juice before adding vegetables for extra brightness.",
    },
    {
        "name": "Salmon & Avocado Power Bowl",
        "uses_ingredients": ["Atlantic Salmon Fillet", "Avocado", "Baby Spinach"],
        "prep_time_minutes": 15,
        "instructions": [
            "Season salmon with salt, pepper, and a drizzle of olive oil.",
            "Cook skin-side down in a hot pan for 4 min, flip for 2 more min.",
            "Slice avocado and arrange over a bed of fresh baby spinach.",
            "Flake the salmon on top and drizzle with soy sauce and sesame oil.",
            "Finish with a squeeze of lime juice.",
        ],
        "tip": "The salmon is done when it flakes easily and the centre is just barely opaque.",
    },
]


# ── Usage Log Seed (for Smart Predictions demo) ───────────────

def get_usage_log_seed() -> list[dict]:
    """
    Returns mock purchase history entries to seed the usage_log table.
    This lets the Smart Predictions feature show results immediately in demo mode.
    Each entry simulates an item bought in the past at realistic intervals.
    """
    today = date.today()

    def past(days: int) -> str:
        return (today - timedelta(days=days)).isoformat()

    return [
        # Milk — bought every ~10 days, last bought 9 days ago → due soon
        {"product_name": "Organic Whole Milk",  "category": "Dairy",     "action": "bought", "action_date": past(30)},
        {"product_name": "Organic Whole Milk",  "category": "Dairy",     "action": "bought", "action_date": past(20)},
        {"product_name": "Organic Whole Milk",  "category": "Dairy",     "action": "bought", "action_date": past(9)},

        # Eggs — bought every ~14 days, last bought 12 days ago → due soon
        {"product_name": "Free Range Eggs",     "category": "Dairy",     "action": "bought", "action_date": past(42)},
        {"product_name": "Free Range Eggs",     "category": "Dairy",     "action": "bought", "action_date": past(28)},
        {"product_name": "Free Range Eggs",     "category": "Dairy",     "action": "bought", "action_date": past(12)},

        # Bread — bought every ~5 days, last bought 5 days ago → overdue
        {"product_name": "Sourdough Bread",     "category": "Bakery",    "action": "bought", "action_date": past(15)},
        {"product_name": "Sourdough Bread",     "category": "Bakery",    "action": "bought", "action_date": past(10)},
        {"product_name": "Sourdough Bread",     "category": "Bakery",    "action": "bought", "action_date": past(5)},

        # OJ — bought every ~10 days, last bought 11 days ago → overdue
        {"product_name": "Orange Juice",        "category": "Beverages", "action": "bought", "action_date": past(32)},
        {"product_name": "Orange Juice",        "category": "Beverages", "action": "bought", "action_date": past(21)},
        {"product_name": "Orange Juice",        "category": "Beverages", "action": "bought", "action_date": past(11)},

        # Bananas — not in current receipt, bought every ~7 days, last 8 days ago
        {"product_name": "Bananas",             "category": "Produce",   "action": "bought", "action_date": past(22)},
        {"product_name": "Bananas",             "category": "Produce",   "action": "bought", "action_date": past(15)},
        {"product_name": "Bananas",             "category": "Produce",   "action": "bought", "action_date": past(8)},

        # Dish Soap — bought every ~30 days, last 28 days ago
        {"product_name": "Dish Soap",           "category": "Household", "action": "bought", "action_date": past(90)},
        {"product_name": "Dish Soap",           "category": "Household", "action": "bought", "action_date": past(60)},
        {"product_name": "Dish Soap",           "category": "Household", "action": "bought", "action_date": past(28)},
    ]


MOCK_VOICE_TEXT_ITEMS = [
    {"product_name": "Almond Milk",        "category": "Dairy",    "quantity": "1 liter",  "shelf_life_days": 10, "confidence": "high"},
    {"product_name": "Whole Wheat Bread",  "category": "Bakery",   "quantity": "1 loaf",   "shelf_life_days": 5,  "confidence": "high"},
    {"product_name": "Banana",             "category": "Produce",  "quantity": "6 count",  "shelf_life_days": 4,  "confidence": "high"},
    {"product_name": "Natural Yogurt",     "category": "Dairy",    "quantity": "500g",     "shelf_life_days": 12, "confidence": "high"},
    {"product_name": "Cherry Tomatoes",    "category": "Produce",  "quantity": "250g",     "shelf_life_days": 5,  "confidence": "high"},
]


def seed_usage_log(conn) -> None:
    """Insert demo usage log entries if the table is empty."""
    count = conn.execute("SELECT COUNT(*) FROM usage_log").fetchone()[0]
    if count == 0:
        for entry in get_usage_log_seed():
            conn.execute(
                "INSERT INTO usage_log (product_name, category, action, action_date) VALUES (?,?,?,?)",
                (entry["product_name"], entry["category"], entry["action"], entry["action_date"]),
            )
        conn.commit()
