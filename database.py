"""
database.py — SQLite inventory store.
Tables: inventory, shopping_list, usage_log
"""

import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional
from collections import defaultdict

DB_PATH = Path("homebrain.db")


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name    TEXT    NOT NULL,
                category        TEXT    NOT NULL DEFAULT 'Other',
                quantity        TEXT    NOT NULL DEFAULT '1',
                unit_price      REAL,
                shelf_life_days INTEGER NOT NULL DEFAULT 7,
                added_by        TEXT    NOT NULL DEFAULT 'You',
                added_date      TEXT    NOT NULL,
                store_name      TEXT,
                confidence      TEXT    DEFAULT 'high'
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS shopping_list (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name  TEXT    NOT NULL,
                category   TEXT    DEFAULT 'Other',
                quantity   TEXT    DEFAULT '1',
                is_bought  INTEGER DEFAULT 0,
                added_date TEXT    NOT NULL
            )
        """)
        # usage_log: records every time an item is marked "used" or removed
        # powers the "smart predictions" / learning inventory manager feature
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usage_log (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                category     TEXT NOT NULL DEFAULT 'Other',
                action       TEXT NOT NULL DEFAULT 'used',  -- 'used' | 'expired' | 'bought'
                action_date  TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS staple_list (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT    NOT NULL,
                category     TEXT    DEFAULT 'Other',
                UNIQUE(product_name COLLATE NOCASE)
            )
        """)
        conn.commit()


# ── Inventory ────────────────────────────────────────────────

def insert_items(items: list[dict], added_by: str, store_name: Optional[str]) -> int:
    today = date.today().isoformat()
    rows = [
        (
            item["product_name"], item["category"], item["quantity"],
            item.get("unit_price"), item["shelf_life_days"],
            added_by, today, store_name, item.get("confidence", "high"),
        )
        for item in items
    ]
    with _conn() as conn:
        conn.executemany(
            """INSERT INTO inventory
               (product_name, category, quantity, unit_price,
                shelf_life_days, added_by, added_date, store_name, confidence)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            rows,
        )
        # Log every purchase
        conn.executemany(
            "INSERT INTO usage_log (product_name, category, action, action_date) VALUES (?,?,'bought',?)",
            [(item["product_name"], item["category"], today) for item in items],
        )
        conn.commit()
    return len(rows)


def get_all_items() -> list[dict]:
    with _conn() as conn:
        rows = conn.execute("SELECT * FROM inventory ORDER BY added_date DESC").fetchall()
    return [_enrich(dict(r)) for r in rows]


def search_items(query: str, category: str = "") -> list[dict]:
    pattern = f"%{query}%"
    with _conn() as conn:
        if category and category != "All":
            rows = conn.execute(
                """SELECT * FROM inventory
                   WHERE (product_name LIKE ? OR category LIKE ?)
                   AND category = ?
                   ORDER BY added_date DESC""",
                (pattern, pattern, category),
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT * FROM inventory
                   WHERE product_name LIKE ? OR category LIKE ?
                   ORDER BY added_date DESC""",
                (pattern, pattern),
            ).fetchall()
    return [_enrich(dict(r)) for r in rows]


def get_expiring_items(within_days: int = 3) -> list[dict]:
    return [i for i in get_all_items() if 0 < i["days_remaining"] <= within_days]


def get_categories() -> list[str]:
    with _conn() as conn:
        rows = conn.execute("SELECT DISTINCT category FROM inventory ORDER BY category").fetchall()
    return [r["category"] for r in rows]


def update_item(item_id: int, quantity: str = None, shelf_life_days: int = None) -> None:
    parts, vals = [], []
    if quantity is not None:
        parts.append("quantity = ?"); vals.append(quantity)
    if shelf_life_days is not None:
        parts.append("shelf_life_days = ?"); vals.append(shelf_life_days)
    if not parts:
        return
    vals.append(item_id)
    with _conn() as conn:
        conn.execute(f"UPDATE inventory SET {', '.join(parts)} WHERE id = ?", vals)
        conn.commit()


def delete_item(item_id: int, reason: str = "used") -> None:
    with _conn() as conn:
        row = conn.execute("SELECT product_name, category FROM inventory WHERE id=?", (item_id,)).fetchone()
        if row:
            conn.execute(
                "INSERT INTO usage_log (product_name, category, action, action_date) VALUES (?,?,?,?)",
                (row["product_name"], row["category"], reason, date.today().isoformat()),
            )
        conn.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
        conn.commit()


def get_stats() -> dict:
    items = get_all_items()
    if not items:
        return {"total": 0, "expiring_soon": 0, "categories": 0, "expired": 0, "fresh": 0}
    return {
        "total":         len(items),
        "expiring_soon": sum(1 for i in items if i["status"] == "Running Low"),
        "expired":       sum(1 for i in items if i["status"] == "Expired"),
        "fresh":         sum(1 for i in items if i["status"] == "Fresh"),
        "categories":    len({i["category"] for i in items}),
    }


# ── Shopping List ─────────────────────────────────────────────

_CATEGORY_PRICE_DEFAULTS: dict[str, float] = {
    "Produce": 3.50, "Dairy": 4.00, "Meat & Fish": 8.00, "Bakery": 3.50,
    "Frozen": 5.00, "Pantry": 4.00, "Beverages": 3.00, "Snacks": 4.50,
    "Household": 6.00, "Personal Care": 7.00, "Other": 4.00,
}


def get_price_estimates(shopping_items: list[dict]) -> dict[str, float]:
    """Return {item_name.lower(): estimated_price} using past unit_price or category default."""
    estimates: dict[str, float] = {}
    with _conn() as conn:
        for item in shopping_items:
            name = item["item_name"]
            row = conn.execute(
                "SELECT AVG(unit_price) as avg_p FROM inventory "
                "WHERE LOWER(product_name)=LOWER(?) AND unit_price IS NOT NULL",
                (name,),
            ).fetchone()
            if row and row["avg_p"]:
                estimates[name.lower()] = round(row["avg_p"], 2)
            else:
                estimates[name.lower()] = _CATEGORY_PRICE_DEFAULTS.get(
                    item.get("category", "Other"), 4.00
                )
    return estimates


def get_shopping_list() -> list[dict]:
    with _conn() as conn:
        rows = conn.execute(
            "SELECT * FROM shopping_list ORDER BY is_bought ASC, added_date DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def add_to_shopping_list(item_name: str, category: str = "Other", quantity: str = "1") -> None:
    with _conn() as conn:
        # Avoid duplicates (same name not yet bought)
        exists = conn.execute(
            "SELECT id FROM shopping_list WHERE item_name=? AND is_bought=0",
            (item_name,),
        ).fetchone()
        if not exists:
            conn.execute(
                "INSERT INTO shopping_list (item_name, category, quantity, added_date) VALUES (?,?,?,?)",
                (item_name, category, quantity, date.today().isoformat()),
            )
            conn.commit()


def mark_bought(item_id: int) -> None:
    with _conn() as conn:
        conn.execute("UPDATE shopping_list SET is_bought=1 WHERE id=?", (item_id,))
        conn.commit()


def unmark_bought(item_id: int) -> None:
    with _conn() as conn:
        conn.execute("UPDATE shopping_list SET is_bought=0 WHERE id=?", (item_id,))
        conn.commit()


def clear_bought() -> None:
    with _conn() as conn:
        conn.execute("DELETE FROM shopping_list WHERE is_bought=1")
        conn.commit()


def auto_populate_shopping_list() -> int:
    """Add all expired/running-low items to shopping list. Returns count added."""
    urgent = [i for i in get_all_items() if i["days_remaining"] <= 2]
    added = 0
    for item in urgent:
        with _conn() as conn:
            exists = conn.execute(
                "SELECT id FROM shopping_list WHERE item_name=? AND is_bought=0",
                (item["product_name"],),
            ).fetchone()
            if not exists:
                conn.execute(
                    "INSERT INTO shopping_list (item_name, category, quantity, added_date) VALUES (?,?,?,?)",
                    (item["product_name"], item["category"], item["quantity"], date.today().isoformat()),
                )
                conn.commit()
                added += 1
    return added


# ── Smart Predictions (usage_log analysis) ───────────────────

def get_smart_predictions() -> list[dict]:
    """
    Analyse purchase history to predict items that are running low
    even if they aren't in the current inventory.

    Logic:
    - For each product ever bought, compute average days between purchases.
    - If (today - last_bought_date) > avg_gap * 0.8 → flag as "likely needed".
    - Only surfaces items NOT currently in inventory.
    """
    with _conn() as conn:
        buys = conn.execute(
            "SELECT product_name, category, action_date FROM usage_log WHERE action='bought' ORDER BY action_date ASC"
        ).fetchall()

    current_names = {i["product_name"].lower() for i in get_all_items()}

    # Group purchase dates per product
    by_product: dict[str, list[date]] = defaultdict(list)
    categories: dict[str, str] = {}
    for row in buys:
        name = row["product_name"]
        try:
            d = date.fromisoformat(row["action_date"])
        except ValueError:
            continue
        by_product[name].append(d)
        categories[name] = row["category"]

    predictions = []
    today = date.today()

    for name, dates in by_product.items():
        if name.lower() in current_names:
            continue  # Already in pantry
        if len(dates) < 2:
            continue  # Need at least 2 purchases to compute gap

        dates_sorted = sorted(dates)
        gaps = [(dates_sorted[i+1] - dates_sorted[i]).days for i in range(len(dates_sorted)-1)]
        avg_gap = sum(gaps) / len(gaps)

        last_bought = dates_sorted[-1]
        days_since = (today - last_bought).days

        if avg_gap > 0 and days_since >= avg_gap * 0.8:
            urgency = "High" if days_since >= avg_gap else "Medium"
            predictions.append({
                "product_name": name,
                "category":     categories.get(name, "Other"),
                "avg_gap_days": round(avg_gap),
                "days_since_last": days_since,
                "urgency":      urgency,
            })

    # Sort: high urgency first, then most overdue
    predictions.sort(key=lambda x: (x["urgency"] != "High", -x["days_since_last"]))
    return predictions[:8]  # Cap at 8 predictions


def get_inventory_predictions() -> dict[str, str]:
    """Returns {product_name.lower(): prediction_text} for items currently in inventory.
    Shows shelf-life countdown and purchase-frequency hint when history is available."""
    items = get_all_items()
    if not items:
        return {}

    with _conn() as conn:
        buys = conn.execute(
            "SELECT product_name, action_date FROM usage_log WHERE action='bought' ORDER BY action_date ASC"
        ).fetchall()

    by_product: dict[str, list[date]] = defaultdict(list)
    for row in buys:
        try:
            d = date.fromisoformat(row["action_date"])
            by_product[row["product_name"].lower()].append(d)
        except ValueError:
            continue

    predictions: dict[str, str] = {}
    for item in items:
        name_lower = item["product_name"].lower()
        days = item["days_remaining"]

        parts = []
        if days <= 0:
            parts.append("Expired")
        elif days <= 5:
            unit = "day" if days == 1 else "days"
            parts.append(f"Runs out in {days} {unit}")

        dates = sorted(by_product.get(name_lower, []))
        if len(dates) >= 2:
            gaps = [(dates[i + 1] - dates[i]).days for i in range(len(dates) - 1)]
            avg_gap = round(sum(gaps) / len(gaps))
            if avg_gap > 0:
                parts.append(f"you buy every ~{avg_gap}d")

        if parts:
            predictions[name_lower] = " · ".join(parts)

    return predictions


# ── Staple List ───────────────────────────────────────────────

def get_staple_list() -> list[dict]:
    with _conn() as conn:
        rows = conn.execute("SELECT * FROM staple_list ORDER BY category, product_name").fetchall()
    return [dict(r) for r in rows]


def add_staple(product_name: str, category: str = "Other") -> bool:
    """Returns True if added, False if already exists."""
    try:
        with _conn() as conn:
            conn.execute(
                "INSERT INTO staple_list (product_name, category) VALUES (?,?)",
                (product_name.strip(), category),
            )
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def remove_staple(staple_id: int) -> None:
    with _conn() as conn:
        conn.execute("DELETE FROM staple_list WHERE id=?", (staple_id,))
        conn.commit()


def get_missing_staples() -> list[dict]:
    """Return staples that are not currently in the pantry (or all expired)."""
    staples = get_staple_list()
    if not staples:
        return []
    inventory = get_all_items()
    # Items that are present and not expired
    in_stock = {i["product_name"].lower() for i in inventory if i["days_remaining"] > 0}
    return [s for s in staples if s["product_name"].lower() not in in_stock]


# ── Internal helpers ──────────────────────────────────────────

def _enrich(item: dict) -> dict:
    try:
        added = date.fromisoformat(item["added_date"])
        elapsed = (date.today() - added).days
        item["days_remaining"] = max(0, item["shelf_life_days"] - elapsed)
    except (ValueError, TypeError):
        item["days_remaining"] = item["shelf_life_days"]

    dr = item["days_remaining"]
    sl = item.get("shelf_life_days", 1) or 1
    item["shelf_pct"] = min(100, round(dr / sl * 100))

    if dr == 0:
        item["status"] = "Expired"
    elif dr <= 2:
        item["status"] = "Running Low"
    elif dr <= 5:
        item["status"] = "Use Soon"
    else:
        item["status"] = "Fresh"

    return item
