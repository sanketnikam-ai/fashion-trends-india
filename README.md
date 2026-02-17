# 🔥 India Fashion — Top Trending Combinations
## Geography × Category × Price × Color

Scores every possible combination across 4 fashion dimensions and surfaces the top N trending signals across India's top 10 cities.

---

## 🚀 Deploy to Streamlit Community Cloud (Free)

```
1. Push these 3 files to a public GitHub repo
2. Go to share.streamlit.io
3. New app → select repo → app.py → Deploy
```

## 💻 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## ⚙️ How the Scoring Engine Works

Every `City × Sub-category × Price × Color` combination is scored on 4 signals:

| Signal       | Weight | Logic |
|---|---|---|
| 📍 Geo Reach    | 20%    | City market size × demand profile fit |
| 🏷️ Category Fit | 35%    | Sub-category affinity for the city |
| 💰 Price Demand | 25%    | Price bracket fit (luxury vs budget bias) |
| 🎨 Color Pull   | 20%    | City-specific colour preference weights |

A **velocity score** (MoM %) is computed separately to show acceleration.  
All scores are normalized 0–100 across the full combination space.

---

## 🎛️ Sidebar Controls

| Control | Effect |
|---|---|
| Time Period | 7 days → 12 months |
| Top N | Show top 3–10 combinations |
| Cities | Filter to specific cities |
| Category Groups | Filter which fashion segments to include |
| Price Buckets | ₹0–1K through ₹5K+ |
| Color | All 27 colors or filter by family |
| Min Velocity | Hide declining combinations |

---

## 📦 Files

```
fashion-top5/
├── app.py            ← Full Streamlit application
├── requirements.txt  ← Python dependencies
└── README.md         ← This file
```

---

## 🗒️ Notes

- Color hex strings are resolved at **data creation time** inside `score_combination()` and stored as a `color_hex` column — no late dictionary lookups at render time.
- Results are **cached for 30 minutes** (`@st.cache_data(ttl=1800)`).
- The export CSV includes the `Color Hex` column for direct use in design tools.
