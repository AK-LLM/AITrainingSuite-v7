# Quickstart Guide

AITrainingSuite v7 can be launched locally or on Streamlit Cloud for rapid ML workflow execution.

## Prerequisites

- Python 3.12+
- pip
- 4GB RAM minimum
- Modern browser

## Install

```bash
git clone <repo-url>
cd AITrainingSuite-v7
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Launch

```bash
streamlit run streamlit_app.py
```

Open `http://localhost:8501`.

## First Successful Run

1. Open **Dataset**
2. Load a dataset into the catalog
3. Open **Train**
4. Run a baseline training job
5. Open **Predict**
6. Run a prediction
7. Open **Reports** or **DOCX**
8. Export the generated report

## Expected Outputs

- experiment created
- metrics saved
- model artifact saved
- report exported to `exports/`

## If Something Fails

See `docs/TROUBLESHOOTING.md`.
