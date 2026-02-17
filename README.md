# 🧵 India Fashion Intelligence
## Geography × Category × Price × Color Framework

A 4-dimensional fashion trend analysis dashboard for India, powered by Google Trends.

---

## The Framework

| Dimension | What it answers | Controls |
|---|---|---|
| 📍 **Geography** | *Where* is demand highest? | Zone (N/S/E/W) or individual state |
| 🏷️ **Category** | *What* is trending? | Ethnic / Western / Fusion / Streetwear / Occasion / Sustainable |
| 💰 **Price** | *How much* are they willing to spend? | Budget / Mid / Premium / Luxury |
| 🎨 **Color** | *What look* is winning? | Earth Tones / Pastels / Bolds / Monochromes / Jewel / Metallics |

Every visualisation in the app lets you **intersect** these four lenses — e.g. "Premium ethnic wear, jewel tones, in South India".

---

## 📊 What's Inside

### Dimension 1 — Geography
- Horizontal bar chart: states ranked by total fashion interest, coloured by zone
- Donut chart: interest share by geographic zone (North/South/East/West/Central)

### Dimension 2 — Category
- **Heatmap**: Category × Zone — which categories are hot in which regions
- **Trend lines**: How each category's interest has moved over your chosen time period

### Dimension 3 — Price Segment
- **Grouped bar**: Price tier × Category — where price sensitivity intersects category
- **Heatmap**: Price tier × Top states — which states prefer which price brackets

### Dimension 4 — Color Palette
- **Radar chart**: Color palette popularity across zones
- **Trend lines**: Color palette trajectories over time
- **Swatches panel**: Visual hex swatches + average scores per palette

### Cross-Dimension
- **Bubble scatter**: Category interest vs Price interest, coloured by zone, by state
- **Auto insights**: 5 plain-language signals auto-generated from the data

---

## 🚀 Deploy to Streamlit Community Cloud

```bash
# 1. Create a public GitHub repo with these files:
#    fashion-gcpc/
#    ├── app.py
#    ├── requirements.txt
#    └── README.md

# 2. Go to share.streamlit.io
# 3. New app → select repo → app.py → Deploy
```

## 💻 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## ⚙️ Configuration

### Sidebar Controls
- **Time Period** — 7 days to 12 months
- **Demo Data toggle** — uses synthetic data (no API calls; useful during dev)
- **Geography** — filter by Zone or individual State
- **Category** — pick which fashion segments to compare
- **Price Segments** — select which tiers to include
- **Color Palettes** — select which color stories to track

### Adding Your Own Keywords
Edit the dictionaries at the top of `app.py`:

```python
# Add a new category
CATEGORIES["Athleisure"] = ["yoga pants India", "sports bra", "running shoes women", "gym wear"]

# Add a new color trend
COLOR_TRENDS["Neo-Mint"] = {
    "keywords": ["mint green outfit", "neo mint fashion", "sage green kurta"],
    "hex": ["#98ff98", "#3eb489", "#c1f0c1"]
}

# Add a new price tier
PRICE_SEGMENTS["Ultra-Budget (< ₹200)"] = {
    "suffix": "under 200", "color": "#6ee7b7", "range": "₹0–200"
}
```

---

## ⚠️ Rate Limiting Note

`pytrends` is unofficial — Google may rate-limit heavy usage. Built-in mitigations:
- Results cached for 1 hour
- 1.2s sleep between API batches
- Auto-fallback to demo data if API fails
- "Use demo data" toggle for development

For production: use **GitHub Actions** to pre-fetch daily and store as CSV.

---

## 📁 Structure

```
fashion-gcpc/
├── app.py            ← Full Streamlit application
├── requirements.txt  ← Dependencies
└── README.md         ← This file
```
