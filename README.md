# HackerOne Analytics Engineer Assignment

## Project Structure

- `data/raw/` - Original dataset
- `data/processed/` - Source of truth tables (CSV)
- `notebooks/` - Jupyter notebooks for analysis
- `dashboards/` - Streamlit dashboard app
- `presentation/` - Slides and screenshots

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download the dataset:**
   - Download the HackerOne Disclosed Reports dataset from HuggingFace: [Hacker0x01/hackerone_disclosed_reports](https://huggingface.co/datasets/Hacker0x01/hackerone_disclosed_reports)
   - Place the raw data files in `data/raw/`

3. **Run Jupyter Notebooks:**
   ```bash
   jupyter lab
   # or
   jupyter notebook
   ```

4. **Run the Streamlit Dashboard:**
   ```bash
   streamlit run dashboards/streamlit_app.py
   ```

## Deliverables
- Jupyter notebooks (analysis workflow)
- Source of truth tables (CSV)
- Streamlit dashboard
- Presentation slides
- Comprehensive documentation

## Documentation

### Core Documentation
- **README.md** - Project overview and setup instructions
- **PROJECT_SUMMARY.md** - Complete project status and deliverables
- **DATA_SCHEMA.md** - Source of truth tables structure and schema
- **METRICS_DICTIONARY.md** - Detailed metric definitions and calculations
- **DATA_QUALITY_ANALYSIS.md** - Data quality assessment and null handling

### Technical Files
- **process_data.py** - Data processing pipeline
- **generate_insights.py** - Insights generation script
- **requirements.txt** - Python dependencies
- **dashboards/streamlit_app.py** - Interactive dashboard application 