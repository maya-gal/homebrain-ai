"""
styles.py — HomeBrain AI design system. Café / warm-vintage aesthetic.
"""

def get_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700;800;900&family=DM+Sans:wght@300;400;500;600;700&display=swap');

/* ── Design Tokens ────────────────────────────────────────── */
:root {
  /* Brand — warm burgundy */
  --primary:          #7D1F1F;
  --primary-dark:     #5C1515;
  --primary-light:    #F5E8E8;
  --on-primary:       #FFF8F0;

  /* Semantic */
  --success:          #2E6B45;
  --success-light:    #DDF0E6;
  --warning:          #A05C1A;
  --warning-light:    #FDF0DC;
  --danger:           #8B2020;
  --danger-light:     #FAE3E3;
  --info:             #2B5F7A;
  --info-light:       #DDF0F9;

  /* Surfaces — warm cream */
  --bg:               #F2E8D5;
  --surface:          #FFFDF7;
  --surface-low:      #F7F0E3;
  --surface-mid:      #EDE2CC;
  --surface-high:     #E2D4B8;
  --border:           #DDD0B5;

  /* Text */
  --text:             #1A0C08;
  --text-muted:       #6B5643;
  --text-light:       #9C836A;

  /* Sidebar */
  --sidebar-bg:       #1C0A08;
  --sidebar-accent:   #C8A06A;

  /* Gradients */
  --grad:       linear-gradient(135deg, #7D1F1F 0%, #C05A1A 100%);
  --grad-warm:  linear-gradient(135deg, #A05C1A 0%, #C83030 100%);
  --grad-green: linear-gradient(135deg, #2E6B45 0%, #5DAA7A 100%);
  --grad-cool:  linear-gradient(135deg, #2B5F7A 0%, #7D1F1F 100%);

  /* Radius */
  --radius:     16px;
  --radius-sm:  10px;
  --radius-xs:  6px;
  --radius-full: 9999px;

  /* Shadow */
  --shadow:    0 2px 8px rgba(26,12,8,.07), 0 1px 2px rgba(0,0,0,.04);
  --shadow-md: 0 6px 24px rgba(26,12,8,.12), 0 2px 6px rgba(0,0,0,.06);
  --shadow-lg: 0 16px 48px rgba(26,12,8,.18);
}

/* ── Base ─────────────────────────────────────────────────── */
html, body, [class*="css"] {
  font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
  color: var(--text);
  background-color: var(--bg) !important;
}
h1, h2, h3, .page-title {
  font-family: 'Playfair Display', Georgia, serif !important;
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
  background: var(--sidebar-bg) !important;
  border-right: 1px solid rgba(200,160,106,.12);
}
section[data-testid="stSidebar"] * { color: #C8A06A !important; }

.sidebar-brand {
  font-family: 'Playfair Display', serif !important;
  font-size: 1.3rem;
  font-weight: 800;
  color: #F5E8D0 !important;
  letter-spacing: 0;
  -webkit-text-fill-color: #F5E8D0 !important;
}
.sidebar-tagline {
  font-size: 0.72rem;
  color: #7A5C3A !important;
  margin-top: 3px;
  letter-spacing: 0.5px;
}
.sidebar-divider { border-color: rgba(200,160,106,.15) !important; }

/* Sidebar nav buttons */
section[data-testid="stSidebar"] .stButton > button {
  border-radius: var(--radius-xs) !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  text-align: left !important;
  transition: all .2s !important;
  background: transparent !important;
  border: none !important;
  color: #B89060 !important;
  padding: 10px 14px !important;
  letter-spacing: 0.2px !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(200,160,106,.1) !important;
  color: #F5E8D0 !important;
  transform: translateX(3px) !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
  background: var(--primary) !important;
  color: #FFF8F0 !important;
  box-shadow: 0 3px 10px rgba(125,31,31,.4) !important;
}

/* Sidebar stat pills */
.stat-pill {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 7px 12px;
  border-radius: var(--radius-xs);
  margin-bottom: 6px;
  background: rgba(200,160,106,.08);
  font-size: 0.78rem;
  border: 1px solid rgba(200,160,106,.15);
}
.stat-pill .label { color: #7A5C3A !important; }
.stat-pill .value { font-weight: 700; color: #D4A06A !important; }
.stat-pill .value.warn   { color: #E08040 !important; }
.stat-pill .value.danger { color: #E07070 !important; }

/* ── Page Headers ─────────────────────────────────────────── */
.page-header { margin-bottom: 1.5rem; }
.page-title {
  font-size: 2rem;
  font-weight: 800;
  color: var(--primary) !important;
  letter-spacing: -0.5px;
  margin: 0;
  font-family: 'Playfair Display', serif !important;
  -webkit-text-fill-color: var(--primary) !important;
}
.page-sub {
  font-size: 0.88rem;
  color: var(--text-muted);
  margin-top: 5px;
  font-weight: 400;
  letter-spacing: 0.1px;
}

/* ── Hero Stat Cards ──────────────────────────────────────── */
.hero-row {
  display: flex;
  gap: 14px;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}
.hero-card {
  flex: 1;
  min-width: 130px;
  background: var(--surface);
  border-radius: var(--radius);
  padding: 1.2rem 1.4rem;
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
  transition: transform .2s, box-shadow .2s;
  position: relative;
  overflow: hidden;
}
.hero-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); }
.hero-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: var(--grad);
  border-radius: var(--radius) var(--radius) 0 0;
}
.hero-card.success::before { background: var(--grad-green); }
.hero-card.warning::before { background: var(--grad-warm); }
.hero-card.danger::before  { background: var(--grad-warm); }

.hero-card .hc-icon  { font-size: 1.5rem; margin-bottom: 8px; }
.hero-card .hc-value {
  font-size: 2.4rem;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 4px;
  color: var(--text);
  font-family: 'Playfair Display', serif;
}
.hero-card.primary .hc-value { color: var(--primary); }
.hero-card.success .hc-value { color: var(--success); }
.hero-card.warning .hc-value { color: var(--warning); }
.hero-card.danger  .hc-value { color: var(--danger); }
.hero-card .hc-label { font-size: 0.78rem; color: var(--text-muted); font-weight: 500; letter-spacing: 0.3px; }

/* ── Badges ───────────────────────────────────────────────── */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.3px;
  white-space: nowrap;
}
.badge-fresh   { background: var(--success-light); color: #1A5C32; }
.badge-soon    { background: var(--warning-light);  color: #7A4210; }
.badge-low     { background: var(--danger-light);   color: #6B1515; }
.badge-expired { background: var(--danger-light);   color: #6B1515; }
.badge-primary { background: var(--primary-light);  color: var(--primary); }
.badge-gray    { background: var(--surface-mid);    color: var(--text-muted); }

/* ── Product Thumbnail ────────────────────────────────────── */
.mh-img .item-thumb { width:80px !important; height:80px !important; border-radius:12px !important; margin-bottom:8px; }
.item-thumb {
  width: 72px;
  height: 72px;
  border-radius: 12px;
  object-fit: cover;
  flex-shrink: 0;
  background: var(--surface-low);
  box-shadow: 0 3px 10px rgba(26,12,8,.14);
  transition: transform .2s;
}
.item-thumb:hover { transform: scale(1.05); }
.item-thumb-emoji {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  background: var(--surface-low);
}

/* ── Item Cards ───────────────────────────────────────────── */
.item-card {
  background: var(--surface);
  border-radius: var(--radius);
  padding: 1rem 1.1rem;
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
  margin-bottom: 14px;
  transition: box-shadow .2s, transform .2s;
  position: relative;
}
.item-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.card-del {
  position: absolute;
  top: 9px; right: 10px;
  width: 20px; height: 20px;
  border-radius: 50%;
  background: var(--danger-light);
  color: var(--danger);
  font-size: 0.72rem;
  font-weight: 700;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity .15s;
  line-height: 1;
}
.item-card:hover .card-del { opacity: 1; }
.item-card-top { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
.item-name { font-size: 0.9rem; font-weight: 600; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.item-qty  { font-size: 0.75rem; color: var(--text-muted); margin-top: 2px; }
.item-meta { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }
.item-prediction {
  font-size: 0.7rem;
  color: var(--primary);
  background: var(--primary-light);
  border-radius: 5px;
  padding: 3px 8px;
  margin-top: 6px;
  display: inline-block;
  font-weight: 600;
}

/* ── Shelf Life Bar ───────────────────────────────────────── */
.shelf-bar-bg { background: var(--surface-mid); border-radius: var(--radius-full); height: 5px; overflow: hidden; }
.shelf-bar-fill { height: 100%; border-radius: var(--radius-full); transition: width .5s cubic-bezier(.4,0,.2,1); }
.shelf-bar-fill.fresh   { background: linear-gradient(90deg, #2E6B45, #5DAA7A); }
.shelf-bar-fill.soon    { background: linear-gradient(90deg, #A05C1A, #D4882A); }
.shelf-bar-fill.low     { background: linear-gradient(90deg, #8B2020, #C04040); }
.shelf-bar-fill.expired { background: linear-gradient(90deg, #6B1515, #8B2020); }
.shelf-days { font-size: 0.7rem; color: var(--text-muted); margin-top: 3px; font-weight: 600; }

/* ── Upload Zone ──────────────────────────────────────────── */
.upload-zone {
  border: 2px dashed var(--border);
  border-radius: var(--radius);
  padding: 3rem 2rem;
  text-align: center;
  background: var(--surface-low);
  transition: all .2s;
}
.upload-zone:hover { border-color: var(--primary); background: var(--primary-light); transform: scale(1.01); }
.upload-icon { font-size: 2.5rem; margin-bottom: 12px; }
.upload-text { font-size: 1rem; font-weight: 700; color: var(--primary); font-family: 'Playfair Display', serif; }
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
.wizard-step { display: flex; align-items: center; gap: 8px; font-size: 0.82rem; font-weight: 500; color: var(--text-muted); flex: 1; }
.wizard-step.active { color: var(--primary); }
.wizard-step.done   { color: var(--success); }
.step-num {
  width: 26px; height: 26px;
  border-radius: var(--radius-full);
  background: var(--surface-mid);
  color: var(--text-muted);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.72rem; font-weight: 700; flex-shrink: 0;
}
.wizard-step.active .step-num { background: var(--primary); color: #fff; }
.wizard-step.done   .step-num { background: var(--success); color: #fff; }
.step-sep { flex: 1; height: 1px; background: var(--border); margin: 0 8px; }

/* ── Recipe Cards ─────────────────────────────────────────── */
.recipe-card {
  background: var(--surface);
  border-radius: var(--radius);
  box-shadow: var(--shadow-md);
  overflow: hidden;
  margin-bottom: 1.5rem;
  border: 1px solid var(--border);
}
.recipe-header { background: var(--grad); padding: 1.4rem 1.5rem; }
.recipe-title { font-size: 1.2rem; font-weight: 700; color: #fff !important; margin: 0; font-family: 'Playfair Display', serif; }
.recipe-time  { font-size: 0.78rem; color: rgba(255,255,255,.75); margin-top: 4px; }
.recipe-body  { padding: 1.2rem 1.5rem; }
.recipe-ingredients { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 1rem; }
.recipe-steps li { font-size: 0.88rem; color: var(--text); margin-bottom: 6px; line-height: 1.55; }
.recipe-tip {
  background: var(--warning-light);
  border-left: 3px solid var(--warning);
  border-radius: 0 var(--radius-xs) var(--radius-xs) 0;
  padding: 10px 14px;
  font-size: 0.82rem;
  color: #7A4210;
  margin-top: 1rem;
}

/* ── Alert Cards ──────────────────────────────────────────── */
.alert-card {
  background: var(--surface);
  border-radius: var(--radius);
  border-left: 4px solid var(--danger);
  padding: 1rem 1.2rem;
  box-shadow: var(--shadow);
  margin-bottom: 12px;
  transition: transform .2s, box-shadow .2s;
}
.alert-card:hover { transform: translateX(3px); box-shadow: var(--shadow-md); }
.alert-card.warn { border-left-color: var(--warning); }
.alert-name  { font-size: 0.95rem; font-weight: 700; color: var(--text); }
.alert-meta  { font-size: 0.76rem; color: var(--text-muted); margin-top: 2px; }
.alert-countdown { font-size: 1.5rem; font-weight: 800; color: var(--danger); line-height: 1; font-family: 'Playfair Display', serif; }
.alert-countdown.warn { color: var(--warning); }

/* ── Section Title ────────────────────────────────────────── */
.section-title {
  font-size: 0.66rem;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 14px;
  border-bottom: 1px solid var(--border);
  padding-bottom: 8px;
}

/* ── Buttons ──────────────────────────────────────────────── */
.stButton > button {
  border-radius: var(--radius-xs) !important;
  font-weight: 600 !important;
  font-size: 0.875rem !important;
  transition: all .2s !important;
  font-family: 'DM Sans', sans-serif !important;
  letter-spacing: 0.1px !important;
}
.stButton > button[kind="primary"] {
  background: var(--primary) !important;
  border: none !important;
  color: #FFF8F0 !important;
  box-shadow: 0 3px 12px rgba(125,31,31,.3) !important;
}
.stButton > button[kind="primary"]:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 18px rgba(125,31,31,.4) !important;
  background: var(--primary-dark) !important;
}

/* ── Streamlit widget overrides ───────────────────────────── */
.stTextInput > div > div,
.stSelectbox > div > div,
.stTextArea > div { border-radius: var(--radius-xs) !important; border-color: var(--border) !important; }

/* ── Pantry Shelf ─────────────────────────────────────────── */
.pantry-unit {
  background: linear-gradient(180deg, #2C1210 0%, #1C0A08 100%);
  border-radius: var(--radius);
  padding: 20px 20px 8px;
  box-shadow: var(--shadow-lg);
}
.shelf-category-label {
  font-size: 0.66rem;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #C8A06A;
  margin-bottom: 8px;
  padding-left: 4px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.shelf-items-row { display: flex; flex-wrap: wrap; gap: 12px; padding: 10px 8px 14px; min-height: 90px; align-items: flex-end; }
.shelf-plank {
  background: linear-gradient(180deg, #5C2E1A 0%, #3C1A0A 100%);
  height: 8px;
  border-radius: 3px;
  box-shadow: 0 5px 10px rgba(0,0,0,.5), inset 0 1px 0 rgba(200,160,106,.1);
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
  box-shadow: 0 4px 12px rgba(0,0,0,.2);
  position: relative;
  transition: transform .2s, box-shadow .2s;
  border-top: 3px solid var(--primary);
}
.product-tile:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,.22); }
.product-tile.status-low     { border-top-color: var(--danger); }
.product-tile.status-expired { border-top-color: var(--danger); }
.product-tile.status-soon    { border-top-color: var(--warning); }
.product-tile.status-fresh   { border-top-color: var(--success); }
.product-tile .pt-icon { font-size: 1.75rem; margin-bottom: 4px; line-height: 1; }
.product-tile .pt-name { font-size: 0.7rem; font-weight: 700; color: var(--text); line-height: 1.2; }
.product-tile .pt-qty  { font-size: 0.62rem; color: var(--text-muted); margin-top: 3px; }
.product-tile .pt-days { font-size: 0.62rem; font-weight: 700; margin-top: 5px; padding: 2px 7px; border-radius: var(--radius-full); }
.pt-days.fresh   { background: var(--success-light); color: #1A5C32; }
.pt-days.soon    { background: var(--warning-light); color: #7A4210; }
.pt-days.low     { background: var(--danger-light);  color: #6B1515; }
.pt-days.expired { background: var(--danger-light);  color: #6B1515; }

/* ── Dataframe ────────────────────────────────────────────── */
[data-testid="stDataFrame"] { border-radius: var(--radius) !important; overflow: hidden; box-shadow: var(--shadow); }

/* ── Expander ─────────────────────────────────────────────── */
[data-testid="stExpander"] {
  border-radius: var(--radius-sm) !important;
  border: 1px solid var(--border) !important;
  background: var(--surface) !important;
}

/* ── Tabs ─────────────────────────────────────────────────── */
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
  color: var(--primary) !important;
  border-bottom-color: var(--primary) !important;
  font-weight: 700 !important;
}
</style>
"""
