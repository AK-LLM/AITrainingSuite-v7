from pathlib import Path
import pandas as pd
import streamlit as st

from app.core.dataset_guard import DatasetGuard
from app.core.experiment_db import ExperimentDB
from app.core.scoring import RiskScorer
from app.core.drift_detector import DriftDetector
from app.core.model_engine import ModelEngine
from app.core.model_compare import ModelComparisonHarness
from app.core.campaign_engine import CampaignEngine
from app.core.traceability import TraceabilityMapper
from app.core.compliance_mapper import ComplianceMapper
from app.core.replay_engine import ReplayEngine
from app.core.analytics import AnalyticsEngine
from app.core.reporting import ReportExporter
from app.core.docx_builder import DocxBuilder
from app.tests.catalog import build_full_catalog, run_catalog

st.set_page_config(page_title="AITrainingSuite v7 Hardened", layout="wide")

APP_ROOT = Path(__file__).resolve().parent
DATA_DIR = APP_ROOT / "data"
EXPORT_DIR = APP_ROOT / "exports"
DOCX_DIR = APP_ROOT / "app" / "docx"

DATA_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
DOCX_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "experiments.db"
db = ExperimentDB(str(DB_PATH))
guard = DatasetGuard()
scorer = RiskScorer()
drift = DriftDetector()
campaigns = CampaignEngine()
traceability = TraceabilityMapper()
compliance = ComplianceMapper()
replay = ReplayEngine()
analytics = AnalyticsEngine()
reporter = ReportExporter(str(EXPORT_DIR))
docx_builder = DocxBuilder(str(DOCX_DIR))
compare_harness = ModelComparisonHarness()

if "df" not in st.session_state:
    st.session_state.df = None
if "target" not in st.session_state:
    st.session_state.target = None
if "model_engine" not in st.session_state:
    st.session_state.model_engine = None
if "last_train_payload" not in st.session_state:
    st.session_state.last_train_payload = None
if "last_test_results" not in st.session_state:
    st.session_state.last_test_results = None
if "last_test_summary" not in st.session_state:
    st.session_state.last_test_summary = None
if "last_campaign_result" not in st.session_state:
    st.session_state.last_campaign_result = None

page = st.sidebar.radio(
    "Navigation",
    [
        "Home", "Dataset", "Train", "Predict", "Model Compare", "Tests", "Campaigns",
        "Experiments", "Compliance", "Traceability", "Replay", "Replay Compare",
        "Analytics", "Reports", "Docs", "DOCX", "About"
    ],
)

def _df():
    return st.session_state.df

if page == "Home":
    st.title("AITrainingSuite v7 Hardened")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Runs", db.count_runs())
    c2.metric("Datasets", db.count_datasets())
    c3.metric("Campaign Logs", db.count_campaigns())
    c4.metric("Catalog Size", len(build_full_catalog()))
    st.info("Final hardening pass with deeper domain packs, replay intelligence, model comparison, and weighted risk.")

elif page == "Dataset":
    st.title("Dataset Intake")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        st.session_state.df = df
        profile = guard.profile(df)
        db.log_dataset(profile)
        st.dataframe(df.head(), use_container_width=True)
        st.subheader("Dataset Profile")
        st.json(profile)
        st.subheader("Distribution Flags")
        st.json(drift.simple_distribution_flags(df))
    if _df() is not None:
        st.session_state.target = st.selectbox("Target column", _df().columns, index=max(0, len(_df().columns)-1))

elif page == "Train":
    st.title("Train Baseline Model")
    df = _df()
    target = st.session_state.target
    if df is None or target is None:
        st.warning("Upload a dataset and select a target first.")
    else:
        algorithm = st.selectbox("Algorithm", ["auto", "logistic_regression", "random_forest_classifier", "linear_regression", "random_forest_regressor"])
        task = st.selectbox("Task type", ["auto", "classification", "regression"])
        if st.button("Train model"):
            engine = ModelEngine()
            result = engine.train(df, target, algorithm=algorithm, task=task)
            st.session_state.model_engine = engine
            st.session_state.last_train_payload = result
            risk_summary = scorer.score_training(result)
            db.log_run(result["model_name"], result["task_type"], result["metrics"], risk_summary, {"algorithm": algorithm})
            db.log_replay("train_event", replay.build_replay_payload("train_event", result))
            st.success("Training complete.")
            st.json(result)
            st.json(risk_summary)

elif page == "Predict":
    st.title("Prediction")
    engine = st.session_state.model_engine
    df = _df()
    target = st.session_state.target
    if engine is None or df is None or target is None:
        st.warning("Train a model first.")
    else:
        row = df.drop(columns=[target]).head(1)
        st.dataframe(row, use_container_width=True)
        if st.button("Run prediction"):
            preds = engine.predict(row)
            st.write(preds.tolist() if hasattr(preds, "tolist") else preds)

elif page == "Model Compare":
    st.title("Model Compare")
    df = _df()
    target = st.session_state.target
    if df is None or target is None:
        st.warning("Upload a dataset and select a target first.")
    else:
        left = st.selectbox("Left algorithm", ["logistic_regression", "random_forest_classifier", "linear_regression", "random_forest_regressor"])
        right = st.selectbox("Right algorithm", ["random_forest_classifier", "logistic_regression", "random_forest_regressor", "linear_regression"])
        task = st.selectbox("Comparison task type", ["auto", "classification", "regression"])
        if st.button("Compare models"):
            result = compare_harness.compare(df, target, left, right, task=task)
            st.json(result)

elif page == "Tests":
    st.title("Catalog Runner")
    catalog = build_full_catalog()
    st.write(f"{len(catalog)} catalog entries available.")
    if st.button("Run catalog"):
        results = run_catalog(
            df_present=_df() is not None,
            target_present=st.session_state.target is not None,
            model_trained=st.session_state.model_engine is not None,
        )
        summary = scorer.score_test_results(results)
        weighted = scorer.weighted_risk(results)
        st.session_state.last_test_results = results
        st.session_state.last_test_summary = summary
        st.dataframe(pd.DataFrame(results).head(250), use_container_width=True)
        st.subheader("Summary")
        st.json(summary)
        st.subheader("Weighted Risk")
        st.json(weighted)

elif page == "Campaigns":
    st.title("Campaign Runner")
    campaign_name = st.selectbox("Campaign", campaigns.available_campaigns())
    if st.button("Run campaign"):
        result = campaigns.run_campaign(campaign_name)
        st.session_state.last_campaign_result = result
        db.log_campaign(campaign_name, result)
        db.log_replay("campaign_event", replay.build_replay_payload("campaign_event", result))
        st.json(result)

elif page == "Experiments":
    st.title("Experiment History")
    runs = db.list_runs()
    if runs:
        st.dataframe(pd.DataFrame(runs), use_container_width=True)
    else:
        st.info("No runs logged yet.")

elif page == "Compliance":
    st.title("Compliance Mapping")
    mapped = compliance.map_tests([x["name"] for x in build_full_catalog()])
    st.json(mapped)

elif page == "Traceability":
    st.title("Traceability")
    report = traceability.audit_report()
    rows = traceability.export_rows()
    st.json(report)
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

elif page == "Replay":
    st.title("Replay Log")
    rows = db.list_replays()
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
    else:
        st.info("No replay events logged yet.")

elif page == "Replay Compare":
    st.title("Replay Compare")
    rows = db.list_replays()
    if len(rows) >= 2:
        first = rows[0]["payload"]
        second = rows[1]["payload"]
        st.json(replay.compare_replays(first, second))
    else:
        st.info("Need at least two replay events.")

elif page == "Analytics":
    st.title("Analytics")
    st.json(analytics.summarize_runs(db.list_runs()))

elif page == "Reports":
    st.title("Reports")
    if st.button("Export traceability CSV"):
        path = reporter.export_csv("traceability.csv", traceability.export_rows())
        st.success(path)
    if st.button("Export session JSON"):
        payload = {
            "runs": db.list_runs()[:25],
            "campaigns": db.list_campaigns()[:25],
            "last_train": st.session_state.last_train_payload,
            "last_tests": st.session_state.last_test_summary,
            "last_campaign": st.session_state.last_campaign_result,
        }
        path = reporter.export_json("session_summary.json", payload)
        st.success(path)

elif page == "Docs":
    st.title("Documentation")
    doc_files = [
        "TEST_REFERENCE_GUIDE.md", "RUNBOOK.md", "COLAB_GUIDE.md", "MIGRATION_GUIDE.md",
        "ARCHITECTURE_GUIDE.md", "SECURITY_MANUAL.md", "COMPETITIVE_ANALYSIS.md",
        "EXPERIMENT_FRAMEWORK.md", "DEPLOYMENT_GUIDE.md",
    ]
    selected = st.selectbox("Document", doc_files)
    path = APP_ROOT / "app" / "docs" / selected
    st.code(path.read_text(encoding="utf-8"))

elif page == "DOCX":
    st.title("DOCX Builder")
    if st.button("Generate DOCX manuals"):
        manuals = [
            ("AITrainingSuite Test Reference Guide", "Catalog coverage, domain packs, campaigns, replay, compliance."),
            ("AITrainingSuite Runbook", "Setup, train, test, campaign, replay, export."),
            ("AITrainingSuite Architecture Guide", "Core module layout and data flow."),
            ("AITrainingSuite Security Manual", "Authorized robustness workflows and logging."),
        ]
        out = []
        for title, body in manuals:
            out.append(docx_builder.create_manual(title, [{"title": "Overview", "body": body}]))
        st.json(out)

elif page == "About":
    st.title("About")
    st.markdown(
        '''
This build strengthens the previously identified improvement areas:
- domain packs are deeper
- campaigns are more adaptive
- replay analysis is more intelligent
- model comparison is included
- weighted risk is included
- operator docs are included
        '''
    )
