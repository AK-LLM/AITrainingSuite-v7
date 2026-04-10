# Troubleshooting

## App Does Not Start

Check dependency installation:

```bash
pip install -r requirements.txt
```

## Streamlit Cloud Build Fails

Verify the deployed repository is using the expected dependency versions and Python configuration.

If using Streamlit Cloud:

- confirm the correct repo and branch are connected
- prefer Python 3.12 unless your package set requires otherwise
- redeploy after dependency changes

## SQLite Errors

If SQLite cannot open the database, ensure these directories exist before startup:

```text
data/
exports/
app/docx/
```

## Training Fails

Check:

- dataset actually loaded
- parameters valid
- enough memory available
- model dependencies installed

## Prediction Fails

Check:

- trained artifact exists
- model path is valid
- input schema matches expected format

## DOCX Export Fails

Check that:

- `app/docx/` exists
- export destination is writable
- required template assets are present if the module expects them
