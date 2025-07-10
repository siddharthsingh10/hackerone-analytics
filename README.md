# 🕵️‍♂️ HackerOne Analytics: Explore, Discover, and Visualize!

Welcome! This project is all about making sense of real-world vulnerability reports from HackerOne. Whether you're a data nerd, a security enthusiast, or just curious about bug bounty trends, you'll find something cool here.

## What is this?
A hands-on, interactive dashboard and data toolkit for exploring thousands of real bug bounty reports. Dive into the data, spot trends, and get a feel for the hacker and organization landscape.

## What can you do here?
- 🗂️ **Explore the Data**: All the raw and processed data is open for you to poke around.
- 📊 **See the Dashboard**: Fire up the Streamlit app and get instant charts, filters, and insights.
- 💡 **Get Insights**: Find out which vulnerabilities are most common, who the top hackers are, and which orgs pay the most bounties.
- 🛠️ **Tinker or Extend**: Want to run your own analysis? The code is yours to play with.

## How to get started
1. **Install what you need:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Process the data:**
   ```bash
   python process_data.py
   ```
3. **Generate key insights (optional, for dashboard):**
   ```bash
   python generate_insights.py
   ```
4. **Launch the dashboard:**
   ```bash
   python -m streamlit run dashboards/streamlit_app.py
   ```

## Project Layout
```
hackerone_assignment/
├── data/
│   ├── raw/         # The original dataset (over 10,000 reports!)
│   └── processed/   # Cleaned, summarized tables for analysis
├── dashboards/      # The Streamlit dashboard app
├── notebooks/       # (Optional) Jupyter notebooks for exploration
├── process_data.py  # The main data wrangling script
├── generate_insights.py # Script for quick summary stats
└── README.md        # This file
```

## Fun Facts & Insights
- 🕵️‍♀️ **Info Disclosure** is the most-reported bug type.
- 🏆 Some orgs pay bounties on 90%+ of their reports!
- 🌟 Elite hackers have >96% valid report rates.
- 📈 The platform's grown a lot—see the trends for yourself.

## Want to know more?
- Check out `DATA_SCHEMA.md` for what each table means.
- Peek at `DATA_QUALITY_ANALYSIS.md` for how we cleaned things up.
- The dashboard has a built-in glossary if you get lost in the lingo.

---

Made with Python, pandas, and a dash of curiosity. Enjoy exploring! 🚀 