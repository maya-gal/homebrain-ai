"""
styles.py — HomeBrain AI design system. Fun, hip, vibrant.
"""

def get_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@400;500;600;700;800;900&family=Nunito:ital,wght@0,400;0,500;0,600;0,700;0,800;1,700&display=swap');

/* ── Design Tokens ────────────────────────────────────────── */
:root {
  /* Brand — vibrant purple */
  --primary:          #7C3AED;
  --primary-dark:     #5B21B6;
  --primary-light:    #EDE9FE;
  --on-primary:       #ffffff;
  --grad:             linear-gradient(135deg, #7C3AED 0%, #EC4899 100%);
  --grad-warm:        linear-gradient(135deg, #F59E0B 0%, #EF4444 100%);
  --grad-cool:        linear-gradient(135deg, #06B6D4 0%, #7C3AED 100%);
  --grad-green:       linear-gradient(135deg, #10B981 0%, #06B6D4 100%);

  /* Semantic */
  --success:          #10B981;
  --success-light:    #D1FAE5;
  --warning:          #F59E0B;
  --warning-light:    #FEF3C7;
  --danger:           #EF4444;
  --danger-light:     #FEE2E2;
  --info:             #06B6D4;
  --info-light:       #CFFAFE;

  /* Surfaces */
  --bg:               #F5F3FF;
  --surface:          #FFFFFF;
  --surface-low:      #F0EEFF;
  --surface-mid:      #E9E6FF;
  --surface-high:     #DDD8FF;
  --border:           #E5E1FF;

  /* Text */
  --text:             #1E1033;
  --text-muted:       #6B7280;
  --text-light:       #9CA3AF;

  /* Category accent colors */
  --cat-produce:      #10B981;
  --cat-dairy:        #06B6D4;
  --cat-meat:         #EF4444;
  --cat-bakery:       #F59E0B;
  --cat-frozen:       #818CF8;
  --cat-pantry:       #F97316;
  --cat-beverages:    #06B6D4;
  --cat-snacks:       #EC4899;
  --cat-household:    #6B7280;
  --cat-other:        #9CA3AF;

  /* Radius */
  --radius:           20px;
  --radius-sm:        12px;
  --radius-xs:        8px;
  --radius-full:      9999px;

  /* Shadow */
  --shadow:    0 1px 3px rgba(124,58,237,.06), 0 1px 2px rgba(0,0,0,.04);
  --shadow-md: 0 4px 20px rgba(124,58,237,.12), 0 2px 6px rgba(0,0,0,.06);
  --shadow-lg: 0 16px 50px rgba(124,58,237,.18);
  --shadow-color: 0 4px 14px rgba(124,58,237,.35);
}

/* ── Base ─────────────────────────────────────────────────── */
html, body, [class*="css"] {
  font-family: 'Nunito', -apple-system, BlinkMacSystemFont, sans-serif !important;
  color: var(--text);
  background-color: var(--bg) !important;
}
h1, h2, h3, .page-title {
  font-family: 'Urbanist', sans-serif !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, .stDeployButton { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

.main .block-container {
  padding-top: 2rem;
  padding-bottom: 3rem;
  max-width: 1100px;
  background: var(--bg);
}

/* ── Sidebar ──────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #1E1033 0%, #2D1657 50%, #1E1033 100%) !important;
  border-right: none;
}
section[data-testid="stSidebar"] * { color: #C4B5FD !important; }

.sidebar-brand {
  font-family: 'Urbanist', sans-serif !important;
  font-size: 1.25rem;
  font-weight: 900;
  color: #fff !important;
  letter-spacing: -0.5px;
  background: var(--grad);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.sidebar-tagline {
  font-size: 0.75rem;
  color: #7C5CBF !important;
  margin-top: 2px;
}

/* Sidebar nav buttons */
section[data-testid="stSidebar"] .stButton > button {
  border-radius: var(--radius-sm) !important;
  font-weight: 700 !important;
  font-size: 0.85rem !important;
  text-align: left !important;
  transition: all .2s !important;
  background: transparent !important;
  border: none !important;
  color: #A78BFA !important;
  padding: 10px 14px !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(124,58,237,.2) !important;
  color: #fff !important;
  transform: translateX(4px) !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
  background: var(--grad) !important;
  color: #fff !important;
  box-shadow: 0 4px 12px rgba(124,58,237,.4) !important;
}

/* Sidebar stat pills */
.stat-pill {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 7px 12px;
  border-radius: var(--radius-xs);
  margin-bottom: 6px;
  background: rgba(124,58,237,.12);
  font-size: 0.78rem;
  border: 1px solid rgba(124,58,237,.2);
}
.stat-pill .label { color: #7C5CBF !important; }
.stat-pill .value { font-weight: 800; color: #E9D5FF !important; }
.stat-pill .value.warn   { color: var(--warning) !important; }
.stat-pill .value.danger { color: #FCA5A5 !important; }

/* ── Page Headers ─────────────────────────────────────────── */
.page-header { margin-bottom: 1.5rem; }
.page-title {
  font-size: 2rem;
  font-weight: 900;
  background: var(--grad);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -1px;
  margin: 0;
  font-family: 'Urbanist', sans-serif !important;
}
.page-sub {
  font-size: 0.9rem;
  color: var(--text-muted);
  margin-top: 4px;
  font-weight: 500;
}

/* ── Demo Banner ──────────────────────────────────────────── */
.demo-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--primary-light);
  border: 1px solid rgba(124,58,237,.25);
  border-radius: var(--radius-sm);
  padding: 10px 16px;
  font-size: 0.82rem;
  color: var(--primary-dark);
  margin-bottom: 1.25rem;
  font-weight: 600;
}

/* ── Hero Stat Cards ──────────────────────────────────────── */
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
  border: 1px solid var(--border);
  transition: transform .2s, box-shadow .2s;
  position: relative;
  overflow: hidden;
}
.hero-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}
.hero-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 4px;
  background: var(--grad);
  border-radius: var(--radius) var(--radius) 0 0;
}
.hero-card.success::before { background: var(--grad-green); }
.hero-card.warning::before { background: var(--grad-warm); }
.hero-card.danger::before  { background: var(--grad-warm); }

.hero-card .hc-icon  { font-size: 1.75rem; margin-bottom: 8px; }
.hero-card .hc-value {
  font-size: 2.5rem;
  font-weight: 900;
  line-height: 1;
  margin-bottom: 4px;
  color: var(--text);
  font-family: 'Urbanist', sans-serif;
}
.hero-card.primary .hc-value { color: var(--primary); }
.hero-card.success .hc-value { color: var(--success); }
.hero-card.warning .hc-value { color: var(--warning); }
.hero-card.danger  .hc-value { color: var(--danger); }
.hero-card .hc-label { font-size: 0.82rem; color: var(--text-muted); font-weight: 600; }

/* ── Badges ───────────────────────────────────────────────── */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.3px;
  white-space: nowrap;
}
.badge-fresh   { background: var(--success-light); color: #065F46; }
.badge-soon    { background: var(--warning-light);  color: #92400E; }
.badge-low     { background: #FEE2E2;               color: #991B1B; }
.badge-expired { background: var(--danger-light);   color: #991B1B; }
.badge-primary { background: var(--primary-light);  color: var(--primary-dark); }
.badge-gray    { background: var(--surface-mid);    color: var(--text-muted); }

/* ── Product Thumbnail ────────────────────────────────────── */
.item-thumb {
  width: 76px;
  height: 76px;
  border-radius: 16px;
  object-fit: cover;
  flex-shrink: 0;
  background: var(--surface-low);
  box-shadow: 0 4px 12px rgba(0,0,0,.12);
  transition: transform .2s;
}
.item-thumb:hover { transform: scale(1.06) rotate(2deg); }
.item-thumb-emoji {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  background: var(--surface-low);
  box-shadow: 0 4px 12px rgba(0,0,0,.08);
}

/* ── Item Cards (kept for alert/prediction cards) ─────────── */
.item-card {
  background: var(--surface);
  border-radius: var(--radius);
  padding: 1rem 1.25rem;
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
  margin-bottom: 14px;
  transition: box-shadow .2s, transform .2s;
}
.item-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.item-card-top  { display: flex; align-items: center; gap: 14px; margin-bottom: 10px; }
.item-name {
  font-size: 0.92rem; font-weight: 800; color: var(--text);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
/* Remove button fused to item card */
[data-testid="element-container"]:has(.item-card) .item-card {
  margin-bottom: 0 !important;
  border-radius: var(--radius) var(--radius) 0 0 !important;
  border-bottom: none !important;
}
[data-testid="element-container"]:has(.item-card) + [data-testid="element-container"] button {
  border-radius: 0 0 var(--radius) var(--radius) !important;
  border-top: none !important;
  margin-top: 0 !important;
  margin-bottom: 14px !important;
  background: #FFF5F5 !important;
  color: #DC2626 !important;
  border: 1px solid var(--border) !important;
  font-size: 0.8rem !important;
  font-weight: 600 !important;
}
[data-testid="element-container"]:has(.item-card) + [data-testid="element-container"] button:hover {
  background: #FEE2E2 !important;
}
.item-qty  { font-size: 0.78rem; color: var(--text-muted); margin-top: 2px; font-weight: 500; }
.item-meta { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }
.item-prediction { font-size: 0.72rem; color: #7C3AED; background: #EDE9FE; border-radius: 6px; padding: 3px 8px; margin-top: 6px; display: inline-block; font-weight: 600; }

/* ── Pantry Cards ─────────────────────────────────────────── */
.pantry-card {
  background: var(--surface);
  border-radius: 16px 16px 0 0;
  border: 1px solid var(--border);
  border-bottom: none;
  box-shadow: 0 2px 14px rgba(0,0,0,.07);
  overflow: hidden;
  margin-bottom: 0;
  text-align: center;
  transition: box-shadow .2s, transform .2s;
}
.pantry-card:hover { box-shadow: 0 6px 24px rgba(0,0,0,.13); transform: translateY(-2px); }
.pc-img {
  padding: 22px 20px 8px;
  display: flex;
  justify-content: center;
}
.pc-img .item-thumb {
  width: 82px !important;
  height: 82px !important;
  font-size: 2.7rem !important;
  margin: 0 auto;
}
.pc-name {
  font-size: 0.95rem;
  font-weight: 800;
  color: var(--text);
  padding: 0 14px 3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.pc-qty { font-size: 0.75rem; color: var(--text-muted); padding: 0 14px 10px; }
.pc-footer {
  border-top: 1px solid #F1F5F9;
  padding: 10px 14px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}
.pc-expiry {
  font-size: 0.8rem;
  font-weight: 700;
  padding: 5px 14px;
  border-radius: 20px;
  letter-spacing: .01em;
}
.pc-expiry.fresh   { background:#D1FAE5; color:#065F46; }
.pc-expiry.soon    { background:#FEF3C7; color:#92400E; }
.pc-expiry.low     { background:#FEE2E2; color:#991B1B; }
.pc-expiry.expired { background:#F3F4F6; color:#6B7280; }
.pc-pred { font-size: 0.7rem; color: #7C3AED; font-weight: 600; }

/* Remove button fused below pantry card */
[data-testid="stMarkdownContainer"]:has(.pantry-card) + [data-testid="stButton"] > button {
  border-radius: 0 0 16px 16px !important;
  border-top: none !important;
  margin-top: 0 !important;
  margin-bottom: 16px !important;
  background: #FFF5F5 !important;
  color: #DC2626 !important;
  border: 1px solid var(--border) !important;
  font-size: 0.8rem !important;
  font-weight: 600 !important;
}
[data-testid="stMarkdownContainer"]:has(.pantry-card) + [data-testid="stButton"] > button:hover {
  background: #FEE2E2 !important;
}

/* ── Shelf Life Bar ───────────────────────────────────────── */
.shelf-bar-bg {
  background: var(--surface-mid);
  border-radius: var(--radius-full);
  height: 7px;
  overflow: hidden;
}
.shelf-bar-fill {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width .5s cubic-bezier(.4,0,.2,1);
}
.shelf-bar-fill.fresh   { background: linear-gradient(90deg, #10B981, #34D399); }
.shelf-bar-fill.soon    { background: linear-gradient(90deg, #F59E0B, #FCD34D); }
.shelf-bar-fill.low     { background: linear-gradient(90deg, #F97316, #FB923C); }
.shelf-bar-fill.expired { background: linear-gradient(90deg, #EF4444, #F87171); }
.shelf-days { font-size: 0.72rem; color: var(--text-muted); margin-top: 3px; font-weight: 600; }

/* ── Upload Zone ──────────────────────────────────────────── */
.upload-zone {
  border: 2.5px dashed var(--primary-light);
  border-radius: var(--radius);
  padding: 3rem 2rem;
  text-align: center;
  background: linear-gradient(135deg, #FAF5FF 0%, #F0EEFF 100%);
  transition: all .2s;
}
.upload-zone:hover {
  border-color: var(--primary);
  background: linear-gradient(135deg, #EDE9FE 0%, #E0D9FD 100%);
  transform: scale(1.01);
}
.upload-icon { font-size: 3rem; margin-bottom: 12px; }
.upload-text { font-size: 1rem; font-weight: 800; color: var(--primary); }
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
  border: 1px solid var(--border);
}
.wizard-step {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-muted);
  flex: 1;
}
.wizard-step.active { color: var(--primary); }
.wizard-step.done   { color: var(--success); }
.step-num {
  width: 28px; height: 28px;
  border-radius: var(--radius-full);
  background: var(--surface-mid);
  color: var(--text-muted);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem; font-weight: 800; flex-shrink: 0;
}
.wizard-step.active .step-num { background: var(--grad); color: #fff; }
.wizard-step.done   .step-num { background: var(--grad-green); color: #fff; }
.step-sep { flex: 1; height: 2px; background: var(--border); margin: 0 8px; border-radius: 2px; }

/* ── Recipe Cards ─────────────────────────────────────────── */
.recipe-card {
  background: var(--surface);
  border-radius: var(--radius);
  box-shadow: var(--shadow-md);
  overflow: hidden;
  margin-bottom: 1.5rem;
  border: 1px solid var(--border);
}
.recipe-header {
  background: var(--grad);
  padding: 1.5rem 1.5rem;
}
.recipe-title {
  font-size: 1.25rem;
  font-weight: 900;
  color: #fff !important;
  margin: 0;
  font-family: 'Urbanist', sans-serif;
  letter-spacing: -0.3px;
}
.recipe-time  { font-size: 0.8rem; color: rgba(255,255,255,.75); margin-top: 4px; font-weight: 600; }
.recipe-body  { padding: 1.25rem 1.5rem; }
.recipe-ingredients { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 1rem; }
.recipe-steps li {
  font-size: 0.88rem;
  color: var(--text);
  margin-bottom: 6px;
  line-height: 1.55;
}
.recipe-tip {
  background: var(--warning-light);
  border-left: 3px solid var(--warning);
  border-radius: 0 var(--radius-xs) var(--radius-xs) 0;
  padding: 10px 14px;
  font-size: 0.82rem;
  color: #92400E;
  margin-top: 1rem;
  font-weight: 600;
}

/* ── Alert Cards (Running Low) ────────────────────────────── */
.alert-card {
  background: var(--surface);
  border-radius: var(--radius);
  border-left: 5px solid var(--danger);
  padding: 1rem 1.25rem;
  box-shadow: var(--shadow);
  margin-bottom: 12px;
  transition: transform .2s, box-shadow .2s;
}
.alert-card:hover {
  transform: translateX(4px);
  box-shadow: var(--shadow-md);
}
.alert-card.warn { border-left-color: var(--warning); }
.alert-name      { font-size: 1rem; font-weight: 800; color: var(--text); }
.alert-meta      { font-size: 0.78rem; color: var(--text-muted); margin-top: 2px; font-weight: 500; }
.alert-countdown {
  font-size: 1.6rem; font-weight: 900;
  color: var(--danger); line-height: 1;
  font-family: 'Urbanist', sans-serif;
}
.alert-countdown.warn { color: var(--warning); }

/* ── Prediction Cards ─────────────────────────────────────── */
.prediction-card {
  background: var(--surface);
  border-radius: var(--radius);
  border-left: 5px solid var(--primary-light);
  padding: 1rem 1.25rem;
  box-shadow: var(--shadow);
  margin-bottom: 12px;
}
.prediction-card.high   { border-left-color: var(--danger); }
.prediction-card.medium { border-left-color: var(--warning); }

/* ── Section Title ────────────────────────────────────────── */
.section-title {
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 1.8px;
  text-transform: uppercase;
  color: var(--primary);
  margin-bottom: 14px;
  opacity: 0.7;
}

/* ── Buttons ──────────────────────────────────────────────── */
.stButton > button {
  border-radius: var(--radius-sm) !important;
  font-weight: 700 !important;
  font-size: 0.875rem !important;
  transition: all .2s !important;
  font-family: 'Nunito', sans-serif !important;
}
.stButton > button[kind="primary"] {
  background: var(--grad) !important;
  border: none !important;
  color: #fff !important;
  box-shadow: 0 4px 14px rgba(124,58,237,.35) !important;
}
.stButton > button[kind="primary"]:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px rgba(124,58,237,.45) !important;
}

/* ── Streamlit widget overrides ───────────────────────────── */
.stTextInput > div > div,
.stSelectbox > div > div,
.stTextArea > div { border-radius: var(--radius-sm) !important; }

div[data-testid="stMetricValue"] {
  font-size: 1.75rem !important;
  font-weight: 900 !important;
  font-family: 'Urbanist', sans-serif !important;
  color: var(--primary) !important;
}

/* ── Pantry Shelf ─────────────────────────────────────────── */
.pantry-unit {
  background: linear-gradient(180deg, #1E1033 0%, #2D1657 100%);
  border-radius: var(--radius);
  padding: 20px 20px 8px;
  box-shadow: var(--shadow-lg);
}

.shelf-category-label {
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #A78BFA;
  margin-bottom: 8px;
  padding-left: 4px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.shelf-items-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  padding: 10px 8px 14px;
  min-height: 90px;
  align-items: flex-end;
}

.shelf-plank {
  background: linear-gradient(180deg, #4C1D95 0%, #3B0764 50%, #2E1065 100%);
  height: 10px;
  border-radius: 4px;
  box-shadow: 0 5px 10px rgba(0,0,0,.45), inset 0 1px 0 rgba(167,139,250,.15);
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
  box-shadow: 0 4px 12px rgba(0,0,0,.20);
  position: relative;
  transition: transform .2s, box-shadow .2s;
  border-top: 3px solid var(--primary);
}
.product-tile:hover {
  transform: translateY(-6px) rotate(-1deg);
  box-shadow: 0 12px 24px rgba(0,0,0,.25);
}
.product-tile.status-low     { border-top-color: var(--danger); }
.product-tile.status-expired { border-top-color: var(--danger); }
.product-tile.status-soon    { border-top-color: var(--warning); }
.product-tile.status-fresh   { border-top-color: var(--success); }

.product-tile .pt-icon { font-size: 1.75rem; margin-bottom: 4px; line-height: 1; }
.product-tile .pt-name { font-size: 0.7rem; font-weight: 800; color: var(--text); line-height: 1.2; }
.product-tile .pt-qty  { font-size: 0.62rem; color: var(--text-muted); margin-top: 3px; font-weight: 600; }
.product-tile .pt-days {
  font-size: 0.62rem; font-weight: 800;
  margin-top: 5px; padding: 2px 7px;
  border-radius: var(--radius-full);
}
.pt-days.fresh   { background: var(--success-light); color: #065F46; }
.pt-days.soon    { background: var(--warning-light);  color: #92400E; }
.pt-days.low     { background: #FEE2E2;               color: #991B1B; }
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
  border: 1px solid var(--border) !important;
  background: var(--surface) !important;
}

/* ── Tab overrides ────────────────────────────────────────── */
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
  color: var(--primary) !important;
  border-bottom-color: var(--primary) !important;
  font-weight: 800 !important;
}
</style>
"""
