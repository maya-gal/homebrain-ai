"""
styles.py — HomeBrain AI design system.
Based on Google Stitch warm-brown token set.
"""

def get_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

/* ── Design Tokens (Stitch warm-brown) ───────────────────── */
:root {
  /* Brand */
  --primary:            #8d6e63;
  --primary-dark:       #5d4037;
  --primary-container:  #d7ccc8;
  --on-primary:         #ffffff;
  --on-primary-container: #3e2723;

  /* Secondary */
  --secondary:          #795548;
  --secondary-container:#efebe9;

  /* Tertiary / Urgent */
  --tertiary:           #ad350a;
  --tertiary-light:     rgba(254,111,66,.12);

  /* Semantic */
  --success:            #5a7a52;
  --success-light:      #dff0d8;
  --warning:            #c4903a;
  --warning-light:      #fdf3dc;
  --danger:             #a73b21;
  --danger-light:       #fde8e4;

  /* Surfaces */
  --bg:                 #faf9f8;
  --surface:            #ffffff;
  --surface-low:        #f4f1ed;
  --surface-mid:        #f1eee9;
  --surface-high:       #e9e5e2;
  --surface-highest:    #e4dedd;

  /* Text */
  --text:               #2d3432;
  --text-muted:         #5f5954;
  --outline:            #7c7570;
  --outline-variant:    #b4aca4;

  /* Radius — Stitch bento style */
  --radius:             20px;
  --radius-sm:          12px;
  --radius-xs:          8px;
  --radius-full:        9999px;

  /* Shadow */
  --shadow:    0 1px 4px rgba(45,52,50,.06), 0 1px 2px rgba(45,52,50,.04);
  --shadow-md: 0 4px 16px rgba(45,52,50,.08), 0 2px 4px rgba(45,52,50,.04);
  --shadow-lg: 0 20px 50px rgba(45,52,50,.08);
}

/* ── Base ─────────────────────────────────────────────────── */
html, body, [class*="css"] {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  color: var(--text);
  background-color: var(--bg) !important;
}

h1, h2, h3, .page-title {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, .stDeployButton { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

/* Main content */
.main .block-container {
  padding-top: 2rem;
  padding-bottom: 3rem;
  max-width: 1100px;
  background: var(--bg);
}

/* ── Sidebar ──────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
  background: #2c1f1a !important;
  border-right: none;
}
section[data-testid="stSidebar"] * { color: #c4b5af !important; }

.sidebar-brand {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 1.2rem;
  font-weight: 800;
  color: #fff !important;
  letter-spacing: -0.3px;
}
.sidebar-tagline {
  font-size: 0.75rem;
  color: #7c6560 !important;
  margin-top: 2px;
}

/* Sidebar nav buttons — override Streamlit */
section[data-testid="stSidebar"] .stButton > button {
  border-radius: var(--radius-sm) !important;
  font-weight: 600 !important;
  font-size: 0.85rem !important;
  text-align: left !important;
  transition: background .15s !important;
  background: transparent !important;
  border: none !important;
  color: #a89590 !important;
  padding: 10px 14px !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(255,255,255,.06) !important;
  color: #fff !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
  background: var(--primary) !important;
  color: #fff !important;
}

/* Sidebar stat pills */
.stat-pill {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 10px;
  border-radius: var(--radius-xs);
  margin-bottom: 6px;
  background: rgba(255,255,255,.05);
  font-size: 0.78rem;
}
.stat-pill .label { color: #7c6560 !important; }
.stat-pill .value { font-weight: 700; color: #e2d8d5 !important; }
.stat-pill .value.warn   { color: var(--warning) !important; }
.stat-pill .value.danger { color: #fd795a !important; }

/* ── Page Headers ─────────────────────────────────────────── */
.page-header { margin-bottom: 1.5rem; }
.page-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--primary);
  letter-spacing: -0.5px;
  margin: 0;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.page-sub {
  font-size: 0.875rem;
  color: var(--text-muted);
  margin-top: 4px;
}

/* ── Demo Banner ──────────────────────────────────────────── */
.demo-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--secondary-container);
  border: 1px solid var(--primary-container);
  border-radius: var(--radius-sm);
  padding: 10px 16px;
  font-size: 0.82rem;
  color: var(--on-primary-container);
  margin-bottom: 1.25rem;
  font-weight: 500;
}

/* ── Hero Stat Cards (Stitch bento style) ─────────────────── */
.hero-row {
  display: flex;
  gap: 16px;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}
.hero-card {
  flex: 1;
  min-width: 140px;
  background: var(--surface);
  border-radius: var(--radius);
  padding: 1.25rem 1.5rem;
  box-shadow: var(--shadow);
  border: 1px solid var(--surface-high);
  transition: transform .15s, box-shadow .15s;
  position: relative;
  overflow: hidden;
}
.hero-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
.hero-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: var(--outline-variant);
  border-radius: var(--radius) var(--radius) 0 0;
}
.hero-card.primary::before { background: var(--primary); }
.hero-card.success::before { background: var(--success); }
.hero-card.warning::before { background: var(--warning); }
.hero-card.danger::before  { background: var(--danger); }

.hero-card .hc-icon  { font-size: 1.5rem; margin-bottom: 8px; }
.hero-card .hc-value {
  font-size: 2.25rem;
  font-weight: 800;
  line-height: 1;
  margin-bottom: 4px;
  color: var(--text);
  font-family: 'Plus Jakarta Sans', sans-serif;
}
.hero-card.primary .hc-value { color: var(--primary); }
.hero-card.success .hc-value { color: var(--success); }
.hero-card.warning .hc-value { color: var(--warning); }
.hero-card.danger  .hc-value { color: var(--danger); }
.hero-card .hc-label { font-size: 0.8rem; color: var(--text-muted); font-weight: 500; }

/* ── Badges ───────────────────────────────────────────────── */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.2px;
  white-space: nowrap;
}
.badge-fresh   { background: var(--success-light); color: #065F46; }
.badge-soon    { background: var(--warning-light);  color: #78350F; }
.badge-low     { background: var(--tertiary-light);  color: var(--tertiary); }
.badge-expired { background: var(--danger-light);   color: #991B1B; }
.badge-primary { background: var(--secondary-container); color: var(--primary-dark); }
.badge-gray    { background: var(--surface-high); color: var(--text-muted); }

/* ── Item Cards ───────────────────────────────────────────── */
.item-card {
  background: var(--surface);
  border-radius: var(--radius);
  padding: 1rem 1.25rem;
  box-shadow: var(--shadow);
  border: 1px solid var(--surface-high);
  margin-bottom: 12px;
  transition: box-shadow .15s, transform .15s;
}
.item-card:hover {
  box-shadow: var(--shadow-md);
  transform: scale(1.005);
}
.item-name { font-size: 0.95rem; font-weight: 700; color: var(--text); }
.item-qty  { font-size: 0.78rem; color: var(--text-muted); margin-top: 2px; }
.item-meta { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }

/* ── Shelf Life Bar ───────────────────────────────────────── */
.shelf-bar-bg {
  background: var(--surface-high);
  border-radius: var(--radius-full);
  height: 6px;
  overflow: hidden;
}
.shelf-bar-fill {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width .4s ease;
}
.shelf-bar-fill.fresh   { background: var(--success); }
.shelf-bar-fill.soon    { background: var(--warning); }
.shelf-bar-fill.low     { background: var(--tertiary); }
.shelf-bar-fill.expired { background: var(--danger); }
.shelf-days { font-size: 0.75rem; color: var(--text-muted); margin-top: 3px; }

/* ── Upload Zone ──────────────────────────────────────────── */
.upload-zone {
  border: 2px dashed var(--primary-container);
  border-radius: var(--radius);
  padding: 3rem 2rem;
  text-align: center;
  background: var(--surface-low);
  transition: border-color .15s, background .15s;
}
.upload-zone:hover {
  border-color: var(--primary);
  background: var(--secondary-container);
}
.upload-icon { font-size: 2.5rem; margin-bottom: 12px; }
.upload-text { font-size: 1rem; font-weight: 600; color: var(--primary); }
.upload-sub  { font-size: 0.82rem; color: var(--text-muted); margin-top: 4px; }

/* ── Wizard Steps ─────────────────────────────────────────── */
.wizard-steps {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
  background: var(--surface);
  border-radius: var(--radius);
  padding: 1rem 1.5rem;
  box-shadow: var(--shadow);
  border: 1px solid var(--surface-high);
}
.wizard-step {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.82rem;
  font-weight: 500;
  color: var(--text-muted);
  flex: 1;
}
.wizard-step.active { color: var(--primary); }
.wizard-step.done   { color: var(--success); }
.step-num {
  width: 26px; height: 26px;
  border-radius: var(--radius-full);
  background: var(--surface-high);
  color: var(--text-muted);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem; font-weight: 700; flex-shrink: 0;
}
.wizard-step.active .step-num { background: var(--primary);  color: #fff; }
.wizard-step.done   .step-num { background: var(--success);  color: #fff; }
.step-sep { flex: 1; height: 1px; background: var(--surface-high); margin: 0 8px; }

/* ── Recipe Cards (Stitch bento) ──────────────────────────── */
.recipe-card {
  background: var(--surface);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow: hidden;
  margin-bottom: 1.5rem;
  border: 1px solid var(--surface-high);
}
.recipe-header {
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  padding: 1.25rem 1.5rem;
}
.recipe-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #fff !important;
  margin: 0;
  font-family: 'Plus Jakarta Sans', sans-serif;
}
.recipe-time  { font-size: 0.8rem; color: rgba(255,255,255,.75); margin-top: 4px; }
.recipe-body  { padding: 1.25rem 1.5rem; }
.recipe-ingredients { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 1rem; }
.recipe-steps li {
  font-size: 0.88rem;
  color: var(--text);
  margin-bottom: 6px;
  line-height: 1.5;
}
.recipe-tip {
  background: var(--warning-light);
  border-left: 3px solid var(--warning);
  border-radius: 0 var(--radius-xs) var(--radius-xs) 0;
  padding: 10px 14px;
  font-size: 0.82rem;
  color: #78350F;
  margin-top: 1rem;
}

/* ── Alert Cards (Running Low) ────────────────────────────── */
.alert-card {
  background: var(--surface);
  border-radius: var(--radius);
  border-left: 4px solid var(--danger);
  padding: 1rem 1.25rem;
  box-shadow: var(--shadow);
  margin-bottom: 12px;
}
.alert-card.warn { border-left-color: var(--warning); }
.alert-name      { font-size: 1rem; font-weight: 700; color: var(--text); }
.alert-meta      { font-size: 0.8rem; color: var(--text-muted); margin-top: 2px; }
.alert-countdown {
  font-size: 1.5rem; font-weight: 800;
  color: var(--danger); line-height: 1;
  font-family: 'Plus Jakarta Sans', sans-serif;
}
.alert-countdown.warn { color: var(--warning); }

/* ── Prediction Cards ─────────────────────────────────────── */
.prediction-card {
  background: var(--surface);
  border-radius: var(--radius);
  border-left: 4px solid var(--primary-container);
  padding: 1rem 1.25rem;
  box-shadow: var(--shadow);
  margin-bottom: 12px;
}
.prediction-card.high { border-left-color: var(--danger); }
.prediction-card.medium { border-left-color: var(--warning); }

/* ── Section Title ────────────────────────────────────────── */
.section-title {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 12px;
}

/* ── Buttons (Stitch pill style) ──────────────────────────── */
.stButton > button {
  border-radius: var(--radius-sm) !important;
  font-weight: 600 !important;
  font-size: 0.875rem !important;
  transition: all .15s !important;
}
.stButton > button[kind="primary"] {
  background: var(--primary) !important;
  border-color: var(--primary) !important;
  color: var(--on-primary) !important;
}
.stButton > button[kind="primary"]:hover {
  background: var(--primary-dark) !important;
  border-color: var(--primary-dark) !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(141,110,99,.35) !important;
}

/* ── Streamlit widget overrides ───────────────────────────── */
.stTextInput > div > div,
.stSelectbox > div > div,
.stTextArea > div { border-radius: var(--radius-sm) !important; }

div[data-testid="stMetricValue"] {
  font-size: 1.5rem !important;
  font-weight: 800 !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── Pantry Shelf (Stitch-toned wood) ────────────────────── */
.pantry-unit {
  background: #1e140f;
  border-radius: var(--radius);
  padding: 20px 20px 8px;
  box-shadow: 0 8px 32px rgba(0,0,0,.30);
}

.shelf-category-label {
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #a07060;
  margin-bottom: 8px;
  padding-left: 4px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.shelf-items-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 10px 8px 14px;
  min-height: 90px;
  align-items: flex-end;
}

.shelf-plank {
  background: linear-gradient(180deg, #b07850 0%, #8d5c38 50%, #6b4226 100%);
  height: 10px;
  border-radius: 3px;
  box-shadow: 0 5px 10px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.12);
  margin-bottom: 20px;
}

/* Product tile */
.product-tile {
  background: var(--surface);
  border-radius: var(--radius-sm);
  padding: 10px 8px 8px;
  width: 100px;
  min-height: 88px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  box-shadow: 0 3px 8px rgba(0,0,0,.20);
  position: relative;
  transition: transform .15s, box-shadow .15s;
  border-top: 3px solid var(--primary);
}
.product-tile:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0,0,0,.25);
}
.product-tile.status-low     { border-top-color: var(--tertiary); }
.product-tile.status-expired { border-top-color: var(--danger); }
.product-tile.status-soon    { border-top-color: var(--warning); }
.product-tile.status-fresh   { border-top-color: var(--success); }

.product-tile .pt-icon { font-size: 1.6rem; margin-bottom: 4px; line-height: 1; }
.product-tile .pt-name { font-size: 0.7rem; font-weight: 700; color: var(--text); line-height: 1.2; }
.product-tile .pt-qty  { font-size: 0.62rem; color: var(--text-muted); margin-top: 3px; }
.product-tile .pt-days {
  font-size: 0.62rem; font-weight: 700;
  margin-top: 5px; padding: 2px 6px;
  border-radius: var(--radius-full);
}
.pt-days.fresh   { background: var(--success-light); color: #065F46; }
.pt-days.soon    { background: var(--warning-light);  color: #78350F; }
.pt-days.low     { background: var(--tertiary-light);  color: var(--tertiary); }
.pt-days.expired { background: var(--danger-light);   color: #991B1B; }

/* ── Dataframe overrides ──────────────────────────────────── */
[data-testid="stDataFrame"] {
  border-radius: var(--radius) !important;
  overflow: hidden;
  box-shadow: var(--shadow);
}

/* ── Expander ─────────────────────────────────────────────── */
[data-testid="stExpander"] {
  border-radius: var(--radius-sm) !important;
  border: 1px solid var(--surface-high) !important;
  background: var(--surface) !important;
}

/* ── Tab overrides ────────────────────────────────────────── */
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
  color: var(--primary) !important;
  border-bottom-color: var(--primary) !important;
}
</style>
"""
