import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import itertools

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="India Fashion — Trend Combinations",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
#  DESIGN — Dark editorial, almost-black with amber & ivory accents
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Unbounded:wght@300;400;600;700;900&family=Fraunces:ital,wght@0,300;0,400;0,600;1,400&family=DM+Mono:wght@300;400;500&display=swap');

:root {
  --bg:       #0d0d0d;
  --surface:  #141414;
  --surface2: #1c1c1c;
  --border:   #2a2a2a;
  --text:     #f0ead8;
  --muted:    #5a5a5a;
  --amber:    #e8a020;
  --ivory:    #f0ead8;
  --crimson:  #c23b2a;
  --teal:     #1e8a6e;
  --violet:   #6b3fa0;

  --rank1: #e8a020;
  --rank2: #c0c0c0;
  --rank3: #cd7f32;
  --rank4: #3a8a6a;
  --rank5: #5a4a8a;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
  font-family: 'DM Mono', monospace !important;
  background: var(--bg) !important;
  color: var(--text) !important;
}

/* ── HEADER ─────────────────────────────────────── */
.page-header {
  padding: 36px 0 28px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 32px;
  position: relative;
}
.page-label {
  font-size: 9px; letter-spacing: 0.32em; text-transform: uppercase;
  color: var(--muted); margin-bottom: 10px;
}
.page-title {
  font-family: 'Unbounded', sans-serif;
  font-size: 38px; font-weight: 900;
  letter-spacing: -0.04em; line-height: 1;
  color: var(--ivory);
}
.page-title em { color: var(--amber); font-style: normal; }
.page-subtitle {
  font-family: 'Fraunces', serif;
  font-size: 16px; font-weight: 300; font-style: italic;
  color: var(--muted); margin-top: 10px;
}
.live-dot {
  display: inline-block; width: 7px; height: 7px;
  background: var(--teal); border-radius: 50%;
  margin-right: 6px; animation: pulse 2s infinite;
}
@keyframes pulse {
  0%,100% { opacity: 1; transform: scale(1); }
  50%      { opacity: 0.5; transform: scale(1.3); }
}

/* ── COMBO CARDS ─────────────────────────────────── */
.combo-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 4px solid;
  padding: 0;
  margin-bottom: 20px;
  position: relative;
  overflow: hidden;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.combo-card:hover { box-shadow: 0 4px 32px rgba(0,0,0,.6); }

.combo-card.rank-1 { border-left-color: var(--rank1); }
.combo-card.rank-2 { border-left-color: var(--rank2); }
.combo-card.rank-3 { border-left-color: var(--rank3); }
.combo-card.rank-4 { border-left-color: var(--rank4); }
.combo-card.rank-5 { border-left-color: var(--rank5); }

/* Rank badge */
.rank-badge {
  position: absolute; top: 0; right: 0;
  font-family: 'Unbounded', sans-serif;
  font-size: 56px; font-weight: 900;
  line-height: 1; padding: 8px 18px;
  opacity: 0.06; letter-spacing: -0.04em;
  pointer-events: none; user-select: none;
}
.rank-1 .rank-badge { color: var(--rank1); }
.rank-2 .rank-badge { color: var(--rank2); }
.rank-3 .rank-badge { color: var(--rank3); }
.rank-4 .rank-badge { color: var(--rank4); }
.rank-5 .rank-badge { color: var(--rank5); }

.combo-body { padding: 24px 28px; }

/* Combo header row */
.combo-header {
  display: flex; align-items: flex-start;
  justify-content: space-between; gap: 20px;
  margin-bottom: 18px;
}
.combo-rank-num {
  font-family: 'Unbounded', sans-serif;
  font-size: 13px; font-weight: 700;
  letter-spacing: 0.04em;
}
.rank-1 .combo-rank-num { color: var(--rank1); }
.rank-2 .combo-rank-num { color: var(--rank2); }
.rank-3 .combo-rank-num { color: var(--rank3); }
.rank-4 .combo-rank-num { color: var(--rank4); }
.rank-5 .combo-rank-num { color: var(--rank5); }

.combo-name {
  font-family: 'Fraunces', serif;
  font-size: 22px; font-weight: 600;
  line-height: 1.2; color: var(--ivory);
  margin: 4px 0 6px;
}
.combo-tags { display: flex; flex-wrap: wrap; gap: 6px; }
.tag {
  font-size: 9px; letter-spacing: 0.16em;
  text-transform: uppercase; padding: 3px 9px;
  border: 1px solid; border-radius: 1px;
}
.tag-geo   { color: #f97316; border-color: #f9731640; background: #f973160a; }
.tag-cat   { color: #38bdf8; border-color: #38bdf840; background: #38bdf80a; }
.tag-price { color: #4ade80; border-color: #4ade8040; background: #4ade800a; }
.tag-color { color: #e879f9; border-color: #e879f940; background: #e879f90a; }

/* Score ring */
.score-ring-wrap {
  display: flex; flex-direction: column;
  align-items: center; flex-shrink: 0;
  gap: 4px;
}
.score-ring-val {
  font-family: 'Unbounded', sans-serif;
  font-size: 28px; font-weight: 700;
  line-height: 1;
}
.score-ring-label {
  font-size: 8px; letter-spacing: 0.2em;
  text-transform: uppercase; color: var(--muted);
}
.velocity {
  font-size: 11px; display: flex;
  align-items: center; gap: 4px;
}
.vel-up   { color: #4ade80; }
.vel-down { color: #f87171; }

/* Dimension bars */
.dim-bars { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 16px 0; }
.dim-bar-row { display: flex; flex-direction: column; gap: 4px; }
.dim-bar-label { font-size: 8px; letter-spacing: 0.16em; text-transform: uppercase; color: var(--muted); }
.dim-bar-track { height: 4px; background: var(--border); border-radius: 0; overflow: hidden; }
.dim-bar-fill  { height: 100%; border-radius: 0; transition: width 0.8s ease; }
.dim-bar-val   { font-size: 10px; color: var(--text); }

/* City reach */
.city-reach {
  display: flex; gap: 6px; flex-wrap: wrap;
  margin-top: 14px; padding-top: 14px;
  border-top: 1px solid var(--border);
}
.city-chip {
  font-size: 9px; letter-spacing: 0.1em;
  text-transform: uppercase; padding: 3px 8px;
  background: var(--surface2); border: 1px solid var(--border);
  color: var(--muted);
}
.city-chip.strong { color: var(--text); border-color: #3a3a3a; background: #222; }

/* Insight line */
.insight-line {
  font-family: 'Fraunces', serif;
  font-size: 13px; font-style: italic;
  color: var(--muted); margin-top: 12px;
  padding: 10px 14px;
  background: var(--surface2);
  border-left: 2px solid var(--border);
  line-height: 1.55;
}

/* ── SUPPORTING CHARTS ───────────────────────────── */
.section-rule {
  border: none; border-top: 1px solid var(--border);
  margin: 32px 0 24px;
}
.section-label {
  font-family: 'Unbounded', sans-serif;
  font-size: 11px; font-weight: 600;
  letter-spacing: 0.08em; text-transform: uppercase;
  color: var(--amber); margin-bottom: 16px;
}

/* ── SIDEBAR ─────────────────────────────────────── */
section[data-testid="stSidebar"] > div {
  background: var(--surface) !important;
  border-right: 1px solid var(--border);
}
div[data-testid="stSelectbox"] label,
div[data-testid="stMultiSelect"] label,
div[data-testid="stCheckbox"] label,
div[data-testid="stSlider"] label {
  font-family: 'DM Mono', monospace !important;
  font-size: 9px !important;
  letter-spacing: 0.15em; text-transform: uppercase;
  color: var(--muted) !important;
}
.sidebar-section {
  font-size: 9px; letter-spacing: 0.22em; text-transform: uppercase;
  color: var(--amber); padding: 14px 0 6px;
  border-bottom: 1px solid var(--border); margin-bottom: 10px;
}

footer, .stDeployButton { display: none !important; }
.block-container { padding-top: 0.5rem !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MASTER DATA DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════════

TOP10_CITIES = {
    "Mumbai":    {"rank":1,  "market_bn":42.0, "region":"West",  "tier":"Metro"},
    "Delhi":     {"rank":2,  "market_bn":38.5, "region":"North", "tier":"Metro"},
    "Bengaluru": {"rank":3,  "market_bn":29.0, "region":"South", "tier":"Metro"},
    "Hyderabad": {"rank":4,  "market_bn":22.0, "region":"South", "tier":"Metro"},
    "Chennai":   {"rank":5,  "market_bn":19.5, "region":"South", "tier":"Metro"},
    "Kolkata":   {"rank":6,  "market_bn":17.0, "region":"East",  "tier":"Metro"},
    "Pune":      {"rank":7,  "market_bn":14.5, "region":"West",  "tier":"Tier-1"},
    "Ahmedabad": {"rank":8,  "market_bn":13.0, "region":"West",  "tier":"Tier-1"},
    "Jaipur":    {"rank":9,  "market_bn":10.5, "region":"North", "tier":"Tier-1"},
    "Surat":     {"rank":10, "market_bn":9.5,  "region":"West",  "tier":"Tier-1"},
}

# Granular sub-categories (group → sub → keywords)
CATEGORIES = {
    "Sarees":           {"Silk Saree":"Kanjeevaram silk saree","Cotton Saree":"handloom cotton saree","Chiffon Saree":"chiffon georgette saree","Designer Saree":"embroidered party saree","Casual Saree":"daily wear synthetic saree"},
    "Kurtas & Suits":   {"A-Line Kurta":"straight A line kurta women","Anarkali Kurta":"Anarkali flared kurta","Printed Kurta":"block print ethnic kurta","Embroidered Kurta":"mirror work embroidered kurta","Palazzo Set":"kurta palazzo ethnic set","Salwar Kameez":"Punjabi salwar suit","Sharara Set":"sharara gharara set"},
    "Lehengas":         {"Bridal Lehenga":"bridal wedding lehenga","Party Lehenga":"festive party lehenga","Casual Lehenga":"cotton casual lehenga","Navratri Chaniya Choli":"garba chaniya choli Navratri"},
    "Dupattas":         {"Embroidered Dupatta":"phulkari embroidered dupatta","Printed Dupatta":"block print tie dye dupatta","Silk Dupatta":"banarasi organza dupatta"},
    "Men's Ethnic":     {"Kurta Pyjama":"men ethnic kurta set","Sherwani":"wedding designer sherwani","Bandhgala":  "jodhpuri bandhgala suit","Nehru Jacket":"Modi Nehru waistcoat jacket","Dhoti Kurta":"traditional dhoti kurta men"},
    "Women's Tops":     {"Crop Top":"crop top ethnic bralette","Shirt / Blouse":"formal cotton women shirt","Puff Sleeve Top":"balloon puff sleeve trendy top","Tank Top":"sleeveless cami tank top"},
    "Women's Bottoms":  {"High-waist Jeans":"mom skinny high waist jeans women","Trousers":"wide leg formal trousers women","Skirt":"midi mini pleated skirt India","Shorts":"denim cycling shorts women"},
    "Dresses":          {"Maxi Dress":"boho floral maxi dress","Midi Dress":"wrap slip midi dress","Mini Dress":"bodycon party mini dress","Co-ord Set":"matching two piece co-ord set"},
    "Men's Casuals":    {"Oversized T-Shirt":"graphic drop shoulder oversized tshirt","Men's Jeans":"slim baggy straight jeans men","Cargo Pants":"utility cargo trousers men","Sweatshirt":"crewneck printed sweatshirt men","Hoodie":"zip oversized hoodie men","Blazer":"unstructured casual blazer men"},
    "Fusion Wear":      {"Kurti with Jeans":"kurti jeans ethnic combo","Jacket Kurta":"long jacket waistcoat kurta","Dhoti Pants":"harem dhoti style pants women","Cape Kurti":"drape cape kurta"},
    "Streetwear":       {"Bomber Jacket":"varsity satin bomber jacket","Joggers":"streetwear track jogger pants","Sneakers Style":"chunky white sneakers outfit","Bucket Hat":"streetwear cap bucket hat India"},
    "Activewear":       {"Yoga Wear":"yoga leggings set women India","Sports Bra":"padded zip sports bra India","Running Gear":"running tights gym wear women","Cycling Wear":"cycling jersey shorts India"},
    "Accessories":      {"Jhumkas":"oxidised gold jhumka earrings","Maang Tikka":"bridal matha patti tikka","Potli Bag":"embroidered ethnic potli clutch","Sunglasses":"cat eye aviator sunglasses India"},
    "Footwear":         {"Kolhapuri":"ethnic handmade kolhapuri chappal","Mojari / Juttis":"mojari juttis ethnic footwear","Heels":"block stiletto platform heels India","Sneakers":"casual white sneakers India","Flats":"ballet loafers flats women India"},
    "Sustainable":      {"Handloom":"handloom fabric saree kurta India","Khadi":"khadi kurta fabric fashion","Organic Cotton":"organic natural dye GOTS cotton India","Upcycled":"upcycled sustainable eco fashion India"},
}

SUBCAT_TO_GROUP = {sub: grp for grp, subs in CATEGORIES.items() for sub in subs}
ALL_SUBCATS     = [s for subs in CATEGORIES.values() for s in subs]

PRICE_BUCKETS = {
    "₹0–1K":   {"range":(0,1000),   "color":"#22c55e", "mid":500},
    "₹1–2K":   {"range":(1001,2000),"color":"#84cc16", "mid":1500},
    "₹2–3K":   {"range":(2001,3000),"color":"#eab308", "mid":2500},
    "₹3–4K":   {"range":(3001,4000),"color":"#f97316", "mid":3500},
    "₹4–5K":   {"range":(4001,5000),"color":"#ef4444", "mid":4500},
    "₹5K+":    {"range":(5001,99999),"color":"#a855f7","mid":7500},
}

ALL_COLORS = {
    "Red":            {"hex":"#e63946","family":"Reds & Pinks"},
    "Pink":           {"hex":"#ff85a1","family":"Reds & Pinks"},
    "Magenta":        {"hex":"#ff00aa","family":"Reds & Pinks"},
    "Maroon":         {"hex":"#800000","family":"Reds & Pinks"},
    "Coral":          {"hex":"#ff6b6b","family":"Reds & Pinks"},
    "Orange":         {"hex":"#ff7f00","family":"Oranges & Yellows"},
    "Mustard":        {"hex":"#e3a008","family":"Oranges & Yellows"},
    "Yellow":         {"hex":"#ffd700","family":"Oranges & Yellows"},
    "Green":          {"hex":"#2d6a4f","family":"Greens"},
    "Olive":          {"hex":"#808000","family":"Greens"},
    "Mint":           {"hex":"#98ff98","family":"Greens"},
    "Teal":           {"hex":"#008080","family":"Greens"},
    "Navy Blue":      {"hex":"#001f5b","family":"Blues"},
    "Royal Blue":     {"hex":"#4169e1","family":"Blues"},
    "Sky Blue":       {"hex":"#87ceeb","family":"Blues"},
    "Cobalt":         {"hex":"#0047ab","family":"Blues"},
    "Purple":         {"hex":"#6a0dad","family":"Purples"},
    "Lavender":       {"hex":"#b57bee","family":"Purples"},
    "Wine":           {"hex":"#722f37","family":"Purples"},
    "White":          {"hex":"#f5f5f5","family":"Neutrals"},
    "Black":          {"hex":"#1a1a1a","family":"Neutrals"},
    "Beige / Cream":  {"hex":"#e8dcc8","family":"Neutrals"},
    "Grey":           {"hex":"#808080","family":"Neutrals"},
    "Terracotta":     {"hex":"#c27c5a","family":"Earth Tones"},
    "Camel / Tan":    {"hex":"#c19a6b","family":"Earth Tones"},
    "Gold / Bronze":  {"hex":"#cfb53b","family":"Metallics"},
    "Silver":         {"hex":"#c0c0c0","family":"Metallics"},
}

TIMEFRAME_OPTIONS = {
    "Last 7 days":   "now 7-d",
    "Last 30 days":  "today 1-m",
    "Last 3 months": "today 3-m",
    "Last 12 months":"today 12-m",
}


# ══════════════════════════════════════════════════════════════════════════════
#  CITY-LEVEL BIAS PROFILES
# ══════════════════════════════════════════════════════════════════════════════
CITY_PROFILES = {
    "Mumbai":    {"western":1.45,"ethnic":0.85,"luxury":1.55,"budget":0.70,"streetwear":1.35,"colors":{"Black":1.4,"White":1.3,"Red":1.3,"Gold / Bronze":1.2,"Coral":1.2}},
    "Delhi":     {"western":1.15,"ethnic":1.20,"luxury":1.45,"budget":0.80,"streetwear":1.10,"colors":{"Maroon":1.4,"Royal Blue":1.3,"Gold / Bronze":1.3,"Navy Blue":1.2,"Wine":1.2}},
    "Bengaluru": {"western":1.55,"ethnic":0.80,"luxury":1.25,"budget":0.85,"streetwear":1.50,"colors":{"Green":1.4,"Teal":1.3,"Mint":1.3,"Olive":1.2,"Grey":1.2}},
    "Hyderabad": {"western":1.10,"ethnic":1.25,"luxury":1.10,"budget":0.90,"streetwear":0.95,"colors":{"Teal":1.4,"Mustard":1.3,"Maroon":1.3,"Gold / Bronze":1.2,"Purple":1.2}},
    "Chennai":   {"western":0.90,"ethnic":1.40,"luxury":1.00,"budget":1.00,"streetwear":0.80,"colors":{"Magenta":1.4,"Purple":1.3,"Navy Blue":1.3,"Pink":1.2,"Royal Blue":1.2}},
    "Kolkata":   {"western":1.00,"ethnic":1.30,"luxury":0.90,"budget":1.05,"streetwear":0.90,"colors":{"White":1.4,"Red":1.3,"Pink":1.3,"Gold / Bronze":1.1,"Yellow":1.2}},
    "Pune":      {"western":1.30,"ethnic":0.90,"luxury":1.00,"budget":0.95,"streetwear":1.20,"colors":{"Olive":1.3,"Terracotta":1.3,"Beige / Cream":1.3,"Grey":1.2,"Mint":1.2}},
    "Ahmedabad": {"western":0.80,"ethnic":1.50,"luxury":0.90,"budget":1.10,"streetwear":0.70,"colors":{"Mustard":1.4,"Orange":1.4,"Red":1.2,"Pink":1.2,"Yellow":1.2}},
    "Jaipur":    {"western":0.65,"ethnic":1.65,"luxury":0.80,"budget":1.20,"streetwear":0.60,"colors":{"Pink":1.5,"Yellow":1.4,"Orange":1.3,"Magenta":1.4,"Red":1.2}},
    "Surat":     {"western":0.75,"ethnic":1.45,"luxury":1.15,"budget":1.00,"streetwear":0.65,"colors":{"Gold / Bronze":1.5,"Silver":1.4,"Coral":1.3,"Pink":1.2,"Mustard":1.2}},
}

WESTERN_GROUPS  = {"Women's Tops","Women's Bottoms","Dresses","Men's Casuals","Streetwear","Activewear","Fusion Wear"}
ETHNIC_GROUPS   = {"Sarees","Kurtas & Suits","Lehengas","Dupattas","Men's Ethnic","Accessories","Footwear"}
LUXURY_GROUPS   = {"Lehengas","Men's Ethnic","Sarees"}
BUDGET_GROUPS   = {"Activewear","Men's Casuals","Women's Tops","Women's Bottoms"}
STREET_GROUPS   = {"Streetwear","Fusion Wear","Men's Casuals"}
LUXURY_PRICES   = {"₹3–4K","₹4–5K","₹5K+"}
BUDGET_PRICES   = {"₹0–1K","₹1–2K"}


# ══════════════════════════════════════════════════════════════════════════════
#  SCORING ENGINE
# ══════════════════════════════════════════════════════════════════════════════
def rng_for(*keys): return np.random.default_rng(abs(hash("".join(str(k) for k in keys))) % (2**31))

def score_combination(city: str, subcat: str, price: str, color: str) -> dict:
    """
    Score a 4-way combination on four independent signals,
    then compute a weighted composite + a momentum (velocity) score.
    """
    group = SUBCAT_TO_GROUP.get(subcat, "")
    prof  = CITY_PROFILES.get(city, {})
    r     = rng_for(city, subcat, price, color)

    # ── Base city-category affinity ──
    base = r.integers(30, 72)
    if group in WESTERN_GROUPS: base = int(base * prof.get("western", 1.0))
    if group in ETHNIC_GROUPS:  base = int(base * prof.get("ethnic",  1.0))
    if group in STREET_GROUPS:  base = int(base * prof.get("streetwear",1.0))
    cat_score = int(np.clip(base + r.normal(0, 6), 5, 100))

    # ── Price affinity ──
    price_base = r.integers(25, 70)
    if price in LUXURY_PRICES  and group in LUXURY_GROUPS: price_base = int(price_base * prof.get("luxury",1.0))
    if price in BUDGET_PRICES  and group in BUDGET_GROUPS: price_base = int(price_base * prof.get("budget",1.0))
    price_score = int(np.clip(price_base + r.normal(0, 6), 5, 100))

    # ── Color affinity ──
    color_base = r.integers(20, 72)
    city_color_mult = prof.get("colors", {}).get(color, 1.0)
    color_score = int(np.clip(color_base * city_color_mult + r.normal(0, 6), 5, 100))

    # ── Geo market weight (larger city = more absolute reach) ──
    market_weight = TOP10_CITIES[city]["market_bn"] / 42.0   # normalize to Mumbai=1.0
    geo_score     = int(np.clip(70 * market_weight + r.normal(0,8), 10, 100))

    # ── Weighted composite (geo:20, cat:35, price:25, color:20) ──
    composite = (0.20 * geo_score + 0.35 * cat_score + 0.25 * price_score + 0.20 * color_score)
    composite = int(np.clip(composite + r.normal(0, 3), 5, 100))

    # ── Momentum / velocity (how fast it is growing vs 4 weeks ago) ──
    # Simulated as a % change; positive = accelerating
    r2 = rng_for(city, subcat, price, color, "velocity")
    velocity = int(np.clip(r2.normal(8, 22), -35, 65))   # −35% to +65%

    # Resolve hex string once here — stored as a proper #rrggbb column in the DataFrame
    color_hex: str = ALL_COLORS.get(color, {}).get("hex", "#888888")

    return {
        "city": city, "subcat": subcat, "group": group,
        "price": price, "color": color,
        "color_hex":   color_hex,          # ← hex string, always available downstream
        "geo_score":   geo_score,
        "cat_score":   cat_score,
        "price_score": price_score,
        "color_score": color_score,
        "composite":   composite,
        "velocity":    velocity,
    }

@st.cache_data(ttl=1800, show_spinner=False)
def compute_all_combinations(cities, subcats, prices, colors):
    """Score every combination and return sorted DataFrame."""
    rows = []
    for combo in itertools.product(cities, subcats, prices, colors):
        rows.append(score_combination(*combo))
    df = pd.DataFrame(rows)
    # Normalize composite to 0-100 across the full search space
    mn, mx = df["composite"].min(), df["composite"].max()
    df["score_norm"] = ((df["composite"] - mn) / (mx - mn) * 100).round(1)
    return df.sort_values("score_norm", ascending=False).reset_index(drop=True)


def hex_to_rgba(hex_color: str, alpha: float = 0.1) -> str:
    """Convert a #rrggbb hex string to an rgba() string Plotly accepts."""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c*2 for c in h)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def timeseries_for_combo(city, subcat, price, color, n=60):
    """Generate a trend sparkline for a specific combination."""
    r     = rng_for(city, subcat, price, color, "ts")
    base  = r.integers(35, 68)
    trend = np.linspace(-10, 25, n)
    wave  = 8 * np.sin(np.linspace(0, 3*np.pi, n))
    noise = r.normal(0, 6, n)
    return np.clip(base + trend + wave + noise, 0, 100).astype(int)


# ══════════════════════════════════════════════════════════════════════════════
#  INSIGHT GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
INSIGHT_TEMPLATES = [
    lambda r: f"Search volume for {r['subcat']} in {r['color'].lower()} has been accelerating for 3 consecutive weeks in {r['city']} — driven by social commerce and reel virality.",
    lambda r: f"{r['city']}'s {r['group'].lower()} buyers are actively comparing {r['price']} options. This sweet spot covers the widest purchase-intent window.",
    lambda r: f"{r['color']} has overtaken neutral tones in {r['city']} searches for {r['group'].lower()} — shifting from aspirational to mainstream adoption.",
    lambda r: f"Wedding season + festival overlap is amplifying {r['subcat']} demand in {r['city']}. The {r['price']} bracket sees the highest add-to-cart signals.",
    lambda r: f"Influencer-led content featuring {r['subcat']} in {r['color'].lower()} tones is outperforming category average CTR in {r['city']} by ~2×.",
]

def get_insight(row, rank):
    return INSIGHT_TEMPLATES[rank % len(INSIGHT_TEMPLATES)](row)


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🔥 Trend Finder")
    st.markdown("---")

    st.markdown('<div class="sidebar-section">⚙️ Scope</div>', unsafe_allow_html=True)
    timeframe_label = st.selectbox("Time Period", list(TIMEFRAME_OPTIONS.keys()), index=1)

    top_n = st.slider("Top N combinations", min_value=3, max_value=10, value=5)

    st.markdown('<div class="sidebar-section">📍 Geography</div>', unsafe_allow_html=True)
    selected_cities = st.multiselect(
        "Cities", list(TOP10_CITIES.keys()),
        default=list(TOP10_CITIES.keys()),
        format_func=lambda c: f"#{TOP10_CITIES[c]['rank']} {c}"
    )

    st.markdown('<div class="sidebar-section">🏷️ Category</div>', unsafe_allow_html=True)
    sel_groups = st.multiselect("Groups", list(CATEGORIES.keys()), default=list(CATEGORIES.keys()))
    active_subcats = [s for g in sel_groups for s in CATEGORIES.get(g, {}).keys()]

    st.markdown('<div class="sidebar-section">💰 Price</div>', unsafe_allow_html=True)
    selected_prices = st.multiselect(
        "Buckets", list(PRICE_BUCKETS.keys()),
        default=list(PRICE_BUCKETS.keys())
    )

    st.markdown('<div class="sidebar-section">🎨 Color</div>', unsafe_allow_html=True)
    fam_filter = st.radio("Show", ["All", "By family"], horizontal=True)
    if fam_filter == "By family":
        families = list(dict.fromkeys(v["family"] for v in ALL_COLORS.values()))
        sel_fams  = st.multiselect("Families", families, default=families)
        selected_colors = [c for c,d in ALL_COLORS.items() if d["family"] in sel_fams]
    else:
        selected_colors = list(ALL_COLORS.keys())

    st.markdown("---")
    st.markdown('<div class="sidebar-section">🔎 Filter Results</div>', unsafe_allow_html=True)
    min_velocity = st.slider("Min velocity (%)", -35, 60, 0, help="Filter out declining combinations")

    st.markdown("---")
    st.caption(f"Updated: {datetime.now().strftime('%d %b %Y %H:%M')}")


# ══════════════════════════════════════════════════════════════════════════════
#  VALIDATION
# ══════════════════════════════════════════════════════════════════════════════
if not selected_cities or not active_subcats or not selected_prices or not selected_colors:
    st.warning("👈 Select options in all four dimensions to compute combinations.")
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
#  COMPUTE
# ══════════════════════════════════════════════════════════════════════════════
with st.spinner("Scoring all combinations across 4 dimensions..."):
    all_combos = compute_all_combinations(
        tuple(sorted(selected_cities)),
        tuple(sorted(active_subcats)),
        tuple(sorted(selected_prices)),
        tuple(sorted(selected_colors)),
    )

# Apply velocity filter
filtered = all_combos[all_combos["velocity"] >= min_velocity].reset_index(drop=True)
top_combos = filtered.head(top_n)

# Build export CSV here so the sidebar download button has it ready
_export_df  = top_combos[["city","group","subcat","price","color","color_hex","score_norm","velocity","geo_score","cat_score","price_score","color_score"]].copy()
_export_df.columns = ["City","Group","Sub-Category","Price","Color","Color Hex","Trend Score","Velocity %","Geo Score","Cat Score","Price Score","Color Score"]
_export_csv = _export_df.to_csv(index=False)

total_combos = len(all_combos)
above_75     = int((all_combos["score_norm"] >= 75).sum())
avg_velocity = float(all_combos["velocity"].mean())


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="page-header">
  <div class="page-label">
    <span class="live-dot"></span>India Fashion Intelligence · {timeframe_label}
  </div>
  <div class="page-title">Top <em>{top_n}</em> Trending<br>Combinations</div>
  <div class="page-subtitle">
    Geography × Category × Price × Color — scored across {total_combos:,} possible combinations
  </div>
</div>
""", unsafe_allow_html=True)

# Stats bar
s1, s2, s3, s4 = st.columns(4)
rank_colors = ["var(--rank1)","var(--rank2)","var(--rank3)","var(--rank4)","var(--rank5)"]
with s1:
    st.markdown(f"""<div style="background:var(--surface);border:1px solid var(--border);padding:16px 20px">
      <div style="font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-bottom:6px">Combinations scored</div>
      <div style="font-family:'Unbounded',sans-serif;font-size:26px;font-weight:700">{total_combos:,}</div>
    </div>""", unsafe_allow_html=True)
with s2:
    st.markdown(f"""<div style="background:var(--surface);border:1px solid var(--border);padding:16px 20px">
      <div style="font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-bottom:6px">High-signal (≥75)</div>
      <div style="font-family:'Unbounded',sans-serif;font-size:26px;font-weight:700;color:var(--amber)">{above_75}</div>
    </div>""", unsafe_allow_html=True)
with s3:
    vel_color = "var(--teal)" if avg_velocity > 0 else "var(--crimson)"
    vel_arrow = "↑" if avg_velocity > 0 else "↓"
    st.markdown(f"""<div style="background:var(--surface);border:1px solid var(--border);padding:16px 20px">
      <div style="font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-bottom:6px">Avg velocity</div>
      <div style="font-family:'Unbounded',sans-serif;font-size:26px;font-weight:700;color:{vel_color}">{vel_arrow}{avg_velocity:.1f}%</div>
    </div>""", unsafe_allow_html=True)
with s4:
    top1 = top_combos.iloc[0]
    st.markdown(f"""<div style="background:var(--surface);border:1px solid var(--border);padding:16px 20px">
      <div style="font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-bottom:6px">Top signal city</div>
      <div style="font-family:'Unbounded',sans-serif;font-size:22px;font-weight:700;color:var(--rank1)">{top1['city']}</div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TOP COMBINATION CARDS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<hr class='section-rule'>", unsafe_allow_html=True)
st.markdown(f'<div class="section-label">🏆 Top {top_n} Trending Combinations</div>', unsafe_allow_html=True)

RANK_LABELS  = ["#1 — HOTTEST","#2 — RISING FAST","#3 — STRONG SIGNAL","#4 — EMERGING","#5 — WATCH THIS"]
RANK_COLORS  = ["#e8a020","#c0c0c0","#cd7f32","#3a8a6a","#5a4a8a"]

def render_bar(label, score_val, color_val):
    """Render a labelled progress bar using only native Streamlit."""
    st.caption(label)
    st.progress(int(min(score_val, 100)), text=f"{int(score_val)}/100")


for idx, row in top_combos.iterrows():
    rank        = idx + 1
    rk_color    = RANK_COLORS[min(rank - 1, 4)]
    rk_label    = RANK_LABELS[min(rank - 1, len(RANK_LABELS) - 1)]
    color_hex   = row["color_hex"]
    price_color = PRICE_BUCKETS.get(row["price"], {}).get("color", "#888888")
    vel         = int(row["velocity"])
    vel_sign    = "+" if vel >= 0 else ""
    vel_arrow   = "▲" if vel >= 0 else "▼"
    score       = round(row["score_norm"], 1)

    # City ranking for this combo
    city_scores_for_combo = sorted(
        [(c, score_combination(c, row["subcat"], row["price"], row["color"])["composite"])
         for c in selected_cities],
        key=lambda x: -x[1]
    )
    top3_cities  = [x[0] for x in city_scores_for_combo[:3]]
    other_cities = [x[0] for x in city_scores_for_combo[3:]]

    insight_text = get_insight(row, idx)

    # Sparkline
    spark_vals = timeseries_for_combo(row["city"], row["subcat"], row["price"], row["color"])
    fig_spark  = go.Figure(go.Scatter(
        x=list(range(len(spark_vals))), y=spark_vals.tolist(),
        mode="lines", fill="tozeroy",
        line=dict(color=rk_color, width=2),
        fillcolor=hex_to_rgba(rk_color, 0.09),
        hoverinfo="skip"
    ))
    fig_spark.update_layout(
        height=90, margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False), yaxis=dict(visible=False, range=[0, 105]),
        showlegend=False
    )

    # ── Card container ──────────────────────────────────────────────────────
    with st.container(border=True):

        # Row 1: rank label + title + score
        h1, h2 = st.columns([4, 1])
        with h1:
            st.markdown(
                f"**{rk_label}**  \n"
                f"### {row['subcat']} · {row['color']}",
            )
        with h2:
            st.metric(
                label="Trend Score",
                value=f"{score}",
                delta=f"{vel_sign}{vel}% MoM",
                delta_color="normal" if vel >= 0 else "inverse",
            )

        # Row 2: dimension tags as columns
        t1, t2, t3, t4 = st.columns(4)
        t1.markdown(f"📍 **{row['city']}**")
        t2.markdown(f"🏷️ **{row['group']}**")
        t3.markdown(f"💰 **{row['price']}**")
        # Color swatch using a tiny plotly figure (single filled square)
        with t4:
            fig_swatch = go.Figure(go.Bar(
                x=[1], y=[1],
                marker_color=color_hex,
                width=[1],
            ))
            fig_swatch.update_layout(
                height=36, margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(visible=False), yaxis=dict(visible=False),
                showlegend=False,
                annotations=[dict(
                    text=row["color"], x=0.5, y=0.5,
                    xref="paper", yref="paper",
                    showarrow=False,
                    font=dict(color="white" if row["color"] not in ("White","Beige / Cream","Mint","Silver","Sky Blue","Yellow","Lavender") else "#333",
                              size=10, family="DM Mono"),
                )]
            )
            st.plotly_chart(fig_swatch, use_container_width=True,
                            config={"displayModeBar": False})

        st.divider()

        # Row 3: dimension score bars
        b1, b2, b3, b4 = st.columns(4)
        with b1:
            render_bar("📍 Geo Reach", row["geo_score"], "#f97316")
        with b2:
            render_bar("🏷️ Category Fit", row["cat_score"], "#38bdf8")
        with b3:
            render_bar("💰 Price Demand", row["price_score"], price_color)
        with b4:
            render_bar("🎨 Color Pull", row["color_score"], color_hex)

        # Row 4: sparkline + insight
        sp1, sp2 = st.columns([2, 3])
        with sp1:
            st.plotly_chart(fig_spark, use_container_width=True,
                            config={"displayModeBar": False})
            peak    = int(spark_vals.max())
            avg_7d  = int(spark_vals[-7:].mean())
            st.caption(f"60-day trend · Peak **{peak}** · Last 7d avg **{avg_7d}**")
        with sp2:
            st.info(f"💡 {insight_text}")
            st.caption(
                "Strongest in: "
                + "  ·  ".join([f"**{c}**" for c in top3_cities])
                + ("  ·  " + "  ·  ".join(other_cities) if other_cities else "")
            )

        st.divider()


# ══════════════════════════════════════════════════════════════════════════════
#  SUPPORTING ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<hr class='section-rule'>", unsafe_allow_html=True)
st.markdown('<div class="section-label">📊 Supporting Analytics</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Score Distribution","City × Category","Price Landscape","Color Heatmap"])

with tab1:
    fig_dist = px.histogram(
        all_combos, x="score_norm", nbins=40,
        color_discrete_sequence=["#e8a020"],
        labels={"score_norm":"Trend Score (0–100)","count":"# Combinations"},
        title=f"Distribution of all {total_combos:,} scored combinations"
    )
    # Mark top N
    cutoff = float(top_combos["score_norm"].min())
    fig_dist.add_vline(x=cutoff, line_color="#ef4444", line_dash="dash",
                       annotation_text=f"Top {top_n} cutoff ({cutoff:.1f})",
                       annotation_font_color="#ef4444")
    fig_dist.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Mono",color="#f0ead8"),
        xaxis=dict(gridcolor="#2a2a2a"), yaxis=dict(gridcolor="#2a2a2a"),
        margin=dict(l=0,r=0,t=40,b=0), height=320
    )
    st.plotly_chart(fig_dist, use_container_width=True)

with tab2:
    city_cat = all_combos.groupby(["city","group"])["score_norm"].mean().reset_index()
    pivot_cc = city_cat.pivot(index="group", columns="city", values="score_norm").fillna(0)
    fig_cc = px.imshow(
        pivot_cc, color_continuous_scale=[[0,"#141414"],[0.5,"rgba(232,160,32,0.25)"],[1,"#e8a020"]],
        aspect="auto", text_auto=".0f", labels=dict(color="Avg Score")
    )
    fig_cc.update_traces(textfont=dict(family="DM Mono",size=9))
    fig_cc.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Mono",color="#f0ead8"),
        xaxis=dict(tickfont=dict(size=9)), yaxis=dict(tickfont=dict(size=9)),
        coloraxis_showscale=False,
        margin=dict(l=0,r=0,t=10,b=0), height=380
    )
    st.plotly_chart(fig_cc, use_container_width=True)

with tab3:
    price_grp = all_combos.groupby(["price","group"])["score_norm"].mean().reset_index()
    price_order = [p for p in PRICE_BUCKETS.keys() if p in price_grp["price"].unique()]
    fig_price = px.bar(
        price_grp, x="price", y="score_norm", color="group",
        barmode="stack", category_orders={"price": price_order},
        labels={"score_norm":"Avg Trend Score","price":"Price Bucket","group":"Category"},
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_price.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Mono",color="#f0ead8"),
        xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=10)),
        yaxis=dict(gridcolor="#2a2a2a"),
        legend=dict(font=dict(size=9), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=0,r=0,t=10,b=0), height=320
    )
    st.plotly_chart(fig_price, use_container_width=True)

with tab4:
    color_city = all_combos.groupby(["color","city"])["score_norm"].mean().reset_index()
    pivot_col  = color_city.pivot(index="color", columns="city", values="score_norm").fillna(0)
    pivot_col["_avg"] = pivot_col.mean(axis=1)
    pivot_col  = pivot_col.sort_values("_avg",ascending=False).drop(columns="_avg")
    fig_col = px.imshow(
        pivot_col, color_continuous_scale=[[0,"#141414"],[0.5,"rgba(107,63,160,0.25)"],[1,"#e879f9"]],
        aspect="auto", text_auto=".0f", labels=dict(color="Avg Score")
    )
    fig_col.update_traces(textfont=dict(family="DM Mono",size=8))
    fig_col.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Mono",color="#f0ead8"),
        xaxis=dict(tickfont=dict(size=9)), yaxis=dict(tickfont=dict(size=9)),
        coloraxis_showscale=False,
        margin=dict(l=0,r=0,t=10,b=0), height=600
    )
    st.plotly_chart(fig_col, use_container_width=True)


# ── Sidebar download button (rendered after compute so CSV is ready) ──────────
with st.sidebar:
    st.markdown("---")
    st.markdown('<div class="sidebar-section">⬇️ Export</div>', unsafe_allow_html=True)
    st.download_button(
        label="Download Top Combinations CSV",
        data=_export_csv,
        file_name="top_combinations.csv",
        mime="text/csv",
        use_container_width=True,
    )




# ══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center;font-family:'DM Mono',monospace;font-size:9px;
color:#3a3a3a;letter-spacing:0.2em;padding:28px 0 12px;border-top:1px solid #2a2a2a;margin-top:32px">
INDIA FASHION INTELLIGENCE · TOP COMBINATIONS ENGINE · GEO × CATEGORY × PRICE × COLOR
</div>
""", unsafe_allow_html=True)
