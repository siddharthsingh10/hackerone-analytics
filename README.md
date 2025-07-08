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
- README and submission package 