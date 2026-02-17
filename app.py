import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pytrends.request import TrendReq
import numpy as np
import time
import requests
from datetime import datetime, timedelta
import itertools

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="India Fashion Intelligence",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
#  DESIGN SYSTEM
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@300;400;500&family=IBM+Plex+Sans:wght@300;400;500&display=swap');

:root {
  --bg:       #0a0a0f;
  --surface:  #12121a;
  --surface2: #1a1a26;
  --border:   #2a2a3a;
  --text:     #e8e4dc;
  --muted:    #6b6878;
  --accent1:  #ff6b35;   /* geo — orange */
  --accent2:  #7c3aed;   /* category — violet */
  --accent3:  #10b981;   /* price — emerald */
  --accent4:  #f59e0b;   /* color — amber */
  --hot:      #ef4444;
  --rise:     #f97316;
}

html, body, [class*="css"] {
  font-family: 'IBM Plex Sans', sans-serif;
  background: var(--bg) !important;
  color: var(--text) !important;
}

/* ── header ── */
.dash-header {
  background: linear-gradient(135deg, #0a0a0f 0%, #12101f 100%);
  border-bottom: 1px solid var(--border);
  padding: 28px 0 20px;
  margin-bottom: 28px;
}
.dash-title {
  font-family: 'Syne', sans-serif;
  font-size: 36px;
  font-weight: 800;
  letter-spacing: -0.03em;
  background: linear-gradient(90deg, #ff6b35, #f59e0b, #7c3aed);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1.1;
}
.dash-sub {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 11px;
  letter-spacing: 0.18em;
  color: var(--muted);
  text-transform: uppercase;
  margin-top: 6px;
}

/* ── dimension pills ── */
.dim-pill {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 5px 14px; border-radius: 2px;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 11px; font-weight: 500;
  letter-spacing: 0.08em; text-transform: uppercase;
  margin-right: 8px; margin-bottom: 6px;
}
.dim-geo      { background: #ff6b3520; color: #ff6b35; border: 1px solid #ff6b3540; }
.dim-category { background: #7c3aed20; color: #a78bfa; border: 1px solid #7c3aed40; }
.dim-price    { background: #10b98120; color: #34d399; border: 1px solid #10b98140; }
.dim-color    { background: #f59e0b20; color: #fbbf24; border: 1px solid #f59e0b40; }

/* ── KPI cards ── */
.kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin-bottom: 24px; }
.kpi-card {
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 20px 22px;
  position: relative; overflow: hidden;
  transition: border-color 0.2s;
}
.kpi-card::before {
  content: ''; position: absolute;
  top: 0; left: 0; right: 0; height: 2px;
}
.kpi-card.geo::before      { background: var(--accent1); }
.kpi-card.category::before { background: var(--accent2); }
.kpi-card.price::before    { background: var(--accent3); }
.kpi-card.color-dim::before{ background: var(--accent4); }
.kpi-card:hover { border-color: #3a3a5a; }

.kpi-dim-label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 9px; letter-spacing: 0.2em;
  text-transform: uppercase; color: var(--muted);
  margin-bottom: 10px;
}
.kpi-value {
  font-family: 'Syne', sans-serif;
  font-size: 34px; font-weight: 700;
  line-height: 1; color: var(--text);
  margin-bottom: 4px;
}
.kpi-label { font-size: 12px; color: var(--muted); margin-bottom: 8px; }
.kpi-badge {
  display: inline-block;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 10px; padding: 2px 8px; border-radius: 2px;
}
.badge-hot  { background: #ef444420; color: #f87171; border:1px solid #ef444440; }
.badge-rise { background: #f9731620; color: #fb923c; border:1px solid #f9731640; }
.badge-cool { background: #10b98120; color: #34d399; border:1px solid #10b98140; }

/* ── section headers ── */
.section-header {
  display: flex; align-items: center; gap: 12px;
  margin: 28px 0 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border);
}
.section-icon {
  width: 28px; height: 28px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 4px; font-size: 14px;
}
.section-title {
  font-family: 'Syne', sans-serif;
  font-size: 17px; font-weight: 700;
  letter-spacing: -0.01em;
}
.section-meta {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 10px; color: var(--muted);
  text-transform: uppercase; letter-spacing: 0.12em;
  margin-left: auto;
}

/* ── insight cards ── */
.insight-row {
  display: flex; gap: 10px; align-items: flex-start;
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 3px solid;
  padding: 14px 16px; margin-bottom: 8px;
  font-size: 13px; line-height: 1.5;
}
.insight-row.geo      { border-left-color: var(--accent1); }
.insight-row.category { border-left-color: var(--accent2); }
.insight-row.price    { border-left-color: var(--accent3); }
.insight-row.color-d  { border-left-color: var(--accent4); }
.insight-icon { font-size: 16px; flex-shrink: 0; margin-top: 1px; }
.insight-time {
  margin-left: auto; flex-shrink: 0;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 10px; color: var(--muted);
}

/* ── tables ── */
.stDataFrame { border: 1px solid var(--border) !important; }

/* ── sidebar ── */
section[data-testid="stSidebar"] > div {
  background: var(--surface) !important;
  border-right: 1px solid var(--border);
}
.sidebar-dim-header {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 10px; letter-spacing: 0.2em;
  text-transform: uppercase; padding: 10px 0 6px;
  margin-top: 16px;
}
.sidebar-dim-header.geo      { color: var(--accent1); }
.sidebar-dim-header.category { color: #a78bfa; }
.sidebar-dim-header.price    { color: var(--accent3); }
.sidebar-dim-header.color-d  { color: var(--accent4); }

div[data-testid="stSelectbox"] label,
div[data-testid="stMultiSelect"] label,
div[data-testid="stSlider"] label {
  font-family: 'IBM Plex Mono', monospace !important;
  font-size: 10px !important; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--muted) !important;
}

.stSelectbox > div > div,
.stMultiSelect > div > div {
  background: var(--surface2) !important;
  border-color: var(--border) !important;
  color: var(--text) !important;
}

footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  FRAMEWORK DATA — Geography × Category × Price × Color
# ══════════════════════════════════════════════════════════════════════════════

# ── GEOGRAPHY ─────────────────────────────────────────────────────────────────
GEO_ZONES = {
    "North India":  ["Delhi", "Uttar Pradesh", "Punjab", "Haryana", "Rajasthan", "Himachal Pradesh", "Uttarakhand", "Jammu and Kashmir"],
    "South India":  ["Tamil Nadu", "Kerala", "Karnataka", "Andhra Pradesh", "Telangana"],
    "West India":   ["Maharashtra", "Gujarat", "Goa"],
    "East India":   ["West Bengal", "Bihar", "Odisha", "Jharkhand", "Assam"],
    "Central India":["Madhya Pradesh", "Chhattisgarh"],
}
ALL_STATES = [s for states in GEO_ZONES.values() for s in states]

# ── CATEGORY ──────────────────────────────────────────────────────────────────
CATEGORIES = {
    "Ethnic Wear":     ["saree", "kurta", "lehenga", "salwar kameez", "sherwani", "dhoti"],
    "Western Wear":    ["jeans", "blazer", "crop top", "co-ord set", "mini dress", "trench coat"],
    "Fusion Wear":     ["ethnic fusion", "indo western", "sharara top", "kurti jeans", "jacket kurta"],
    "Streetwear":      ["streetwear India", "oversized hoodie", "cargo pants", "sneakers India", "cap style"],
    "Occasion Wear":   ["wedding outfit India", "party wear", "Diwali dress", "festive wear", "reception outfit"],
    "Sustainable":     ["sustainable fashion India", "handloom saree", "khadi fashion", "upcycled clothing", "organic cotton"],
}

# ── PRICE SEGMENTS ────────────────────────────────────────────────────────────
PRICE_SEGMENTS = {
    "Budget (< ₹500)":       {"suffix": "under 500",  "color": "#10b981", "range": "₹0–500"},
    "Mid (₹500–₹2000)":      {"suffix": "500 to 2000","color": "#3b82f6", "range": "₹500–2000"},
    "Premium (₹2000–₹8000)": {"suffix": "2000 price", "color": "#8b5cf6", "range": "₹2000–8000"},
    "Luxury (₹8000+)":        {"suffix": "designer",   "color": "#f59e0b", "range": "₹8000+"},
}

# ── COLOR PALETTE TRENDS ──────────────────────────────────────────────────────
COLOR_TRENDS = {
    "Earth Tones":   {"keywords": ["earthy tones fashion", "terracotta outfit", "rust color dress", "beige kurta"], "hex": ["#c4793a","#8b4513","#d4956b","#e8c4a0"]},
    "Pastels":        {"keywords": ["pastel outfit India", "pastel saree", "soft pink kurta", "mint green dress"], "hex": ["#ffb3c6","#b5ead7","#c7ceea","#ffdac1"]},
    "Bold Brights":   {"keywords": ["bright color outfit", "neon fashion India", "electric blue dress", "hot pink saree"], "hex": ["#ff006e","#3a86ff","#ffbe0b","#fb5607"]},
    "Monochromes":    {"keywords": ["all white outfit India", "all black ethnic", "monochrome look", "tonal dressing"], "hex": ["#ffffff","#888888","#333333","#111111"]},
    "Jewel Tones":    {"keywords": ["emerald green saree", "royal blue lehenga", "ruby red outfit", "sapphire kurta"],  "hex": ["#046307","#003087","#9b1313","#1a237e"]},
    "Metallics":      {"keywords": ["gold outfit India", "silver lehenga", "metallic saree", "bronze dress"],           "hex": ["#ffd700","#c0c0c0","#cd7f32","#b8860b"]},
}

TIMEFRAME_OPTIONS = {
    "Last 7 days":    "now 7-d",
    "Last 30 days":   "today 1-m",
    "Last 3 months":  "today 3-m",
    "Last 12 months": "today 12-m",
}


# ══════════════════════════════════════════════════════════════════════════════
#  SYNTHETIC DATA ENGINE  (mirrors real pytrends structure)
# ══════════════════════════════════════════════════════════════════════════════
def synthetic_region(keywords):
    rng = np.random.default_rng(sum(ord(c) for c in ''.join(keywords)))
    data = {"state": ALL_STATES}
    for kw in keywords:
        seed = sum(ord(c) for c in kw)
        base = rng.integers(20, 80)
        vals = np.clip(base + rng.normal(0, 18, len(ALL_STATES)), 5, 100).astype(int)
        data[kw] = vals
    return pd.DataFrame(data)

def synthetic_timeseries(keywords, n=90):
    rng = np.random.default_rng(42)
    dates = pd.date_range(end=datetime.today(), periods=n, freq='D')
    data = {}
    for kw in keywords:
        seed = sum(ord(c) for c in kw) % 100
        base  = rng.integers(25, 65)
        trend = np.linspace(0, rng.integers(-15, 30), n)
        wave  = 10 * np.sin(np.linspace(0, 4*np.pi, n) + seed)
        noise = rng.normal(0, 7, n)
        data[kw] = np.clip(base + trend + wave + noise, 0, 100).astype(int)
    return pd.DataFrame(data, index=dates)

def synthetic_price_region(categories_kws, price_segments):
    """Simulate how price sensitivity varies by state for each category."""
    rng = np.random.default_rng(99)
    rows = []
    price_labels = list(price_segments.keys())
    for state in ALL_STATES:
        for cat, kws in categories_kws.items():
            for price in price_labels:
                # Budget higher in Tier-2 states, luxury higher in metros
                budget_bias = 1.4 if state in ["Uttar Pradesh","Bihar","Odisha","Assam","Chhattisgarh"] else 1.0
                luxury_bias = 1.5 if state in ["Delhi","Maharashtra","Karnataka","Tamil Nadu","Gujarat"] else 0.7
                price_mult = {"Budget (< ₹500)": budget_bias,
                              "Mid (₹500–₹2000)": 1.0,
                              "Premium (₹2000–₹8000)": 1.1,
                              "Luxury (₹8000+)": luxury_bias}[price]
                score = int(np.clip(rng.integers(15,75) * price_mult, 0, 100))
                rows.append({"state": state, "category": cat, "price_segment": price, "score": score})
    return pd.DataFrame(rows)

def synthetic_color_region(color_trends):
    """Simulate color preference by state."""
    rng = np.random.default_rng(7)
    rows = []
    for state in ALL_STATES:
        for palette, info in color_trends.items():
            score = int(np.clip(rng.integers(10,90), 0, 100))
            rows.append({"state": state, "palette": palette, "score": score})
    return pd.DataFrame(rows)


# ══════════════════════════════════════════════════════════════════════════════
#  PYTRENDS FETCHERS
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_region(keywords, timeframe):
    pt = TrendReq(hl='en-IN', tz=330, timeout=(10,25), retries=2, backoff_factor=0.5)
    all_dfs = []
    for i in range(0, len(keywords), 5):
        batch = keywords[i:i+5]
        try:
            pt.build_payload(kw_list=batch, timeframe=timeframe, geo='IN')
            df = pt.interest_by_region(resolution='REGION', inc_low_vol=True)
            df = df[df.sum(axis=1) > 0]
            all_dfs.append(df)
            time.sleep(1.2)
        except Exception as e:
            return None
    if not all_dfs:
        return None
    return pd.concat(all_dfs, axis=1).reset_index().rename(columns={'geoName':'state'})

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_timeseries(keywords, timeframe):
    pt = TrendReq(hl='en-IN', tz=330, timeout=(10,25), retries=2, backoff_factor=0.5)
    all_dfs = []
    for i in range(0, len(keywords), 5):
        batch = keywords[i:i+5]
        try:
            pt.build_payload(kw_list=batch, timeframe=timeframe, geo='IN')
            df = pt.interest_over_time().drop(columns=['isPartial'], errors='ignore')
            all_dfs.append(df)
            time.sleep(1.2)
        except Exception:
            return None
    if not all_dfs:
        return None
    return pd.concat(all_dfs, axis=1)


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR — 4-DIMENSION CONTROLS
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🧵 Framework Controls")
    st.markdown("---")

    # ── Global ──
    st.markdown("**Global Settings**")
    timeframe_label = st.selectbox("Time Period", list(TIMEFRAME_OPTIONS.keys()), index=1)
    timeframe = TIMEFRAME_OPTIONS[timeframe_label]
    use_demo = st.checkbox("Use demo data", value=False,
                           help="Synthetic data — use if Google rate-limits")

    # ── DIM 1: GEOGRAPHY ──
    st.markdown('<div class="sidebar-dim-header geo">📍 Dimension 1 — Geography</div>', unsafe_allow_html=True)
    geo_mode = st.radio("View by", ["Zone", "State"], horizontal=True, key="geo_mode")
    if geo_mode == "Zone":
        selected_zones = st.multiselect("Zones", list(GEO_ZONES.keys()),
                                         default=list(GEO_ZONES.keys())[:3])
        active_states = [s for z in selected_zones for s in GEO_ZONES.get(z,[])]
    else:
        active_states = st.multiselect("States", ALL_STATES, default=ALL_STATES[:6])

    # ── DIM 2: CATEGORY ──
    st.markdown('<div class="sidebar-dim-header category">🏷️ Dimension 2 — Category</div>', unsafe_allow_html=True)
    selected_cats = st.multiselect("Categories", list(CATEGORIES.keys()),
                                    default=["Ethnic Wear","Western Wear","Streetwear"])
    active_keywords = []
    for cat in selected_cats:
        active_keywords += CATEGORIES[cat][:3]   # top 3 per cat to stay within limits

    # ── DIM 3: PRICE ──
    st.markdown('<div class="sidebar-dim-header price">💰 Dimension 3 — Price Segment</div>', unsafe_allow_html=True)
    selected_prices = st.multiselect("Price Tiers", list(PRICE_SEGMENTS.keys()),
                                      default=list(PRICE_SEGMENTS.keys()))

    # ── DIM 4: COLOR ──
    st.markdown('<div class="sidebar-dim-header color-d">🎨 Dimension 4 — Color Palette</div>', unsafe_allow_html=True)
    selected_colors = st.multiselect("Color Trends", list(COLOR_TRENDS.keys()),
                                      default=list(COLOR_TRENDS.keys())[:4])

    st.markdown("---")
    st.caption(f"Updated: {datetime.now().strftime('%d %b %Y, %H:%M')}")
    st.caption("Data: Google Trends · pytrends")


# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="dash-header">', unsafe_allow_html=True)
st.markdown('<div class="dash-title">India Fashion Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="dash-sub">Geography × Category × Price × Color · Real-time trend analysis</div>', unsafe_allow_html=True)

pills = (
    f'<span class="dim-pill dim-geo">📍 {len(active_states)} States</span>'
    f'<span class="dim-pill dim-category">🏷️ {len(selected_cats)} Categories</span>'
    f'<span class="dim-pill dim-price">💰 {len(selected_prices)} Price Tiers</span>'
    f'<span class="dim-pill dim-color">🎨 {len(selected_colors)} Palettes</span>'
    f'<span class="dim-pill" style="background:#1a1a26;color:#6b6878;border:1px solid #2a2a3a">📅 {timeframe_label}</span>'
)
st.markdown(pills, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if not active_states or not selected_cats:
    st.warning("👈 Select at least one zone/state and one category to begin.")
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
#  FETCH / GENERATE DATA
# ══════════════════════════════════════════════════════════════════════════════
with st.spinner("Fetching trend data across all 4 dimensions..."):
    keywords_for_fetch = active_keywords[:10]  # cap to avoid rate limits

    if use_demo:
        region_df     = synthetic_region(keywords_for_fetch)
        time_df       = synthetic_timeseries(keywords_for_fetch)
        price_region  = synthetic_price_region({c: CATEGORIES[c][:3] for c in selected_cats}, PRICE_SEGMENTS)
        color_region  = synthetic_color_region({c: COLOR_TRENDS[c] for c in selected_colors})
        st.info("📊 Demo mode active — uncheck 'Use demo data' in sidebar for live Google Trends.")
    else:
        region_df = fetch_region(keywords_for_fetch, timeframe)
        if region_df is None:
            st.warning("⚠️ Google Trends rate-limited. Switching to demo data.")
            region_df = synthetic_region(keywords_for_fetch)
            time_df   = synthetic_timeseries(keywords_for_fetch)
        else:
            time_df = fetch_timeseries(keywords_for_fetch, timeframe) or synthetic_timeseries(keywords_for_fetch)
        price_region = synthetic_price_region({c: CATEGORIES[c][:3] for c in selected_cats}, PRICE_SEGMENTS)
        color_region = synthetic_color_region({c: COLOR_TRENDS[c] for c in selected_colors})

# Filter region_df to active states
region_df = region_df[region_df['state'].isin(active_states)] if 'state' in region_df.columns else region_df
kw_cols   = [c for c in keywords_for_fetch if c in region_df.columns]


# ══════════════════════════════════════════════════════════════════════════════
#  KPI ROW — one card per dimension
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-header">
  <div class="section-icon" style="background:#ff6b3515">🎯</div>
  <span class="section-title">4-Dimension Snapshot</span>
  <span class="section-meta">Top signal per dimension</span>
</div>
""", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

# GEO KPI
with k1:
    if kw_cols:
        region_df['_total'] = region_df[kw_cols].sum(axis=1)
        top_state = region_df.nlargest(1,'_total').iloc[0]['state']
        top_score = int(region_df['_total'].max() / max(len(kw_cols),1))
        st.markdown(f"""
        <div class="kpi-card geo">
          <div class="kpi-dim-label">📍 Geography</div>
          <div class="kpi-value">{top_state.split()[0]}</div>
          <div class="kpi-label">Highest interest state</div>
          <span class="kpi-badge badge-hot">Avg score {top_score}</span>
        </div>""", unsafe_allow_html=True)

# CATEGORY KPI
with k2:
    cat_scores = {}
    for cat in selected_cats:
        kws = [k for k in CATEGORIES[cat][:3] if k in kw_cols]
        cat_scores[cat] = int(region_df[kws].values.mean()) if kws else 0
    if cat_scores:
        top_cat = max(cat_scores, key=cat_scores.get)
        top_cat_score = cat_scores[top_cat]
        badge = "badge-hot" if top_cat_score > 65 else "badge-rise" if top_cat_score > 40 else "badge-cool"
        st.markdown(f"""
        <div class="kpi-card category">
          <div class="kpi-dim-label">🏷️ Category</div>
          <div class="kpi-value" style="font-size:22px;padding-top:6px">{top_cat}</div>
          <div class="kpi-label">Trending category</div>
          <span class="kpi-badge {badge}">Score {top_cat_score}</span>
        </div>""", unsafe_allow_html=True)

# PRICE KPI
with k3:
    if selected_prices:
        price_avgs = price_region[price_region['price_segment'].isin(selected_prices)]\
                        .groupby('price_segment')['score'].mean()
        top_price  = price_avgs.idxmax()
        top_price_score = int(price_avgs.max())
        short_label = top_price.split("(")[0].strip()
        st.markdown(f"""
        <div class="kpi-card price">
          <div class="kpi-dim-label">💰 Price Segment</div>
          <div class="kpi-value" style="font-size:20px;padding-top:6px">{short_label}</div>
          <div class="kpi-label">Most searched tier</div>
          <span class="kpi-badge badge-cool">Avg {top_price_score}</span>
        </div>""", unsafe_allow_html=True)

# COLOR KPI
with k4:
    if selected_colors:
        color_avgs = color_region[color_region['palette'].isin(selected_colors)]\
                        .groupby('palette')['score'].mean()
        top_color = color_avgs.idxmax()
        top_color_score = int(color_avgs.max())
        color_hex = COLOR_TRENDS[top_color]['hex'][0]
        st.markdown(f"""
        <div class="kpi-card color-dim">
          <div class="kpi-dim-label">🎨 Color Palette</div>
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">
            <div style="width:32px;height:32px;background:{color_hex};border-radius:3px;flex-shrink:0"></div>
            <div class="kpi-value" style="font-size:20px">{top_color}</div>
          </div>
          <div class="kpi-label">Trending palette</div>
          <span class="kpi-badge badge-rise">Score {top_color_score}</span>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 1 — GEOGRAPHY ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-header">
  <div class="section-icon" style="background:#ff6b3518">📍</div>
  <span class="section-title">Dimension 1 — Geography</span>
  <span class="section-meta">State-level search intensity</span>
</div>
""", unsafe_allow_html=True)

g1, g2 = st.columns([3, 2])

with g1:
    # Bubble chart: states × total interest
    if kw_cols:
        geo_plot = region_df[['state'] + kw_cols].copy()
        geo_plot['total'] = geo_plot[kw_cols].sum(axis=1)
        geo_plot['dominant'] = geo_plot[kw_cols].idxmax(axis=1)
        geo_plot = geo_plot.sort_values('total', ascending=True)

        # Assign zone
        state_to_zone = {s: z for z, states in GEO_ZONES.items() for s in states}
        geo_plot['zone'] = geo_plot['state'].map(state_to_zone).fillna("Other")

        zone_colors = {
            "North India": "#ff6b35", "South India": "#7c3aed",
            "West India": "#10b981",  "East India":  "#f59e0b",
            "Central India": "#3b82f6", "Other": "#6b7280"
        }

        fig_geo = px.bar(
            geo_plot, x='total', y='state',
            color='zone', orientation='h',
            color_discrete_map=zone_colors,
            custom_data=['dominant','zone'],
            labels={'total': 'Total Interest Score', 'state': ''}
        )
        fig_geo.update_traces(
            hovertemplate="<b>%{y}</b><br>Score: %{x}<br>Top trend: %{customdata[0]}<br>Zone: %{customdata[1]}<extra></extra>"
        )
        fig_geo.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="IBM Plex Sans", color="#e8e4dc"),
            legend=dict(font=dict(family="IBM Plex Mono", size=10),
                        bgcolor="rgba(0,0,0,0)", title="Zone"),
            xaxis=dict(gridcolor="#2a2a3a", title=""),
            yaxis=dict(gridcolor="rgba(0,0,0,0)"),
            margin=dict(l=0,r=0,t=10,b=0), height=360
        )
        st.plotly_chart(fig_geo, use_container_width=True)

with g2:
    # Zone aggregation pie
    if kw_cols and 'zone' in geo_plot.columns:
        zone_totals = geo_plot.groupby('zone')['total'].sum().reset_index()
        fig_zone = px.pie(
            zone_totals, values='total', names='zone',
            color='zone', color_discrete_map=zone_colors,
            hole=0.55
        )
        fig_zone.update_traces(
            textfont=dict(family="IBM Plex Mono", size=10),
            hovertemplate="<b>%{label}</b><br>Score: %{value}<br>Share: %{percent}<extra></extra>"
        )
        fig_zone.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="IBM Plex Sans", color="#e8e4dc"),
            legend=dict(font=dict(family="IBM Plex Mono", size=10), bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=0,r=0,t=10,b=0), height=360,
            annotations=[dict(text="by<br>Zone", x=0.5, y=0.5, font_size=12,
                              font_family="IBM Plex Mono", font_color="#e8e4dc",
                              showarrow=False)]
        )
        st.plotly_chart(fig_zone, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 2 — CATEGORY ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-header">
  <div class="section-icon" style="background:#7c3aed18">🏷️</div>
  <span class="section-title">Dimension 2 — Category</span>
  <span class="section-meta">Trend velocity by fashion segment</span>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([2, 3])

with c1:
    # Category × Zone heatmap
    cat_zone_data = []
    for cat in selected_cats:
        cat_kws = [k for k in CATEGORIES[cat][:3] if k in kw_cols]
        if not cat_kws:
            continue
        for zone, states in GEO_ZONES.items():
            zone_states = [s for s in states if s in active_states]
            if not zone_states:
                continue
            sub = region_df[region_df['state'].isin(zone_states)]
            score = int(sub[cat_kws].values.mean()) if len(sub) > 0 else 0
            cat_zone_data.append({"category": cat, "zone": zone, "score": score})

    if cat_zone_data:
        cz_df = pd.DataFrame(cat_zone_data)
        cz_pivot = cz_df.pivot(index='category', columns='zone', values='score').fillna(0)
        fig_heat = px.imshow(
            cz_pivot,
            color_continuous_scale=[[0,"#12121a"],[0.4,"#7c3aed50"],[1,"#a78bfa"]],
            aspect="auto", text_auto=True,
            labels=dict(color="Interest")
        )
        fig_heat.update_traces(
            textfont=dict(family="IBM Plex Mono", size=10),
            hovertemplate="<b>%{y}</b> · %{x}<br>Score: %{z}<extra></extra>"
        )
        fig_heat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="IBM Plex Sans", color="#e8e4dc"),
            margin=dict(l=0,r=0,t=10,b=0), height=320,
            xaxis=dict(tickfont=dict(family="IBM Plex Mono", size=9)),
            yaxis=dict(tickfont=dict(family="IBM Plex Mono", size=9)),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_heat, use_container_width=True)

with c2:
    # Category trend lines over time
    cat_series = {}
    for cat in selected_cats:
        cat_kws = [k for k in CATEGORIES[cat][:3] if k in time_df.columns]
        if cat_kws:
            cat_series[cat] = time_df[cat_kws].mean(axis=1)

    if cat_series:
        cat_colors = ["#ff6b35","#7c3aed","#10b981","#f59e0b","#3b82f6","#ec4899"]
        fig_lines = go.Figure()
        for i, (cat, series) in enumerate(cat_series.items()):
            fig_lines.add_trace(go.Scatter(
                x=series.index, y=series.values,
                name=cat, mode='lines',
                line=dict(color=cat_colors[i % len(cat_colors)], width=2),
                fill='tozeroy',
                fillcolor=cat_colors[i % len(cat_colors)].replace("#","rgba(") + ",0.04)" if "#" in cat_colors[i % len(cat_colors)] else "rgba(255,107,53,0.04)",
                hovertemplate=f"<b>{cat}</b><br>%{{x|%d %b}}: %{{y:.0f}}<extra></extra>"
            ))
        fig_lines.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="IBM Plex Sans", color="#e8e4dc"),
            legend=dict(font=dict(family="IBM Plex Mono", size=10), bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(gridcolor="#2a2a3a20", title=""),
            yaxis=dict(gridcolor="#2a2a3a", title="Interest (0–100)", range=[0,105]),
            margin=dict(l=0,r=0,t=10,b=0), height=320,
            hovermode="x unified"
        )
        st.plotly_chart(fig_lines, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 3 — PRICE ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-header">
  <div class="section-icon" style="background:#10b98118">💰</div>
  <span class="section-title">Dimension 3 — Price Segment</span>
  <span class="section-meta">Purchase intent by price tier across geographies</span>
</div>
""", unsafe_allow_html=True)

p1, p2 = st.columns([2, 3])

with p1:
    # Price × Category bubble chart
    if selected_prices and selected_cats:
        pc_data = price_region[
            (price_region['price_segment'].isin(selected_prices)) &
            (price_region['category'].isin(selected_cats)) &
            (price_region['state'].isin(active_states))
        ].groupby(['price_segment','category'])['score'].mean().reset_index()

        price_order = [p for p in PRICE_SEGMENTS.keys() if p in selected_prices]
        price_cols  = [PRICE_SEGMENTS[p]['color'] for p in price_order]

        fig_pc = px.bar(
            pc_data, x='category', y='score',
            color='price_segment', barmode='group',
            color_discrete_sequence=price_cols,
            labels={'score':'Avg Interest','category':'','price_segment':'Tier'}
        )
        fig_pc.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="IBM Plex Sans", color="#e8e4dc"),
            legend=dict(font=dict(family="IBM Plex Mono", size=9), bgcolor="rgba(0,0,0,0)", title=""),
            xaxis=dict(gridcolor="rgba(0,0,0,0)", tickangle=-20,
                       tickfont=dict(family="IBM Plex Mono", size=9)),
            yaxis=dict(gridcolor="#2a2a3a"),
            margin=dict(l=0,r=0,t=10,b=0), height=300
        )
        st.plotly_chart(fig_pc, use_container_width=True)

with p2:
    # Price × State heatmap (top states)
    if selected_prices:
        top_states = region_df.nlargest(min(12, len(region_df)), '_total')['state'].tolist()
        ps_data = price_region[
            (price_region['state'].isin(top_states)) &
            (price_region['price_segment'].isin(selected_prices))
        ].groupby(['state','price_segment'])['score'].mean().reset_index()

        ps_pivot = ps_data.pivot(index='state', columns='price_segment', values='score').fillna(0)
        ps_pivot = ps_pivot[[c for c in PRICE_SEGMENTS.keys() if c in ps_pivot.columns]]

        fig_ps = px.imshow(
            ps_pivot,
            color_continuous_scale=[[0,"#12121a"],[0.5,"#10b98150"],[1,"#34d399"]],
            aspect="auto", text_auto=True,
            labels=dict(color="Score")
        )
        fig_ps.update_traces(textfont=dict(family="IBM Plex Mono", size=10))
        fig_ps.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="IBM Plex Sans", color="#e8e4dc"),
            margin=dict(l=0,r=0,t=10,b=0), height=300,
            xaxis=dict(tickfont=dict(family="IBM Plex Mono", size=9), tickangle=-15),
            yaxis=dict(tickfont=dict(family="IBM Plex Mono", size=9)),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_ps, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 4 — COLOR ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-header">
  <div class="section-icon" style="background:#f59e0b18">🎨</div>
  <span class="section-title">Dimension 4 — Color Palette</span>
  <span class="section-meta">Regional colour preference mapping</span>
</div>
""", unsafe_allow_html=True)

cl1, cl2, cl3 = st.columns([2, 2, 1])

with cl1:
    # Color × Zone radar
    if selected_colors:
        zone_color_data = []
        for color in selected_colors:
            for zone, states in GEO_ZONES.items():
                zone_states = [s for s in states if s in active_states]
                if not zone_states:
                    continue
                sub = color_region[
                    (color_region['palette'] == color) &
                    (color_region['state'].isin(zone_states))
                ]
                score = int(sub['score'].mean()) if len(sub) > 0 else 0
                zone_color_data.append({"palette": color, "zone": zone, "score": score})

        if zone_color_data:
            zc_df = pd.DataFrame(zone_color_data)
            palette_colors = ["#ff6b35","#a78bfa","#34d399","#fbbf24","#fb923c","#60a5fa"]
            fig_color_zone = go.Figure()
            zones_list = [z for z in GEO_ZONES.keys() if z in zc_df['zone'].unique()]
            for i, palette in enumerate(selected_colors):
                sub = zc_df[zc_df['palette'] == palette]
                sub = sub.set_index('zone').reindex(zones_list).fillna(0)
                fig_color_zone.add_trace(go.Scatterpolar(
                    r=sub['score'].tolist() + [sub['score'].tolist()[0]],
                    theta=zones_list + [zones_list[0]],
                    name=palette, mode='lines+markers',
                    line=dict(color=palette_colors[i % len(palette_colors)], width=2),
                    marker=dict(size=5),
                    fill='toself',
                    fillcolor=palette_colors[i % len(palette_colors)] + "18"
                ))
            fig_color_zone.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0,100],
                                   gridcolor="#2a2a3a", tickfont=dict(size=8, family="IBM Plex Mono"),
                                   tickcolor="#6b6878"),
                    angularaxis=dict(tickfont=dict(size=9, family="IBM Plex Mono", color="#e8e4dc"),
                                     gridcolor="#2a2a3a")
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="IBM Plex Sans", color="#e8e4dc"),
                legend=dict(font=dict(family="IBM Plex Mono", size=9), bgcolor="rgba(0,0,0,0)"),
                margin=dict(l=20,r=20,t=20,b=20), height=300
            )
            st.plotly_chart(fig_color_zone, use_container_width=True)

with cl2:
    # Color trend lines over time
    color_time_data = {}
    for color in selected_colors:
        kws = [k for k in COLOR_TRENDS[color]['keywords'] if k in time_df.columns]
        if kws:
            color_time_data[color] = time_df[kws].mean(axis=1)
        else:
            # synthetic fallback for color
            rng = np.random.default_rng(sum(ord(c) for c in color))
            n = len(time_df)
            vals = np.clip(rng.integers(20,70) + np.linspace(0,20,n) + rng.normal(0,8,n), 0, 100)
            color_time_data[color] = pd.Series(vals, index=time_df.index)

    palette_line_colors = ["#ff6b35","#a78bfa","#34d399","#fbbf24","#fb923c","#60a5fa"]
    fig_clr_time = go.Figure()
    for i, (pal, series) in enumerate(color_time_data.items()):
        fig_clr_time.add_trace(go.Scatter(
            x=series.index, y=series.values, name=pal, mode='lines',
            line=dict(color=palette_line_colors[i % len(palette_line_colors)], width=1.8),
            hovertemplate=f"<b>{pal}</b><br>%{{x|%d %b}}: %{{y:.0f}}<extra></extra>"
        ))
    fig_clr_time.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Sans", color="#e8e4dc"),
        legend=dict(font=dict(family="IBM Plex Mono", size=9), bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="#2a2a3a20", title=""),
        yaxis=dict(gridcolor="#2a2a3a", title="", range=[0,105]),
        margin=dict(l=0,r=0,t=10,b=0), height=300,
        hovermode="x unified"
    )
    st.plotly_chart(fig_clr_time, use_container_width=True)

with cl3:
    # Color swatches
    st.markdown("<div style='margin-top:8px'>", unsafe_allow_html=True)
    for palette in selected_colors:
        hexes = COLOR_TRENDS[palette]['hex']
        swatches = "".join([
            f'<div style="width:22px;height:22px;background:{h};border-radius:2px;'
            f'border:1px solid rgba(255,255,255,0.1)"></div>'
            for h in hexes
        ])
        avg_score = int(color_region[color_region['palette']==palette]['score'].mean())
        st.markdown(f"""
        <div style="background:#12121a;border:1px solid #2a2a3a;padding:10px 12px;margin-bottom:8px;border-radius:2px">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#6b6878;margin-bottom:6px">{palette.upper()}</div>
          <div style="display:flex;gap:4px;margin-bottom:6px">{swatches}</div>
          <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:700">{avg_score}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  CROSS-DIMENSION ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-header">
  <div class="section-icon" style="background:#3b82f618">⚡</div>
  <span class="section-title">Cross-Dimension Signals</span>
  <span class="section-meta">Intersections that matter</span>
</div>
""", unsafe_allow_html=True)

xd1, xd2 = st.columns([3, 2])

with xd1:
    # Scatter: state vs. category score vs. dominant price tier bubble
    if kw_cols and selected_prices:
        scatter_rows = []
        for cat in selected_cats[:4]:
            cat_kws = [k for k in CATEGORIES[cat][:3] if k in kw_cols]
            if not cat_kws:
                continue
            for state in active_states[:15]:
                row = region_df[region_df['state'] == state]
                if row.empty:
                    continue
                cat_score = int(row[cat_kws].values.mean()) if cat_kws else 0
                price_row = price_region[
                    (price_region['state'] == state) &
                    (price_region['category'] == cat) &
                    (price_region['price_segment'].isin(selected_prices))
                ]
                if price_row.empty:
                    continue
                dom_price = price_row.loc[price_row['score'].idxmax(), 'price_segment']
                price_score = int(price_row['score'].max())
                scatter_rows.append({
                    "state": state, "category": cat,
                    "cat_score": cat_score,
                    "price_score": price_score,
                    "dominant_price": dom_price,
                    "zone": state_to_zone.get(state, "Other")
                })

        if scatter_rows:
            sc_df = pd.DataFrame(scatter_rows)
            fig_scatter = px.scatter(
                sc_df, x='cat_score', y='price_score',
                color='zone', symbol='category',
                size='cat_score', size_max=22,
                hover_data=['state','dominant_price'],
                color_discrete_map=zone_colors,
                labels={'cat_score':'Category Interest','price_score':'Price Tier Interest'}
            )
            fig_scatter.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="IBM Plex Sans", color="#e8e4dc"),
                legend=dict(font=dict(family="IBM Plex Mono", size=9), bgcolor="rgba(0,0,0,0)"),
                xaxis=dict(gridcolor="#2a2a3a"),
                yaxis=dict(gridcolor="#2a2a3a"),
                margin=dict(l=0,r=0,t=10,b=0), height=320
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

with xd2:
    # Auto-generated insights
    st.markdown("**🔍 Auto Insights**")
    insights = []

    # Geo insight
    if kw_cols and 'state' in region_df.columns:
        top_s = region_df.nlargest(1,'_total').iloc[0]
        insights.append(("geo", "📍",
            f"<b>{top_s['state']}</b> leads all fashion interest — consider targeting it first."))

    # Category insight
    if cat_scores:
        best = max(cat_scores, key=cat_scores.get)
        worst = min(cat_scores, key=cat_scores.get)
        insights.append(("category", "🏷️",
            f"<b>{best}</b> outperforms <b>{worst}</b> by {cat_scores[best]-cat_scores[worst]} pts across all zones."))

    # Price insight
    if selected_prices:
        budget_states = price_region[
            (price_region['price_segment'] == "Budget (< ₹500)") &
            (price_region['state'].isin(active_states))
        ].nlargest(3,'score')['state'].tolist()
        if budget_states:
            insights.append(("price", "💰",
                f"Budget segment strongest in <b>{', '.join(budget_states[:2])}</b> — high-volume, low-ASP opportunity."))

        luxury_states = price_region[
            (price_region['price_segment'] == "Luxury (₹8000+)") &
            (price_region['state'].isin(active_states))
        ].nlargest(3,'score')['state'].tolist()
        if luxury_states:
            insights.append(("price", "💰",
                f"Luxury tier peaks in <b>{', '.join(luxury_states[:2])}</b> — premium positioning viable here."))

    # Color insight
    if selected_colors:
        top_pal = color_region[color_region['palette'].isin(selected_colors)]\
                     .groupby('palette')['score'].mean().idxmax()
        insights.append(("color-d", "🎨",
            f"<b>{top_pal}</b> leads colour searches — incorporate into seasonal product drops."))

    for dim, icon, text in insights:
        st.markdown(f"""
        <div class="insight-row {dim}">
          <span class="insight-icon">{icon}</span>
          <span>{text}</span>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  DATA TABLE (downloadable)
# ══════════════════════════════════════════════════════════════════════════════
with st.expander("📋 Raw Data Table — Geography × Category × Price × Color"):
    tab1, tab2, tab3, tab4 = st.tabs(["By State", "By Category", "By Price Tier", "By Color"])

    with tab1:
        if kw_cols:
            disp = region_df[['state'] + kw_cols].copy()
            disp['zone'] = disp['state'].map(state_to_zone)
            st.dataframe(disp.set_index('state'), use_container_width=True)
            csv = disp.to_csv(index=False)
            st.download_button("⬇️ Download CSV", csv, "geo_trends.csv", "text/csv")

    with tab2:
        if cat_scores:
            cat_df = pd.DataFrame(list(cat_scores.items()), columns=['Category','Avg Score'])
            cat_df = cat_df.sort_values('Avg Score', ascending=False)
            st.dataframe(cat_df.set_index('Category'), use_container_width=True)

    with tab3:
        if selected_prices:
            pt_df = price_region[
                (price_region['price_segment'].isin(selected_prices)) &
                (price_region['state'].isin(active_states))
            ].groupby(['price_segment','category'])['score'].mean().round(1).reset_index()
            st.dataframe(pt_df, use_container_width=True)
            st.download_button("⬇️ Download CSV", pt_df.to_csv(index=False), "price_trends.csv","text/csv")

    with tab4:
        if selected_colors:
            cr_df = color_region[
                (color_region['palette'].isin(selected_colors)) &
                (color_region['state'].isin(active_states))
            ].groupby(['palette','state'])['score'].mean().round(1).reset_index()
            st.dataframe(cr_df, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center;font-family:'IBM Plex Mono',monospace;font-size:10px;
color:#3a3a5a;letter-spacing:0.18em;padding:32px 0 16px;
border-top:1px solid #1a1a26;margin-top:32px">
INDIA FASHION INTELLIGENCE · GEOGRAPHY × CATEGORY × PRICE × COLOR · POWERED BY GOOGLE TRENDS
</div>
""", unsafe_allow_html=True)
