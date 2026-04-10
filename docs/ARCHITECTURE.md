# Architecture

AITrainingSuite v7 is a lightweight MLOps workbench built around a Streamlit interface, SQLite metadata storage, and file-based artifact persistence.

## High-Level Flow

```text
User → Streamlit UI → Workflow Module → Experiment Engine → SQLite / Artifacts
```

## Core Components

### Streamlit UI
Provides the navigation shell and workflow execution surfaces.

### Workflow Modules
Primary modules include:

- Dataset
- Train
- Predict
- Model Compare
- Experiments
- Compliance
- Replay
- Analytics
- Reports
- DOCX

### Metadata Layer
Experiment metadata is stored in:

```text
data/experiments.db
```

### Artifact Layer
Generated outputs are written to:

```text
exports/
```

## Experiment Lifecycle

```text
Dataset Loaded
→ Training Run
→ Metrics Generated
→ Artifact Saved
→ Experiment Recorded
→ Prediction Available
→ Report Exported
```

## Startup Requirements

The app expects these directories to exist:

- `data/`
- `exports/`
- `app/docx/`

These should be created during startup before SQLite initialization.
