# HackerOne Analytics Engineer Assignment

## 🎯 Project Overview
Interactive analytics dashboard for HackerOne vulnerability reports with data democratization and strategic insights.

## 📊 Deliverables
- **Source of Truth Tables**: 4 CSV files for data democratization
- **Interactive Dashboard**: Streamlit app with real-time filtering
- **Strategic Insights**: Business recommendations and trend analysis
- **Documentation**: Complete setup and usage guides

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Process data:**
   ```bash
   python process_data.py
   ```

3. **Run dashboard:**
   ```bash
   python -m streamlit run dashboards/streamlit_app.py
   ```

## 📁 Project Structure
```
hackerone_assignment/
├── data/
│   ├── raw/                    # Original dataset (10,094 reports)
│   └── processed/              # Source of truth tables
├── dashboards/                 # Streamlit application
├── notebooks/                  # Jupyter analysis notebooks
├── process_data.py            # Data processing pipeline
└── README.md                  # This file
```

## 📈 Key Insights
- **Information Disclosure** dominates vulnerability types (1,010 reports)
- **Top organizations** achieve 90%+ bounty rates
- **Elite reporters** maintain >96% validity rates
- **Platform maturity** shows stabilized growth patterns

## 📖 Documentation
- **DATA_SCHEMA.md** - Source tables structure
- **DATA_QUALITY_ANALYSIS.md** - Data quality assessment
- **Glossary** - Available in dashboard for metric definitions 