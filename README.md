# 👗 India Fashion Trend Tracker

A Streamlit dashboard that pulls live Google Trends data to show which fashion trends are picking up across Indian states.

---

## 🖥️ Live Demo

Deploy free at [share.streamlit.io](https://share.streamlit.io) — no server needed.

---

## 📦 Features

- **Interactive India map** — choropleth heatmap by state (search interest 0–100)
- **Trend lines** — see how each keyword has grown over time
- **Keyword × State heatmap** — compare multiple trends across regions at once
- **Rising queries** — spot breakout search terms before they go mainstream
- **State leaderboard** — which states drive the most fashion search volume
- **5 keyword categories** — Traditional, Western, Emerging, Occasion, Accessories
- **Demo mode** — works with synthetic data if the API is rate-limited

---

## 🚀 Deploy to Streamlit Community Cloud (Free)

### Step 1 — Fork / push to GitHub
```
your-github/
└── fashion-trends-india/
    ├── app.py
    ├── requirements.txt
    └── README.md
```

### Step 2 — Connect to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repo → branch: `main` → file: `app.py`
5. Click **"Deploy"** → your app is live in ~60 seconds!

---

## 💻 Run Locally

```bash
# Clone your repo
git clone https://github.com/YOUR_USERNAME/fashion-trends-india
cd fashion-trends-india

# Install dependencies
pip install -r requirements.txt

# Run
streamlit run app.py
```

App opens at `http://localhost:8501`

---

## 🎛️ How to Use

| Control | What it does |
|---|---|
| **Keyword Category** | Switch between Traditional, Western, Emerging trends etc. |
| **Fashion Keywords** | Pick up to 5 keywords to compare |
| **Time Period** | 7 days → 12 months |
| **Use demo data** | Tick this if Google rate-limits your requests |
| **Keyword to map** | Choose which keyword renders on the India state map |
| **Rising Queries** | Explore breakout search terms for any selected keyword |

---

## ⚠️ Rate Limiting

`pytrends` is an **unofficial** Google Trends client. Google may rate-limit you if you make too many requests too fast. Tips:

- The app **caches results for 1 hour** — refreshing won't re-hit the API
- Use **"Use demo data"** checkbox during testing / development
- For production, consider pre-fetching daily via **GitHub Actions** and storing results as a CSV

---

## 📁 Project Structure

```
fashion-trends-india/
├── app.py             ← Main Streamlit application
├── requirements.txt   ← Python dependencies
└── README.md          ← This file
```

---

## 🛠️ Extend This

Ideas for what to add next:

- [ ] **GitHub Actions cron** — auto-fetch trends daily, cache as CSV
- [ ] **City-level data** — change `resolution='CITY'` in pytrends call
- [ ] **Brand tracking** — add Myntra, Meesho, Nykaa Fashion as keywords  
- [ ] **Email alerts** — notify when a keyword hits breakout status
- [ ] **Export to CSV** — add a download button for the data table
- [ ] **SerpApi backend** — swap pytrends for a paid, more reliable API

---

## 📄 License

MIT — free to use, modify, and deploy.
