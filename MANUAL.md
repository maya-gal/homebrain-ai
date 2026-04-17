# HomeBrain AI — Full User & Developer Manual

> **Version:** 1.0 MVP | **Stack:** Python · Streamlit · OpenAI GPT-4o · SQLite

---

## Table of Contents

1. [What Is HomeBrain AI?](#1-what-is-homebrain-ai)
2. [System Architecture](#2-system-architecture)
3. [File Structure](#3-file-structure)
4. [Prerequisites & Installation](#4-prerequisites--installation)
5. [Configuration (API Key)](#5-configuration-api-key)
6. [Running the App](#6-running-the-app)
7. [Feature Guide — Page by Page](#7-feature-guide--page-by-page)
   - 7.1 Sidebar
   - 7.2 Scan Receipt
   - 7.3 Family Dashboard
   - 7.4 Chaos Meal Planner
   - 7.5 Running Low
8. [The AI System Prompts — Deep Dive](#8-the-ai-system-prompts--deep-dive)
9. [Database Schema](#9-database-schema)
10. [Data Flow Diagram](#10-data-flow-diagram)
11. [Key Design Decisions](#11-key-design-decisions)
12. [Troubleshooting](#12-troubleshooting)
13. [How to Extend the MVP](#13-how-to-extend-the-mvp)

---

## 1. What Is HomeBrain AI?

HomeBrain AI is a household inventory management application.  
Its core promise: **upload a grocery receipt → your family pantry is automatically updated.**

No manual data entry. No spreadsheets. Just a photo.

The "Happy Path":
```
User uploads receipt image
       ↓
GPT-4o Vision reads the receipt
       ↓
Structured JSON: product, category, quantity, shelf life
       ↓
SQLite database stores the inventory
       ↓
Dashboard shows family pantry in real time
       ↓
AI detects expiring items → suggests dinner recipes
```

---

## 2. System Architecture

```
┌─────────────────────────────────────────────┐
│              Streamlit UI (app.py)           │
│  ┌──────────┐ ┌──────────┐ ┌─────────────┐  │
│  │  Scan    │ │Dashboard │ │Meal Planner │  │
│  │ Receipt  │ │          │ │             │  │
│  └────┬─────┘ └────┬─────┘ └──────┬──────┘  │
└───────┼────────────┼──────────────┼──────────┘
        │            │              │
        ▼            ▼              ▼
   vision.py    database.py     planner.py
        │            │              │
        ▼            │              ▼
   OpenAI API    SQLite DB     OpenAI API
  (GPT-4o Vision)  homebrain.db  (GPT-4o Text)
```

**Layers:**
- **UI Layer** — `app.py` only. No business logic here.
- **AI Layer** — `vision.py` (receipt) + `planner.py` (meals). Pure functions.
- **Data Layer** — `database.py`. Single source of truth, no leakage to UI.

---

## 3. File Structure

```
📁 project root/
├── app.py            ← Streamlit app, routing, UI components
├── vision.py         ← GPT-4o Vision: receipt → JSON
├── database.py       ← SQLite CRUD: store, query, enrich items
├── planner.py        ← GPT-4o Text: expiring items → recipes
├── requirements.txt  ← Python dependencies (5 packages)
├── .env              ← Your API key (you create this)
├── .env.example      ← Template for .env
├── MANUAL.md         ← This file
└── homebrain.db      ← Auto-created on first run (SQLite)
```

---

## 4. Prerequisites & Installation

### Step 1 — Install Python

Download Python **3.11 or higher** from:  
https://www.python.org/downloads/

> ✅ During installation, check **"Add Python to PATH"**

Verify:
```bash
python --version
# Expected: Python 3.11.x or higher
```

### Step 2 — Clone / Open the Project

Open a terminal in the project folder:
```bash
cd "C:\Users\User\OneDrive\claude code 1st project"
```

### Step 3 — (Recommended) Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:

| Package | Version | Purpose |
|---------|---------|---------|
| `streamlit` | ≥1.35 | Web UI framework |
| `openai` | ≥1.30 | GPT-4o API client |
| `pandas` | ≥2.0 | Table display & manipulation |
| `python-dotenv` | ≥1.0 | Load API key from .env |
| `Pillow` | ≥10.0 | Image handling |

---

## 5. Configuration (API Key)

### Get an OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Click **"Create new secret key"**
3. Copy the key (starts with `sk-...`)
4. Make sure your account has **GPT-4o access**

### Set Up Your .env File

In the project root, create a file named `.env`:

```bash
# Windows (Command Prompt)
copy .env.example .env
notepad .env
```

Edit `.env` to contain:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

> ⚠️ Never share this file or commit it to git.

---

## 6. Running the App

```bash
streamlit run app.py
```

Expected output:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

The browser opens automatically at `http://localhost:8501`.

To stop the server: press `Ctrl + C` in the terminal.

---

## 7. Feature Guide — Page by Page

### 7.1 Sidebar (always visible)

| Element | Description |
|---------|-------------|
| 🏠 HomeBrain AI | App brand + tagline |
| Navigation | Radio buttons to switch between 4 pages |
| 👤 Adding as | Simulates multi-user: You / Mom / Dad / Kids |
| Pantry at a glance | Live counts: total items, expiring items, categories |

The "Adding as" selector attaches a **Created By** label to every item saved in that session.

---

### 7.2 📸 Scan Receipt

**Purpose:** Upload a grocery receipt → extract inventory automatically.

**Step-by-step:**

1. Click **"Browse files"** or drag-and-drop a receipt image (JPG, PNG, WEBP).
2. The image appears on the left. GPT-4o Vision analyzes it (takes ~5–10 seconds).
3. Three metadata chips show: store name, purchase date, total amount.
4. A **data editor table** shows all extracted items — you can edit any cell before saving.
5. Click **"✅ Save to Pantry"** to write to the database.

**What GPT-4o extracts per item:**

| Field | Example |
|-------|---------|
| Product Name | "Whole Milk" |
| Category | "Dairy" |
| Quantity | "1 gallon" |
| Shelf Life (days) | 10 |
| Confidence | "high" / "medium" / "low" |

**Zero-entry design:** The user never types anything. The only interaction is upload → review → save.

---

### 7.3 🏠 Family Dashboard

**Purpose:** See everything in your household pantry.

**Elements:**

- **Search bar** — Type any word (e.g. "milk", "frozen") to filter in real time.
- **4 metric cards** — Total / Fresh / Running Low / Expired counts.
- **Colour-coded table:**

| Colour | Status | Meaning |
|--------|--------|---------|
| 🟢 Green | Fresh | >5 days remaining |
| 🟡 Yellow | Use Soon | 3–5 days remaining |
| 🟠 Orange | Running Low | 1–2 days remaining |
| 🔴 Red | Expired | 0 days remaining |

- **Category Breakdown chart** — expandable bar chart showing distribution across categories.
- **Added By column** — shows which family member added each item.

---

### 7.4 🍳 Chaos Meal Planner

**Purpose:** Turn expiring ingredients into tonight's dinner — no waste.

**How it works:**

1. The app automatically finds items expiring within the next **5 days**.
2. It shows them as "pills" so you know what's at stake.
3. Click **"✨ Generate Meal Ideas"**.
4. GPT-4o suggests **2 complete recipes** that use those ingredients.

**Each recipe includes:**
- Recipe name
- Which pantry items it uses
- Step-by-step instructions
- Prep time in minutes
- One chef's tip

**If nothing is expiring:** A success message confirms your pantry is in good shape.

---

### 7.5 ⚠️ Running Low

**Purpose:** Urgent alert view — items with ≤2 days remaining.

**How days_remaining is calculated:**
```
days_remaining = shelf_life_days - (today - added_date)
```

This is computed fresh every time the page loads — never stored in the DB, so it's always accurate.

**Actions:**
- Each item shows: name, category, quantity, days left, who added it, from which store.
- Click **"🗑 Remove"** to delete an item after you've used or discarded it.
- The page auto-refreshes after deletion.

---

## 8. The AI System Prompts — Deep Dive

### Receipt Prompt (vision.py)

The prompt is the contract between the app and GPT-4o.  
Key design choices:

**1. Shelf Life Rules (baked into the prompt)**
```
- Fresh produce: 3–7 days
- Dairy: 7–14 days
- Meat & Fish (fresh): 1–3 days
- Bakery: 3–5 days
- Frozen: 60–180 days
- Canned: 365–730 days
- Dry pantry: 180–365 days
```
These rules live in the prompt, not in Python code. This means you can tune shelf life estimates without changing any code — just edit the prompt.

**2. Fixed Category Taxonomy**
```
Produce | Dairy | Meat & Fish | Bakery | Frozen |
Pantry | Beverages | Snacks | Household | Personal Care | Other
```
By giving GPT-4o a closed list of categories, the DB data stays consistent and filterable.

**3. `response_format: json_object` + `temperature: 0.1`**
- `json_object` mode: OpenAI enforces valid JSON at the API level — no partial responses.
- `temperature: 0.1`: Near-deterministic output. The same receipt should always produce the same items.

**4. Confidence field**
Every item gets `"confidence": "high" | "medium" | "low"`.  
Low-confidence items are still extracted — the user can review and correct them in the editable table.

---

### Meal Planner Prompt (planner.py)

Different job, different settings:

- **`temperature: 0.7`** — Creativity is wanted here. Each click should produce different recipes.
- The prompt lists ingredient names + days remaining, so GPT-4o knows which items to prioritize.
- "You may assume the family has common pantry staples" — prevents recipes like "chicken + salt" being rejected because salt wasn't on the receipt.

---

## 9. Database Schema

File: `homebrain.db` (SQLite, auto-created on first run)

```sql
CREATE TABLE inventory (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name    TEXT    NOT NULL,
    category        TEXT    NOT NULL DEFAULT 'Other',
    quantity        TEXT    NOT NULL DEFAULT '1',
    unit_price      REAL,                          -- nullable
    shelf_life_days INTEGER NOT NULL DEFAULT 7,
    added_by        TEXT    NOT NULL DEFAULT 'You',
    added_date      TEXT    NOT NULL,              -- ISO date: 2025-06-01
    store_name      TEXT,                          -- nullable
    confidence      TEXT    DEFAULT 'high'
);
```

**Computed fields (not stored):**

| Field | Computed as |
|-------|-------------|
| `days_remaining` | `shelf_life_days - (today - added_date)` |
| `status` | `Fresh / Use Soon / Running Low / Expired` based on `days_remaining` |

These are added in `database.py → _enrich()` at read time. Storing them would make them go stale.

---

## 10. Data Flow Diagram

```
┌─────────────┐
│ User uploads│
│ receipt.jpg │
└──────┬──────┘
       │ image bytes
       ▼
┌─────────────────────────────┐
│  vision.analyze_receipt()   │
│                             │
│  1. base64 encode image     │
│  2. POST to OpenAI API      │
│     model: gpt-4o           │
│     response_format: json   │
│  3. parse + return dict     │
└──────────────┬──────────────┘
               │ {"items": [...], "store_name": "...", ...}
               ▼
┌─────────────────────────────┐
│  Streamlit data_editor      │
│  (user reviews & edits)     │
└──────────────┬──────────────┘
               │ confirmed items list
               ▼
┌─────────────────────────────┐
│  database.insert_items()    │
│  → SQLite homebrain.db      │
└──────────────┬──────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
 get_all_items()   get_expiring_items()
 → Dashboard       → Meal Planner + Running Low
```

---

## 11. Key Design Decisions

### Why SQLite and not Airtable?
Zero configuration. No API key. Single file you can inspect with any DB browser.  
Swapping to Airtable: replace `_conn()` in `database.py` with an Airtable API call. The rest of the code doesn't change.

### Why are `days_remaining` and `status` computed at read time, not stored?
If they were stored columns, they'd be correct the moment of insert and wrong every day after.  
Computing from `added_date + shelf_life_days` is always accurate, costs one subtraction.

### Why `temperature: 0.1` for receipts but `0.7` for recipes?
Receipt parsing is structured extraction — variance is a bug.  
Recipe generation benefits from novelty — variance is the feature.

### Why `response_format: json_object`?
OpenAI enforces valid JSON at the API layer. Without it, the model might wrap its response in markdown code fences (```json ... ```) which would break `json.loads()`. The additional regex strip in `_extract_json()` is a safety net.

### Why is the OpenAI client cached with `@st.cache_resource`?
Streamlit reruns the entire script on every user interaction. Without caching, a new `OpenAI()` client would be instantiated on every click, wasting memory and re-reading the `.env` file repeatedly.

### Why `row_factory = sqlite3.Row`?
Returns rows as dict-like objects instead of plain tuples, so `row["product_name"]` works instead of `row[1]`. Makes the code self-documenting.

---

## 12. Troubleshooting

### "Set OPENAI_API_KEY" error on startup
- Make sure `.env` exists in the project root (not `.env.example`)
- File must contain: `OPENAI_API_KEY=sk-...`
- Restart the terminal after creating the file

### Analysis failed / JSON parse error
- Receipt image may be too blurry or low resolution
- Try a clearer photo with good lighting
- Check that your OpenAI account has GPT-4o access (not just GPT-3.5)

### "No items found"
- The receipt may be partially cut off
- Non-grocery receipts (hardware store, gas station) may produce fewer items
- GPT-4o needs to see at least part of the itemized list

### Port already in use
```bash
streamlit run app.py --server.port 8502
```

### Database locked error
Close any SQLite browser tools that may have the file open, then restart the app.

### Module not found
Make sure you activated your virtual environment before running:
```bash
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

---

## 13. How to Extend the MVP

### Add real multi-user support
Replace the sidebar dropdown with Streamlit's `st.experimental_user` or integrate a simple login with `streamlit-authenticator`.

### Add push notifications
Use `schedule` + `smtplib` to email the family when items hit "Running Low".

### Replace SQLite with Airtable
In `database.py`, replace `_conn()` with:
```python
from pyairtable import Table
def _table():
    return Table(os.getenv("AIRTABLE_TOKEN"), os.getenv("BASE_ID"), "inventory")
```
Then map the CRUD functions to Airtable's `.all()`, `.create()`, `.delete()`.

### Add barcode scanning
Use the `pyzbar` library to scan barcodes from images, then look up the product via the Open Food Facts API — zero-prompt product lookup.

### Add shopping list generation
A new page that reads items with `days_remaining == 0` (expired) and generates a shopping list, optionally ordered by supermarket aisle.

### Deploy to the cloud
```bash
# Streamlit Community Cloud (free)
# 1. Push to GitHub
# 2. Go to share.streamlit.io
# 3. Connect repo, set OPENAI_API_KEY in Secrets
```

---

## Quick Reference Card

```
Start app:        streamlit run app.py
Stop app:         Ctrl + C
DB file:          homebrain.db (project root)
API key:          .env → OPENAI_API_KEY=sk-...
Add item:         Scan Receipt → upload → Save to Pantry
Search pantry:    Family Dashboard → search bar
Get recipes:      Meal Planner → Generate Meal Ideas
Clear expired:    Running Low → 🗑 Remove
```

---

*HomeBrain AI MVP — Built for Wix application demo*
