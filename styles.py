"""
styles.py — HomeBrain AI design system. Modern & vibrant.
"""

def get_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Syne:wght@700;800&display=swap');

/* ── Design Tokens ────────────────────────────────────────── */
:root {
  --primary:       #C0392B;
  --primary-dark:  #922B21;
  --primary-light: #FDEAEA;
  --accent:        #E67E22;
  --accent2:       #8E44AD;

  --success:       #27AE60;
  --success-light: #D5F5E3;
  --warning:       #E67E22;
  --warning-light: #FDEBD0;
  --danger:        #C0392B;
  --danger-light:  #FDEAEA;

  --bg:            #F0EDE8;
  --surface:       #FFFFFF;
  --surface-low:   #F8F5F1;
  --surface-mid:   #EDE8E0;
  --border:        #E0D9D0;

  --text:          #1A1008;
  --text-muted:    #6B5A4E;
  --text-light:    #A89080;

  --sidebar-bg:    #160C08;

  --grad:          linear-gradient(135deg, #C0392B 0%, #E67E22 100%);
  --grad-green:    linear-gradient(135deg, #27AE60 0%, #2ECC71 100%);
  --grad-warm:     linear-gradient(135deg, #E67E22 0%, #C0392B 100%);
  --grad-cool:     linear-gradient(135deg, #8E44AD 0%, #C0392B 100%);

  --radius:        18px;
  --radius-sm:     12px;
  --radius-xs:     8px;
  --radius-full:   9999px;

  --shadow:     0 2px 12px rgba(26,10,8,.08), 0 1px 3px rgba(0,0,0,.05);
  --shadow-md:  0 8px 32px rgba(192,57,43,.14), 0 2px 8px rgba(0,0,0,.06);
  --shadow-lg:  0 20px 60px rgba(26,10,8,.18);
  --glow-red:   0 0 24px rgba(192,57,43,.35);
  --glow-green: 0 0 20px rgba(39,174,96,.3);
}

/* ── Base ─────────────────────────────────────────────────── */
html, body, [class*="css"] {
  font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
  color: var(--text);
  background: var(--bg) !important;
}
h1,h2,h3,.page-title { font-family: 'Syne', sans-serif !important; }

#MainMenu, footer, .stDeployButton { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
.main .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1100px; }

/* ── Sidebar ──────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
  background: var(--sidebar-bg) !important;
  border-right: 1px solid rgba(255,255,255,.06);
}
section[data-testid="stSidebar"] * { color: #D4A08A !important; }

.sidebar-brand {
  font-family: 'Syne', sans-serif !important;
  font-size: 1.3rem;
  font-weight: 800;
  background: var(--grad);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
}
.sidebar-tagline { font-size: 0.72rem; color: #5A3828 !important; margin-top: 2px; }
.sidebar-divider { border-color: rgba(255,255,255,.07) !important; }

section[data-testid="stSidebar"] .stButton > button {
  border-radius: var(--radius-xs) !important;
  font-weight: 600 !important;
  font-size: 0.86rem !important;
  text-align: left !important;
  background: transparent !important;
  border: none !important;
  color: #A87060 !important;
  padding: 10px 14px !important;
  transition: all .2s !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(192,57,43,.15) !important;
  color: #F5D0C0 !important;
  transform: translateX(3px) !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
  background: linear-gradient(135deg,#922B21,#C0392B) !important;
  color: #FFF0EC !important;
  box-shadow: 0 4px 14px rgba(192,57,43,.45) !important;
}

.stat-pill {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 7px 12px;
  border-radius: var(--radius-xs);
  margin-bottom: 6px;
  background: rgba(192,57,43,.08);
  font-size: 0.78rem;
  border: 1px solid rgba(192,57,43,.14);
}
.stat-pill .label { color: #6B3828 !important; }
.stat-pill .value { font-weight: 700; color: #E0907A !important; }
.stat-pill .value.warn   { color: #E8A060 !important; }
.stat-pill .value.danger { color: #E87070 !important; }

/* ── Page Header ──────────────────────────────────────────── */
.page-header { margin-bottom: 1.5rem; }
.page-title {
  font-size: 2.2rem;
  font-weight: 800;
  background: var(--grad);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -1px;
  margin: 0;
  font-family: 'Syne', sans-serif !important;
}
.page-sub { font-size: 0.88rem; color: var(--text-muted); margin-top: 5px; font-weight: 400; }

/* ── Hero Stat Cards ──────────────────────────────────────── */
.hero-row { display: flex; gap: 14px; margin-bottom: 1.5rem; flex-wrap: wrap; }
.hero-card {
  flex: 1; min-width: 130px;
  border-radius: var(--radius);
  padding: 1.3rem 1.4rem;
  transition: transform .25s, box-shadow .25s;
  position: relative;
  overflow: hidden;
  border: none;
  /* Default: clean white glass */
  background: var(--surface);
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
}
.hero-card:hover { transform: translateY(-5px) scale(1.02); box-shadow: var(--shadow-md); }

/* Coloured variants */
.hero-card.primary {
  background: linear-gradient(145deg, #C0392B 0%, #E8503A 60%, #E67E22 100%);
  box-shadow: 0 8px 32px rgba(192,57,43,.45);
  border: none;
}
.hero-card.success {
  background: linear-gradient(145deg, #1A8A48 0%, #27AE60 60%, #52D68A 100%);
  box-shadow: 0 8px 32px rgba(39,174,96,.4);
  border: none;
}
.hero-card.warning {
  background: linear-gradient(145deg, #B05010 0%, #E67E22 60%, #F0A050 100%);
  box-shadow: 0 8px 32px rgba(230,126,34,.4);
  border: none;
}
.hero-card.danger {
  background: linear-gradient(145deg, #7A1818 0%, #C0392B 60%, #E05050 100%);
  box-shadow: 0 8px 32px rgba(192,57,43,.45);
  border: none;
}

/* Glossy overlay on coloured cards */
.hero-card.primary::after,
.hero-card.success::after,
.hero-card.warning::after,
.hero-card.danger::after {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 50%;
  background: linear-gradient(180deg, rgba(255,255,255,.18) 0%, rgba(255,255,255,0) 100%);
  border-radius: var(--radius) var(--radius) 0 0;
  pointer-events: none;
}

.hero-card .hc-icon { font-size: 1.8rem; margin-bottom: 10px; filter: drop-shadow(0 3px 6px rgba(0,0,0,.25)); }
.hero-card .hc-value {
  font-size: 2.6rem; font-weight: 800; line-height: 1; margin-bottom: 4px;
  font-family: 'Syne', sans-serif;
  color: var(--text);
}
.hero-card.primary .hc-value,
.hero-card.success .hc-value,
.hero-card.warning .hc-value,
.hero-card.danger  .hc-value { color: #fff; text-shadow: 0 2px 8px rgba(0,0,0,.2); }
.hero-card .hc-label { font-size: 0.78rem; font-weight: 600; color: var(--text-muted); }
.hero-card.primary .hc-label,
.hero-card.success .hc-label,
.hero-card.warning .hc-label,
.hero-card.danger  .hc-label { color: rgba(255,255,255,.8); }

/* ── Badges ───────────────────────────────────────────────── */
.badge {
  display: inline-flex; align-items: center;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  font-size: 0.7rem; font-weight: 700; letter-spacing: 0.3px; white-space: nowrap;
}
.badge-fresh   { background: var(--success-light); color: #1A7040; }
.badge-soon    { background: var(--warning-light); color: #8A4010; }
.badge-low     { background: var(--danger-light);  color: #8A1818; }
.badge-expired { background: var(--danger-light);  color: #8A1818; }
.badge-primary { background: var(--primary-light); color: var(--primary); }
.badge-gray    { background: var(--surface-mid);   color: var(--text-muted); }

/* ── Product Thumbnail ────────────────────────────────────── */
.mh-img .item-thumb { width:80px !important; height:80px !important; border-radius:14px !important; margin-bottom:8px; }
.item-thumb {
  width: 72px; height: 72px;
  border-radius: 14px;
  object-fit: cover;
  flex-shrink: 0;
  background: var(--surface-low);
  box-shadow: 0 6px 16px rgba(0,0,0,.18), 0 2px 4px rgba(0,0,0,.1);
  transition: transform .2s;
}
.item-thumb:hover { transform: scale(1.07) rotate(1deg); }
.item-thumb-emoji { display: flex; align-items: center; justify-content: center; font-size: 1.8rem; }

/* ── Item Cards ───────────────────────────────────────────── */
.item-card {
  background: var(--surface);
  border-radius: var(--radius);
  padding: 1rem 1.1rem;
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
  margin-bottom: 14px;
  transition: box-shadow .22s, transform .22s;
  position: relative;
}
.item-card:hover { box-shadow: var(--shadow-md); transform: translateY(-3px); }
.card-del {
  position: absolute; top: 9px; right: 10px;
  width: 22px; height: 22px; border-radius: 50%;
  background: var(--danger-light); color: var(--danger);
  font-size: 0.72rem; font-weight: 700;
  text-decoration: none; display: flex; align-items: center; justify-content: center;
  opacity: 0; transition: opacity .15s, transform .15s; line-height: 1;
}
.item-card:hover .card-del { opacity: 1; transform: scale(1.1); }
.item-card-top { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
.item-name { font-size: 0.9rem; font-weight: 700; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.item-qty  { font-size: 0.75rem; color: var(--text-muted); margin-top: 2px; }
.item-meta { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }
.item-prediction {
  font-size: 0.7rem; color: var(--primary); background: var(--primary-light);
  border-radius: 5px; padding: 3px 8px; margin-top: 6px; display: inline-block; font-weight: 600;
}

/* ── Shelf Life Bar ───────────────────────────────────────── */
.shelf-bar-bg { background: var(--surface-mid); border-radius: var(--radius-full); height: 5px; overflow: hidden; }
.shelf-bar-fill { height: 100%; border-radius: var(--radius-full); transition: width .5s cubic-bezier(.4,0,.2,1); }
.shelf-bar-fill.fresh   { background: linear-gradient(90deg, #27AE60, #52D68A); }
.shelf-bar-fill.soon    { background: linear-gradient(90deg, #E67E22, #F0A050); }
.shelf-bar-fill.low     { background: linear-gradient(90deg, #C0392B, #E05050); }
.shelf-bar-fill.expired { background: linear-gradient(90deg, #7A1818, #C0392B); }
.shelf-days { font-size: 0.7rem; color: var(--text-muted); margin-top: 3px; font-weight: 600; }

/* ── Upload Zone ──────────────────────────────────────────── */
.upload-zone {
  border: 2px dashed var(--border); border-radius: var(--radius);
  padding: 3rem 2rem; text-align: center; background: var(--surface-low); transition: all .2s;
}
.upload-zone:hover { border-color: var(--primary); background: var(--primary-light); transform: scale(1.01); }
.upload-icon { font-size: 2.5rem; margin-bottom: 12px; }
.upload-text { font-size: 1rem; font-weight: 700; color: var(--primary); font-family: 'Syne', sans-serif; }
.upload-sub  { font-size: 0.82rem; color: var(--text-muted); margin-top: 4px; }

/* ── Wizard Steps ─────────────────────────────────────────── */
.wizard-steps { display: flex; align-items: center; margin-bottom: 2rem; background: var(--surface); border-radius: var(--radius); padding: 1rem 1.5rem; box-shadow: var(--shadow); border: 1px solid var(--border); }
.wizard-step  { display: flex; align-items: center; gap: 8px; font-size: 0.82rem; font-weight: 500; color: var(--text-muted); flex: 1; }
.wizard-step.active { color: var(--primary); }
.wizard-step.done   { color: var(--success); }
.step-num { width: 26px; height: 26px; border-radius: var(--radius-full); background: var(--surface-mid); color: var(--text-muted); display: flex; align-items: center; justify-content: center; font-size: 0.72rem; font-weight: 700; flex-shrink: 0; }
.wizard-step.active .step-num { background: var(--grad); color: #fff; }
.wizard-step.done   .step-num { background: var(--grad-green); color: #fff; }
.step-sep { flex: 1; height: 1px; background: var(--border); margin: 0 8px; }

/* ── Recipe Box (pantry box view) ────────────────────────── */
.recipe-box-wrap {
  background: linear-gradient(160deg, #3A1A08 0%, #2A1005 50%, #1A0804 100%);
  border-radius: 20px;
  padding: 0 20px 0;
  box-shadow: 0 12px 48px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.07);
  overflow: visible;
  margin-bottom: 8px;
}
.recipe-box-cards {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  padding: 28px 8px 0;
  min-height: 160px;
  align-items: flex-end;
}
.box-card {
  background: linear-gradient(180deg, #FFFEF9 0%, #FFF8EC 100%);
  border-radius: 10px 10px 2px 2px;
  width: 88px;
  padding: 10px 7px 10px;
  display: flex; flex-direction: column; align-items: center; text-align: center;
  box-shadow: 3px 3px 14px rgba(0,0,0,.35), inset 0 1px 0 rgba(255,255,255,.9);
  cursor: pointer;
  transition: transform .3s cubic-bezier(.34,1.56,.64,1), box-shadow .3s;
  position: relative;
}
.box-card:hover {
  transform: translateY(-36px) rotate(-1.5deg) scale(1.06);
  box-shadow: 6px 20px 40px rgba(0,0,0,.5);
  z-index: 20;
}
.box-card .bc-img .item-thumb { width:52px !important; height:52px !important; border-radius:10px !important; margin-bottom:0; }
.bc-name { font-size: 0.68rem; font-weight: 700; color: #1A0808; margin-top: 6px; line-height: 1.2; }
.bc-days { font-size: 0.62rem; font-weight: 800; margin-top: 3px; }
.recipe-box-body {
  height: 22px;
  display: flex; align-items: center; justify-content: center;
  padding-bottom: 10px;
  margin-top: 6px;
}
.rbox-label { font-size: 0.65rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: rgba(200,160,100,.6); }

/* ── Wooden Shelf (pantry shelf view) ────────────────────── */
.shelf-unit { margin-bottom: 20px; }
.shelf-cat-label { font-size: 0.65rem; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px; padding-left: 4px; }
.shelf-row {
  display: flex; flex-wrap: wrap; gap: 10px;
  padding: 8px 12px 0;
  background: linear-gradient(180deg, rgba(26,8,4,.25) 0%, transparent 60%);
  min-height: 110px; align-items: flex-end;
}
.shelf-plank {
  background: linear-gradient(180deg, #7A3A18 0%, #6B3010 20%, #7A3A18 50%, #5C2808 100%);
  height: 14px; border-radius: 4px;
  box-shadow: 0 8px 20px rgba(0,0,0,.55), inset 0 2px 4px rgba(255,220,160,.15), inset 0 -2px 3px rgba(0,0,0,.4);
  position: relative; overflow: hidden;
}
.shelf-plank::after {
  content: '';
  position: absolute; top: 4px; left: 0; right: 0; height: 1px;
  background: repeating-linear-gradient(90deg, transparent 0, transparent 40px, rgba(255,200,120,.08) 40px, rgba(255,200,120,.08) 80px);
}
.shelf-tile {
  background: linear-gradient(180deg, #FFFEF9 0%, #FFF5E8 100%);
  border-radius: 10px 10px 3px 3px;
  border-top: 3px solid var(--top-color, #C0392B);
  width: 82px; min-height: 100px;
  padding: 9px 6px 8px;
  display: flex; flex-direction: column; align-items: center; text-align: center;
  box-shadow: 2px 6px 18px rgba(0,0,0,.3), inset 0 1px 0 rgba(255,255,255,.9);
  transition: transform .25s cubic-bezier(.34,1.56,.64,1);
  cursor: default;
}
.shelf-tile:hover { transform: translateY(-10px) rotate(1deg); }
.shelf-tile .st-img .item-thumb { width:50px !important; height:50px !important; border-radius:9px !important; }
.st-name { font-size: 0.65rem; font-weight: 700; color: #1A0808; margin-top: 5px; line-height: 1.2; }
.st-days { font-size: 0.6rem; font-weight: 800; margin-top: 4px; padding: 2px 6px; border-radius: 99px; }
.st-days.fresh   { background: #D5F5E3; color: #1A7040; }
.st-days.soon    { background: #FDEBD0; color: #8A4010; }
.st-days.low     { background: #FDEAEA; color: #8A1818; }
.st-days.expired { background: #FDEAEA; color: #8A1818; }

/* ── Recipe Cards ─────────────────────────────────────────── */
.recipe-card { background: var(--surface); border-radius: var(--radius); box-shadow: var(--shadow-md); overflow: hidden; margin-bottom: 1.5rem; border: 1px solid var(--border); }
.recipe-header { background: var(--grad); padding: 1.4rem 1.5rem; }
.recipe-title  { font-size: 1.2rem; font-weight: 700; color: #fff !important; margin: 0; font-family: 'Syne', sans-serif; }
.recipe-time   { font-size: 0.78rem; color: rgba(255,255,255,.75); margin-top: 4px; }
.recipe-body   { padding: 1.2rem 1.5rem; }
.recipe-ingredients { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 1rem; }
.recipe-steps li { font-size: 0.88rem; color: var(--text); margin-bottom: 6px; line-height: 1.55; }
.recipe-tip { background: var(--warning-light); border-left: 3px solid var(--warning); border-radius: 0 var(--radius-xs) var(--radius-xs) 0; padding: 10px 14px; font-size: 0.82rem; color: #7A4010; margin-top: 1rem; }

/* ── Alert Cards ──────────────────────────────────────────── */
.alert-card { background: var(--surface); border-radius: var(--radius); border-left: 4px solid var(--danger); padding: 1rem 1.2rem; box-shadow: var(--shadow); margin-bottom: 12px; transition: transform .2s, box-shadow .2s; }
.alert-card:hover { transform: translateX(3px); box-shadow: var(--shadow-md); }
.alert-card.warn { border-left-color: var(--warning); }
.alert-name  { font-size: 0.95rem; font-weight: 700; color: var(--text); }
.alert-meta  { font-size: 0.76rem; color: var(--text-muted); margin-top: 2px; }
.alert-countdown { font-size: 1.5rem; font-weight: 800; color: var(--danger); line-height: 1; font-family: 'Syne', sans-serif; }
.alert-countdown.warn { color: var(--warning); }

/* ── Section Title ────────────────────────────────────────── */
.section-title {
  font-size: 0.65rem; font-weight: 700; letter-spacing: 2.5px;
  text-transform: uppercase; color: var(--text-muted);
  margin-bottom: 14px; border-bottom: 1px solid var(--border); padding-bottom: 8px;
}

/* ── Buttons ──────────────────────────────────────────────── */
.stButton > button {
  border-radius: var(--radius-xs) !important;
  font-weight: 600 !important; font-size: 0.875rem !important;
  transition: all .2s !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stButton > button[kind="primary"] {
  background: var(--grad) !important;
  border: none !important; color: #fff !important;
  box-shadow: 0 4px 16px rgba(192,57,43,.35) !important;
}
.stButton > button[kind="primary"]:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px rgba(192,57,43,.5) !important;
}

/* ── Streamlit overrides ──────────────────────────────────── */
.stTextInput > div > div,
.stSelectbox > div > div,
.stTextArea > div { border-radius: var(--radius-xs) !important; border-color: var(--border) !important; }
[data-testid="stDataFrame"]  { border-radius: var(--radius) !important; overflow: hidden; box-shadow: var(--shadow); }
[data-testid="stExpander"]   { border-radius: var(--radius-sm) !important; border: 1px solid var(--border) !important; background: var(--surface) !important; }
[data-testid="stTabs"] [role="tab"][aria-selected="true"] { color: var(--primary) !important; border-bottom-color: var(--primary) !important; font-weight: 700 !important; }

/* ── Pantry Shelf ─────────────────────────────────────────── */
.pantry-unit { background: linear-gradient(180deg,#1C0A08 0%,#2C1410 100%); border-radius: var(--radius); padding: 20px 20px 8px; box-shadow: var(--shadow-lg); }
.shelf-category-label { font-size: 0.66rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #D4907A; margin-bottom: 8px; padding-left: 4px; display: flex; align-items: center; gap: 6px; }
.shelf-items-row { display: flex; flex-wrap: wrap; gap: 12px; padding: 10px 8px 14px; min-height: 90px; align-items: flex-end; }
.shelf-plank { background: linear-gradient(180deg,#5C2A18 0%,#3C1608 100%); height: 8px; border-radius: 3px; box-shadow: 0 5px 10px rgba(0,0,0,.5); margin-bottom: 20px; }
.product-tile { background: var(--surface); border-radius: var(--radius-sm); padding: 10px 8px 8px; width: 100px; min-height: 88px; display: flex; flex-direction: column; align-items: center; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,.2); position: relative; transition: transform .2s, box-shadow .2s; border-top: 3px solid var(--primary); }
.product-tile:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,.22); }
.product-tile.status-low     { border-top-color: var(--danger); }
.product-tile.status-expired { border-top-color: var(--danger); }
.product-tile.status-soon    { border-top-color: var(--warning); }
.product-tile.status-fresh   { border-top-color: var(--success); }
.product-tile .pt-icon { font-size: 1.75rem; margin-bottom: 4px; line-height: 1; }
.product-tile .pt-name { font-size: 0.7rem; font-weight: 700; color: var(--text); line-height: 1.2; }
.product-tile .pt-qty  { font-size: 0.62rem; color: var(--text-muted); margin-top: 3px; }
.product-tile .pt-days { font-size: 0.62rem; font-weight: 700; margin-top: 5px; padding: 2px 7px; border-radius: var(--radius-full); }
.pt-days.fresh   { background: var(--success-light); color: #1A7040; }
.pt-days.soon    { background: var(--warning-light); color: #8A4010; }
.pt-days.low     { background: var(--danger-light);  color: #8A1818; }
.pt-days.expired { background: var(--danger-light);  color: #8A1818; }
</style>
"""
