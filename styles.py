"""
styles.py — Full design system for HomeBrain AI.
All CSS lives here. Import get_css() and inject with st.markdown().
"""

def get_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Reset & Base ─────────────────────────────────────────── */
:root {
  --primary:       #6366F1;
  --primary-light: #EEF2FF;
  --primary-dark:  #4F46E5;
  --success:       #10B981;
  --success-light: #D1FAE5;
  --warning:       #F59E0B;
  --warning-light: #FEF3C7;
  --danger:        #EF4444;
  --danger-light:  #FEE2E2;
  --info:          #3B82F6;
  --info-light:    #DBEAFE;
  --surface:       #FFFFFF;
  --bg:            #F1F5F9;
  --border:        #E2E8F0;
  --text:          #0F172A;
  --muted:         #64748B;
  --radius:        12px;
  --radius-sm:     8px;
  --shadow:        0 1px 3px rgba(0,0,0,.08), 0 1px 2px rgba(0,0,0,.04);
  --shadow-md:     0 4px 6px -1px rgba(0,0,0,.1), 0 2px 4px -1px rgba(0,0,0,.06);
}

html, body, [class*="css"] {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  color: var(--text);
}

/* Hide Streamlit chrome */
#MainMenu, footer, .stDeployButton { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

/* Main content padding */
.main .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1100px; }

/* ── Sidebar ──────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
  background: var(--text) !important;
  border-right: none;
}
section[data-testid="stSidebar"] * { color: #CBD5E1 !important; }
section[data-testid="stSidebar"] .sidebar-brand { color: #fff !important; }
section[data-testid="stSidebar"] .sidebar-divider {
  border-color: #1E293B !important; margin: 0.75rem 0;
}

/* Sidebar nav button */
.nav-btn {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 14px; border-radius: var(--radius-sm);
  cursor: pointer; transition: background .15s;
  font-size: 0.88rem; font-weight: 500;
  color: #94A3B8 !important;
  margin-bottom: 4px; width: 100%;
}
.nav-btn:hover  { background: #1E293B; color: #E2E8F0 !important; }
.nav-btn.active { background: var(--primary); color: #fff !important; }
.nav-btn.active * { color: #fff !important; }
.nav-icon { font-size: 1.1rem; width: 22px; text-align: center; }

/* Sidebar stat pill */
.stat-pill {
  display: flex; justify-content: space-between; align-items: center;
  padding: 6px 10px; border-radius: 6px; margin-bottom: 6px;
  background: #1E293B; font-size: 0.8rem;
}
.stat-pill .label { color: #94A3B8 !important; }
.stat-pill .value { font-weight: 700; color: #F1F5F9 !important; }
.stat-pill .value.warn { color: var(--warning) !important; }
.stat-pill .value.danger { color: var(--danger) !important; }

/* Sidebar brand */
.sidebar-brand {
  font-size: 1.25rem; font-weight: 800; letter-spacing: -0.5px;
  color: #FFFFFF !important; display: flex; align-items: center; gap: 8px;
}
.sidebar-tagline { font-size: 0.78rem; color: #64748B !important; margin-top: 2px; }

/* ── Page Headers ─────────────────────────────────────────── */
.page-header { margin-bottom: 1.5rem; }
.page-title {
  font-size: 1.75rem; font-weight: 800; color: var(--text);
  letter-spacing: -0.5px; margin: 0;
}
.page-sub { font-size: 0.875rem; color: var(--muted); margin-top: 4px; }

/* ── Demo Banner ──────────────────────────────────────────── */
.demo-banner {
  display: flex; align-items: center; gap: 10px;
  background: var(--primary-light); border: 1px solid #C7D2FE;
  border-radius: var(--radius-sm); padding: 10px 16px;
  font-size: 0.82rem; color: var(--primary); margin-bottom: 1.25rem;
  font-weight: 500;
}

/* ── Hero Stat Cards ──────────────────────────────────────── */
.hero-row { display: flex; gap: 16px; margin-bottom: 1.5rem; flex-wrap: wrap; }
.hero-card {
  flex: 1; min-width: 140px;
  background: var(--surface); border-radius: var(--radius);
  padding: 1.25rem 1.5rem; box-shadow: var(--shadow);
  border-top: 3px solid var(--border);
  transition: transform .15s, box-shadow .15s;
}
.hero-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
.hero-card.primary { border-top-color: var(--primary); }
.hero-card.success { border-top-color: var(--success); }
.hero-card.warning { border-top-color: var(--warning); }
.hero-card.danger  { border-top-color: var(--danger); }
.hero-card .hc-icon  { font-size: 1.5rem; margin-bottom: 8px; }
.hero-card .hc-value {
  font-size: 2.25rem; font-weight: 800; line-height: 1;
  margin-bottom: 4px; color: var(--text);
}
.hero-card.primary .hc-value { color: var(--primary); }
.hero-card.success .hc-value { color: var(--success); }
.hero-card.warning .hc-value { color: var(--warning); }
.hero-card.danger  .hc-value { color: var(--danger); }
.hero-card .hc-label { font-size: 0.8rem; color: var(--muted); font-weight: 500; }

/* ── Item Cards (Pantry Grid) ─────────────────────────────── */
.item-card {
  background: var(--surface); border-radius: var(--radius);
  padding: 1rem 1.25rem; box-shadow: var(--shadow);
  border: 1px solid var(--border); margin-bottom: 12px;
  transition: box-shadow .15s;
}
.item-card:hover { box-shadow: var(--shadow-md); }
.item-card-top {
  display: flex; justify-content: space-between;
  align-items: flex-start; margin-bottom: 8px;
}
.item-name { font-size: 0.95rem; font-weight: 700; color: var(--text); }
.item-qty  { font-size: 0.78rem; color: var(--muted); margin-top: 2px; }
.item-meta { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }

/* ── Badges ───────────────────────────────────────────────── */
.badge {
  display: inline-flex; align-items: center;
  padding: 2px 10px; border-radius: 99px;
  font-size: 0.72rem; font-weight: 600; letter-spacing: 0.2px;
  white-space: nowrap;
}
.badge-fresh   { background: var(--success-light); color: #065F46; }
.badge-soon    { background: var(--warning-light); color: #92400E; }
.badge-low     { background: #FEE4CC; color: #9A3412; }
.badge-expired { background: var(--danger-light);  color: #991B1B; }
.badge-primary { background: var(--primary-light); color: var(--primary-dark); }
.badge-gray    { background: #F1F5F9; color: var(--muted); }

/* ── Shelf Life Bar ───────────────────────────────────────── */
.shelf-bar-wrap { margin: 8px 0 4px; }
.shelf-bar-bg {
  background: #F1F5F9; border-radius: 99px; height: 6px; overflow: hidden;
}
.shelf-bar-fill {
  height: 100%; border-radius: 99px;
  transition: width .4s ease;
}
.shelf-bar-fill.fresh   { background: var(--success); }
.shelf-bar-fill.soon    { background: var(--warning); }
.shelf-bar-fill.low     { background: #FB923C; }
.shelf-bar-fill.expired { background: var(--danger); }
.shelf-days { font-size: 0.75rem; color: var(--muted); margin-top: 3px; }

/* ── Upload Zone ──────────────────────────────────────────── */
.upload-zone {
  border: 2px dashed #C7D2FE; border-radius: var(--radius);
  padding: 3rem 2rem; text-align: center;
  background: var(--primary-light); transition: border-color .15s;
}
.upload-zone:hover { border-color: var(--primary); }
.upload-icon { font-size: 2.5rem; margin-bottom: 12px; }
.upload-text { font-size: 1rem; font-weight: 600; color: var(--primary); }
.upload-sub  { font-size: 0.82rem; color: #818CF8; margin-top: 4px; }

/* ── Wizard Steps ─────────────────────────────────────────── */
.wizard-steps {
  display: flex; align-items: center;
  gap: 0; margin-bottom: 2rem; background: var(--surface);
  border-radius: var(--radius); padding: 1rem 1.5rem;
  box-shadow: var(--shadow); overflow: hidden;
}
.wizard-step {
  display: flex; align-items: center; gap: 8px;
  font-size: 0.82rem; font-weight: 500; color: var(--muted);
  flex: 1; position: relative;
}
.wizard-step.active { color: var(--primary); }
.wizard-step.done   { color: var(--success); }
.step-num {
  width: 26px; height: 26px; border-radius: 50%;
  background: var(--border); color: var(--muted);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem; font-weight: 700; flex-shrink: 0;
}
.wizard-step.active .step-num { background: var(--primary); color: #fff; }
.wizard-step.done   .step-num { background: var(--success); color: #fff; }
.step-sep { width: 100%; height: 1px; background: var(--border); margin: 0 8px; }

/* ── Recipe Cards ─────────────────────────────────────────── */
.recipe-card {
  background: var(--surface); border-radius: var(--radius);
  box-shadow: var(--shadow); overflow: hidden; margin-bottom: 1.5rem;
  border: 1px solid var(--border);
}
.recipe-header {
  background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
  padding: 1.25rem 1.5rem; color: #fff;
}
.recipe-title { font-size: 1.15rem; font-weight: 700; color: #fff !important; margin: 0; }
.recipe-time  { font-size: 0.8rem; color: #C7D2FE; margin-top: 4px; }
.recipe-body  { padding: 1.25rem 1.5rem; }
.recipe-ingredients { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 1rem; }
.recipe-steps ol { padding-left: 1.25rem; margin: 0; }
.recipe-steps li { font-size: 0.88rem; color: var(--text); margin-bottom: 6px; line-height: 1.5; }
.recipe-tip {
  background: #FFFBEB; border-left: 3px solid var(--warning);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  padding: 10px 14px; font-size: 0.82rem; color: #78350F;
  margin-top: 1rem;
}

/* ── Shopping List ────────────────────────────────────────── */
.shop-item {
  display: flex; align-items: center; gap: 12px;
  padding: 12px 16px; background: var(--surface);
  border-radius: var(--radius-sm); border: 1px solid var(--border);
  margin-bottom: 8px; transition: opacity .2s;
}
.shop-item.bought { opacity: .45; }
.shop-item-name { font-size: 0.9rem; font-weight: 600; }
.shop-item-meta { font-size: 0.78rem; color: var(--muted); }

/* ── Alert Cards (Running Low) ────────────────────────────── */
.alert-card {
  background: var(--surface); border-radius: var(--radius);
  border-left: 4px solid var(--danger); padding: 1rem 1.25rem;
  box-shadow: var(--shadow); margin-bottom: 12px;
}
.alert-card.warn { border-left-color: var(--warning); }
.alert-name  { font-size: 1rem; font-weight: 700; }
.alert-meta  { font-size: 0.8rem; color: var(--muted); margin-top: 2px; }
.alert-countdown {
  font-size: 1.5rem; font-weight: 800;
  color: var(--danger); line-height: 1;
}
.alert-countdown.warn { color: var(--warning); }

/* ── Form Styles ──────────────────────────────────────────── */
.section-title {
  font-size: 0.75rem; font-weight: 700; letter-spacing: 1px;
  text-transform: uppercase; color: var(--muted); margin-bottom: 12px;
}

/* ── Buttons (override Streamlit) ────────────────────────── */
.stButton > button {
  border-radius: var(--radius-sm) !important;
  font-weight: 600 !important; font-size: 0.875rem !important;
  transition: all .15s !important;
}
.stButton > button[kind="primary"] {
  background: var(--primary) !important;
  border-color: var(--primary) !important;
}
.stButton > button[kind="primary"]:hover {
  background: var(--primary-dark) !important;
  border-color: var(--primary-dark) !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(99,102,241,.35) !important;
}

/* ── Streamlit widget overrides ───────────────────────────── */
.stTextInput > div > div { border-radius: var(--radius-sm) !important; }
.stSelectbox > div > div { border-radius: var(--radius-sm) !important; }
div[data-testid="stMetricValue"] { font-size: 1.5rem !important; font-weight: 800 !important; }
</style>
"""
