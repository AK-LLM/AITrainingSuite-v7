import streamlit as st
import pandas as pd

from app.core.data import DataProcessor
from app.core.registry import ModelRegistry
from app.core.evaluator import Evaluator
from app.experiments.tracker import ExperimentTracker
from app.persistence.io import save_model, load_model

st.set_page_config(page_title="AI Suite PRO", layout="wide")

mode = st.sidebar.radio("Mode", ["Cloud", "Local"])
page = st.sidebar.selectbox("Page", ["Home","Upload","Train","Evaluate","Predict","Experiments","Model IO"])

if "data" not in st.session_state:
    st.session_state.data = None
if "model" not in st.session_state:
    st.session_state.model = None

tracker = ExperimentTracker()

if page == "Home":
    st.title("AI Training Suite PRO")
    st.write("Full ML system with experiments, persistence, and hybrid execution.")

elif page == "Upload":
    file = st.file_uploader("Upload CSV")
    if file:
        df = pd.read_csv(file)
        st.session_state.data = df
        st.dataframe(df.head())

elif page == "Train":
    if st.session_state.data is None:
        st.warning("Upload data first")
    else:
        df = st.session_state.data
        target = st.selectbox("Target", df.columns)

        model_name = st.selectbox("Model", ModelRegistry.list_models(mode))

        if st.button("Train"):
            processor = DataProcessor(df, target)
            X_train, X_test, y_train, y_test = processor.process()

            model = ModelRegistry.create(model_name)
            model.train(X_train, y_train)

            st.session_state.model = model
            st.session_state.test = (X_test, y_test)

            metrics = Evaluator(model).evaluate(X_test, y_test)
            tracker.log_run(model_name, metrics)

            st.success("Training complete")
            st.write(metrics)

elif page == "Evaluate":
    if st.session_state.model:
        X_test, y_test = st.session_state.test
        results = Evaluator(st.session_state.model).evaluate(X_test, y_test)
        st.write(results)

elif page == "Predict":
    if st.session_state.model:
        inp = st.text_area("Input JSON")
        if st.button("Predict"):
            data = pd.DataFrame([eval(inp)])
            pred = st.session_state.model.predict(data)
            st.write(pred)

elif page == "Experiments":
    st.write(tracker.get_runs())

elif page == "Model IO":
    if st.button("Save Model"):
        save_model(st.session_state.model, "model.joblib")
        st.success("Saved")

    if st.button("Load Model"):
        st.session_state.model = load_model("model.joblib")
        st.success("Loaded")