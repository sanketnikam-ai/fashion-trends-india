import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pytrends.request import TrendReq
import json
import time
from datetime import datetime
import requests

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="India Fashion Trends",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono&display=swap');
    
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    
    .main { background-color: #faf8f5; }
    
    .metric-card {
        background: white;
        border: 1.5px solid #e8e0d0;
        border-radius: 4px;
        padding: 20px 24px;
        margin-bottom: 8px;
    }
    .metric-label {
        font-size: 11px;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #7a7060;
        font-family: 'DM Mono', monospace;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 600;
        color: #0e0e0e;
        line-height: 1;
    }
    .metric-delta-up   { color: #2a5c45; font-size: 13px; font-family: 'DM Mono', monospace; }
    .metric-delta-down { color: #c8441a; font-size: 13px; font-family: 'DM Mono', monospace; }

    .trend-pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 2px;
        font-family: 'DM Mono', monospace;
        font-size: 11px;
        font-weight: 500;
    }
    .pill-hot  { background: #fde8e0; color: #c8441a; }
    .pill-warm { background: #fff3cd; color: #856404; }
    .pill-cool { background: #d4edda; color: #2a5c45; }

    h1 { font-weight: 700 !important; letter-spacing: -0.02em !important; }
    h2, h3 { font-weight: 600 !important; }

    .stSelectbox label, .stMultiSelect label { 
        font-family: 'DM Mono', monospace !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #7a7060 !important;
    }

    div[data-testid="stSidebarContent"] { background: #f0ebe0; }
    
    .stAlert { border-radius: 4px !important; }
    
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── INDIA STATES GEOJSON ─────────────────────────────────────────────────────
@st.cache_data(ttl=86400)
def load_india_geojson():
    url = "https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson"
    try:
        r = requests.get(url, timeout=10)
        return r.json()
    except Exception:
        return None

# ─── STATE NAME MAPPING ───────────────────────────────────────────────────────
# Maps pytrends region names → GeoJSON feature names
STATE_MAP = {
    "Andhra Pradesh":        "Andhra Pradesh",
    "Arunachal Pradesh":     "Arunachal Pradesh",
    "Assam":                 "Assam",
    "Bihar":                 "Bihar",
    "Chhattisgarh":          "Chhattisgarh",
    "Delhi":                 "NCT of Delhi",
    "Goa":                   "Goa",
    "Gujarat":               "Gujarat",
    "Haryana":               "Haryana",
    "Himachal Pradesh":      "Himachal Pradesh",
    "Jammu and Kashmir":     "Jammu & Kashmir",
    "Jharkhand":             "Jharkhand",
    "Karnataka":             "Karnataka",
    "Kerala":                "Kerala",
    "Madhya Pradesh":        "Madhya Pradesh",
    "Maharashtra":           "Maharashtra",
    "Manipur":               "Manipur",
    "Meghalaya":             "Meghalaya",
    "Mizoram":               "Mizoram",
    "Nagaland":              "Nagaland",
    "Odisha":                "Odisha",
    "Punjab":                "Punjab",
    "Rajasthan":             "Rajasthan",
    "Sikkim":                "Sikkim",
    "Tamil Nadu":            "Tamil Nadu",
    "Telangana":             "Telangana",
    "Tripura":               "Tripura",
    "Uttar Pradesh":         "Uttar Pradesh",
    "Uttarakhand":           "Uttarakhand",
    "West Bengal":           "West Bengal",
}

# ─── KEYWORD CATEGORIES ───────────────────────────────────────────────────────
KEYWORD_CATEGORIES = {
    "Traditional Wear": ["saree", "kurta", "lehenga", "salwar kameez", "sherwani"],
    "Western Wear":     ["jeans", "crop top", "blazer", "co-ord set", "hoodie"],
    "Emerging Trends":  ["Y2K fashion", "streetwear", "cottagecore", "ethnic fusion", "modest fashion"],
    "Occasion Wear":    ["wedding outfit", "Diwali dress", "party wear", "ethnic wear", "casual wear"],
    "Accessories":      ["dupatta", "mojari", "kolhapuri", "potli bag", "statement earrings"],
}

TIMEFRAME_OPTIONS = {
    "Last 7 days":    "now 7-d",
    "Last 30 days":   "today 1-m",
    "Last 3 months":  "today 3-m",
    "Last 12 months": "today 12-m",
}

# ─── PYTRENDS FETCH ───────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_trends_by_region(keywords: list, timeframe: str) -> pd.DataFrame:
    """Fetch interest_by_region for India, broken down by state."""
    pytrends = TrendReq(hl='en-IN', tz=330, timeout=(10, 25),
                        retries=2, backoff_factor=0.5)
    all_dfs = []

    # pytrends allows max 5 keywords per request — batch if needed
    for i in range(0, len(keywords), 5):
        batch = keywords[i:i+5]
        try:
            pytrends.build_payload(kw_list=batch, timeframe=timeframe, geo='IN')
            df = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True)
            df = df[df.sum(axis=1) > 0]   # drop zero rows
            all_dfs.append(df)
            time.sleep(1)  # be polite to Google
        except Exception as e:
            st.warning(f"Could not fetch data for {batch}: {e}")

    if not all_dfs:
        return pd.DataFrame()

    result = pd.concat(all_dfs, axis=1)
    result.index.name = 'state'
    return result.reset_index()


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_trends_over_time(keywords: list, timeframe: str) -> pd.DataFrame:
    """Fetch interest over time for trend lines."""
    pytrends = TrendReq(hl='en-IN', tz=330, timeout=(10, 25),
                        retries=2, backoff_factor=0.5)
    all_dfs = []

    for i in range(0, len(keywords), 5):
        batch = keywords[i:i+5]
        try:
            pytrends.build_payload(kw_list=batch, timeframe=timeframe, geo='IN')
            df = pytrends.interest_over_time()
            if not df.empty:
                df = df.drop(columns=['isPartial'], errors='ignore')
                all_dfs.append(df)
            time.sleep(1)
        except Exception as e:
            st.warning(f"Time-series fetch failed for {batch}: {e}")

    if not all_dfs:
        return pd.DataFrame()

    return pd.concat(all_dfs, axis=1)


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_rising_queries(keyword: str, timeframe: str) -> pd.DataFrame:
    """Fetch 'rising' related queries for a single keyword."""
    pytrends = TrendReq(hl='en-IN', tz=330, timeout=(10, 25))
    try:
        pytrends.build_payload(kw_list=[keyword], timeframe=timeframe, geo='IN')
        related = pytrends.related_queries()
        rising = related.get(keyword, {}).get('rising', pd.DataFrame())
        return rising if isinstance(rising, pd.DataFrame) else pd.DataFrame()
    except Exception:
        return pd.DataFrame()


# ─── DEMO / FALLBACK DATA ─────────────────────────────────────────────────────
def get_demo_region_data(keywords: list) -> pd.DataFrame:
    """Fallback synthetic data when API is unavailable."""
    import numpy as np
    np.random.seed(42)
    states = list(STATE_MAP.keys())
    data = {"state": states}
    patterns = {
        "saree":          [90,45,85,70,55,40,30,75,50,65,60,80,95,92,70,78,55,40,35,42,88,62,82,38,93,86,48,72,58,76],
        "kurta":          [75,68,72,80,70,82,65,78,85,72,68,76,70,68,75,73,60,55,52,58,72,78,72,60,70,72,62,80,70,74],
        "lehenga":        [82,35,40,60,45,78,25,88,65,55,50,70,65,60,80,75,35,30,28,32,55,70,68,28,65,68,38,72,48,60],
        "streetwear":     [55,60,48,52,78,85,72,62,58,68,55,70,62,58,65,65,45,42,40,44,60,82,62,50,62,62,55,70,62,70],
        "Y2K fashion":    [48,52,42,45,72,82,68,55,50,62,48,65,55,50,58,60,38,35,32,38,52,78,55,42,55,55,48,65,55,65],
        "ethnic fusion":  [70,58,65,68,65,80,60,72,68,72,62,75,72,68,70,72,52,48,45,52,68,78,70,55,70,72,58,74,65,72],
        "co-ord set":     [60,62,55,58,75,85,70,65,60,68,58,72,65,62,68,68,48,45,42,48,62,82,62,52,62,62,55,70,60,70],
        "modest fashion": [45,50,40,48,55,60,52,50,45,55,45,58,52,48,55,55,38,35,30,38,50,62,50,40,50,50,45,58,48,55],
    }
    for kw in keywords:
        if kw in patterns:
            data[kw] = patterns[kw][:len(states)]
        else:
            data[kw] = list(np.random.randint(20, 95, len(states)))
    return pd.DataFrame(data)


def get_demo_time_data(keywords: list) -> pd.DataFrame:
    """Fallback synthetic time-series data."""
    import numpy as np
    dates = pd.date_range(end=datetime.today(), periods=90, freq='D')
    data = {'date': dates}
    np.random.seed(7)
    for kw in keywords:
        base = np.random.randint(30, 70)
        trend = np.linspace(0, np.random.randint(-20, 30), 90)
        noise = np.random.normal(0, 8, 90)
        data[kw] = np.clip(base + trend + noise, 0, 100).astype(int)
    df = pd.DataFrame(data).set_index('date')
    return df


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Controls")
    st.markdown("---")

    category = st.selectbox(
        "Keyword Category",
        options=list(KEYWORD_CATEGORIES.keys()),
        index=0
    )

    available_keywords = KEYWORD_CATEGORIES[category]
    selected_keywords = st.multiselect(
        "Fashion Keywords",
        options=available_keywords,
        default=available_keywords[:3],
        help="Select up to 5 keywords at once"
    )
    if len(selected_keywords) > 5:
        st.warning("⚠️ Max 5 keywords. Extra ones will be ignored.")
        selected_keywords = selected_keywords[:5]

    timeframe_label = st.selectbox(
        "Time Period",
        options=list(TIMEFRAME_OPTIONS.keys()),
        index=1
    )
    timeframe = TIMEFRAME_OPTIONS[timeframe_label]

    use_demo = st.checkbox(
        "Use demo data (no API calls)",
        value=False,
        help="Use synthetic data if pytrends is rate-limited or you're testing"
    )

    st.markdown("---")
    st.markdown("**Rising Queries Explorer**")
    rising_kw = st.selectbox(
        "Keyword to explore",
        options=selected_keywords if selected_keywords else available_keywords[:1]
    )

    st.markdown("---")
    st.caption("Data via Google Trends · pytrends · Updated hourly")
    st.caption(f"Last refresh: {datetime.now().strftime('%d %b %Y, %H:%M')}")


# ─── MAIN HEADER ──────────────────────────────────────────────────────────────
st.markdown("# 👗 India Fashion Trend Tracker")
st.markdown(
    f"<span style='font-family:DM Mono,monospace;font-size:12px;color:#7a7060;'>"
    f"CATEGORY: {category.upper()}  ·  PERIOD: {timeframe_label.upper()}  ·  "
    f"KEYWORDS: {len(selected_keywords)} SELECTED</span>",
    unsafe_allow_html=True
)
st.markdown("---")

if not selected_keywords:
    st.info("👈 Select at least one keyword in the sidebar to get started.")
    st.stop()


# ─── FETCH DATA ───────────────────────────────────────────────────────────────
with st.spinner("🔍 Fetching Google Trends data for India..."):
    if use_demo:
        region_df  = get_demo_region_data(selected_keywords)
        time_df    = get_demo_time_data(selected_keywords)
        st.info("📊 Showing demo data. Uncheck 'Use demo data' to fetch live trends.")
    else:
        try:
            region_df = fetch_trends_by_region(selected_keywords, timeframe)
            time_df   = fetch_trends_over_time(selected_keywords, timeframe)
            if region_df.empty:
                st.warning("⚠️ API returned no data (possible rate limit). Switching to demo data.")
                region_df = get_demo_region_data(selected_keywords)
                time_df   = get_demo_time_data(selected_keywords)
        except Exception as e:
            st.warning(f"⚠️ API error: {e}. Showing demo data instead.")
            region_df = get_demo_region_data(selected_keywords)
            time_df   = get_demo_time_data(selected_keywords)


# ─── KPI ROW ──────────────────────────────────────────────────────────────────
st.markdown("### 📌 Snapshot")
kpi_cols = st.columns(len(selected_keywords))

for i, kw in enumerate(selected_keywords):
    with kpi_cols[i]:
        if kw in region_df.columns:
            score = int(region_df[kw].max())
            top_state = region_df.loc[region_df[kw].idxmax(), 'state']
            avg = int(region_df[kw].mean())
            if score > 75:
                pill = '<span class="trend-pill pill-hot">🔥 Hot</span>'
            elif score > 45:
                pill = '<span class="trend-pill pill-warm">↗ Rising</span>'
            else:
                pill = '<span class="trend-pill pill-cool">Steady</span>'

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{kw}</div>
                <div class="metric-value">{score}</div>
                <div style="margin:6px 0 4px">{pill}</div>
                <div style="font-size:12px;color:#7a7060;">Peak: <b>{top_state}</b><br>Avg score: {avg}</div>
            </div>
            """, unsafe_allow_html=True)


st.markdown("---")

# ─── MAP + TIME CHART ─────────────────────────────────────────────────────────
col_map, col_time = st.columns([3, 2])

with col_map:
    st.markdown("### 🗺️ Interest by State")
    map_kw = st.selectbox("Keyword to map", selected_keywords, key="map_kw")

    if map_kw in region_df.columns:
        plot_df = region_df[['state', map_kw]].copy()
        plot_df.columns = ['state', 'score']
        plot_df['state_mapped'] = plot_df['state'].map(STATE_MAP).fillna(plot_df['state'])

        geojson = load_india_geojson()

        if geojson:
            fig_map = px.choropleth(
                plot_df,
                geojson=geojson,
                locations='state_mapped',
                featureidkey='properties.NAME_1',
                color='score',
                color_continuous_scale=["#f5f0e8", "#e8a825", "#c8441a"],
                range_color=(0, 100),
                hover_name='state',
                hover_data={'score': True, 'state_mapped': False},
                labels={'score': 'Interest (0–100)'},
                title=f'"{map_kw}" — Search Interest Across India'
            )
            fig_map.update_geos(
                fitbounds="locations", visible=False,
                bgcolor="#faf8f5"
            )
            fig_map.update_layout(
                margin=dict(l=0, r=0, t=40, b=0),
                paper_bgcolor="#faf8f5",
                font_family="DM Sans",
                coloraxis_colorbar=dict(
                    title="Interest",
                    tickfont=dict(family="DM Mono", size=10)
                )
            )
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            # Fallback: horizontal bar chart
            plot_df_sorted = plot_df.nlargest(15, 'score')
            fig_bar = px.bar(
                plot_df_sorted, x='score', y='state',
                orientation='h', color='score',
                color_continuous_scale=["#e8d8c0", "#c8441a"],
                labels={'score': 'Interest (0–100)', 'state': ''},
                title=f'"{map_kw}" — Top 15 States'
            )
            fig_bar.update_layout(
                paper_bgcolor="#faf8f5", plot_bgcolor="#faf8f5",
                font_family="DM Sans", showlegend=False,
                yaxis=dict(autorange="reversed")
            )
            st.plotly_chart(fig_bar, use_container_width=True)


with col_time:
    st.markdown("### 📈 Trend Over Time")
    if not time_df.empty:
        time_plot = time_df[
            [c for c in selected_keywords if c in time_df.columns]
        ].copy()
        time_plot.index = pd.to_datetime(time_plot.index)

        fig_time = go.Figure()
        colors = ["#0e0e0e", "#c8441a", "#2a5c45", "#e8a825", "#7a7060"]
        for i, kw in enumerate(time_plot.columns):
            fig_time.add_trace(go.Scatter(
                x=time_plot.index, y=time_plot[kw],
                name=kw, mode='lines',
                line=dict(color=colors[i % len(colors)], width=2),
                hovertemplate=f"<b>{kw}</b><br>Date: %{{x|%d %b}}<br>Score: %{{y}}<extra></extra>"
            ))

        fig_time.update_layout(
            paper_bgcolor="#faf8f5", plot_bgcolor="#faf8f5",
            font_family="DM Sans",
            legend=dict(font=dict(family="DM Mono", size=10)),
            xaxis=dict(gridcolor="#e8e0d0", title=""),
            yaxis=dict(gridcolor="#e8e0d0", title="Interest (0–100)", range=[0, 105]),
            margin=dict(l=0, r=0, t=10, b=0),
            hovermode="x unified"
        )
        st.plotly_chart(fig_time, use_container_width=True)
    else:
        st.info("Time-series data unavailable.")


# ─── HEATMAP: ALL KEYWORDS × TOP STATES ───────────────────────────────────────
st.markdown("---")
st.markdown("### 🔥 Keyword × State Heatmap")
st.caption("Deeper colour = stronger search interest in that state")

kw_cols = [c for c in selected_keywords if c in region_df.columns]
if kw_cols:
    heat_df = region_df.set_index('state')[kw_cols]
    heat_df['total'] = heat_df.sum(axis=1)
    heat_df = heat_df.nlargest(15, 'total').drop(columns='total')

    fig_heat = px.imshow(
        heat_df.T,
        color_continuous_scale=["#f5f0e8", "#e8a825", "#c8441a"],
        aspect="auto",
        labels=dict(x="State", y="Keyword", color="Interest"),
        title="Top 15 States × Selected Keywords"
    )
    fig_heat.update_layout(
        paper_bgcolor="#faf8f5", font_family="DM Sans",
        xaxis=dict(tickfont=dict(family="DM Mono", size=10)),
        yaxis=dict(tickfont=dict(family="DM Mono", size=10)),
        margin=dict(l=0, r=0, t=40, b=0),
        coloraxis_showscale=True
    )
    st.plotly_chart(fig_heat, use_container_width=True)


# ─── RISING QUERIES ───────────────────────────────────────────────────────────
st.markdown("---")
col_r1, col_r2 = st.columns([1, 1])

with col_r1:
    st.markdown(f"### 🚀 Rising Searches for *{rising_kw}*")
    st.caption("Queries with the biggest recent growth (breakout = >5000% increase)")

    if use_demo:
        rising_df = pd.DataFrame({
            'query': [
                f'{rising_kw} for women 2025', f'best {rising_kw} online',
                f'{rising_kw} under 500', f'{rising_kw} trend India',
                f'latest {rising_kw} design', f'{rising_kw} with jeans',
                f'{rising_kw} for wedding', f'designer {rising_kw}'
            ],
            'value': [5200, 3800, 2600, 1900, 1400, 950, 720, 480]
        })
    else:
        rising_df = fetch_rising_queries(rising_kw, timeframe)

    if not rising_df.empty:
        rising_df = rising_df.head(8)
        max_val = rising_df['value'].max()
        for _, row in rising_df.iterrows():
            label = "Breakout 🚀" if row['value'] >= 5000 else f"+{int(row['value'])}%"
            pct   = min(row['value'] / max(max_val, 1) * 100, 100)
            color = "#c8441a" if row['value'] >= 5000 else "#2a5c45"
            st.markdown(f"""
            <div style="margin-bottom:10px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                    <span style="font-size:13px;font-weight:500">{row['query']}</span>
                    <span style="font-family:'DM Mono',monospace;font-size:11px;color:{color}">{label}</span>
                </div>
                <div style="background:#e8e0d0;height:5px;border-radius:2px;">
                    <div style="width:{pct}%;background:{color};height:100%;border-radius:2px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No rising queries data available.")

with col_r2:
    st.markdown("### 🏆 State Leaderboard")
    st.caption("States ranked by total fashion search interest")

    kw_cols = [c for c in selected_keywords if c in region_df.columns]
    if kw_cols:
        leaderboard = region_df.copy()
        leaderboard['total_score'] = leaderboard[kw_cols].sum(axis=1)
        leaderboard['dominant']    = leaderboard[kw_cols].idxmax(axis=1)
        leaderboard = leaderboard.nlargest(10, 'total_score')[
            ['state', 'total_score', 'dominant']
        ].reset_index(drop=True)
        leaderboard.index += 1
        leaderboard.columns = ['State', 'Total Score', 'Top Trend']
        leaderboard['Total Score'] = leaderboard['Total Score'].astype(int)
        st.dataframe(
            leaderboard,
            use_container_width=True,
            hide_index=False
        )


# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;font-family:DM Mono,monospace;font-size:10px;"
    "color:#7a7060;letter-spacing:0.15em;padding:16px 0'>"
    "INDIA FASHION TREND TRACKER · POWERED BY GOOGLE TRENDS · BUILT WITH STREAMLIT"
    "</div>",
    unsafe_allow_html=True
)
