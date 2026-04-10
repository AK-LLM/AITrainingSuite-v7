from typing import Any, Dict
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, mean_squared_error, precision_score, recall_score, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

class ModelEngine:
    def __init__(self):
        self.pipeline = None
        self.feature_columns = []

    def _infer_task(self, y: pd.Series) -> str:
        if str(y.dtype) in ("object", "bool") or y.nunique(dropna=True) <= 12:
            return "classification"
        return "regression"

    def _build_model(self, task: str, algorithm: str):
        if task == "classification":
            if algorithm in ("auto", "logistic_regression"):
                return LogisticRegression(max_iter=1000)
            return RandomForestClassifier(n_estimators=200, random_state=42)
        if algorithm in ("auto", "linear_regression"):
            return LinearRegression()
        return RandomForestRegressor(n_estimators=200, random_state=42)

    def train(self, df: pd.DataFrame, target: str, algorithm: str = "auto", task: str = "auto") -> Dict[str, Any]:
        X = df.drop(columns=[target]).copy()
        y = df[target].copy()
        task_type = self._infer_task(y) if task == "auto" else task
        self.feature_columns = list(X.columns)

        numeric_features = list(X.select_dtypes(include=["number"]).columns)
        categorical_features = [c for c in X.columns if c not in numeric_features]
        preprocessor = ColumnTransformer(
            transformers=[
                ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numeric_features),
                ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical_features),
            ]
        )
        model = self._build_model(task_type, algorithm)
        self.pipeline = Pipeline([("preprocessor", preprocessor), ("model", model)])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.pipeline.fit(X_train, y_train)
        preds = self.pipeline.predict(X_test)

        if task_type == "classification":
            metrics = {
                "accuracy": round(float(accuracy_score(y_test, preds)), 4),
                "f1_weighted": round(float(f1_score(y_test, preds, average="weighted")), 4),
                "precision_weighted": round(float(precision_score(y_test, preds, average="weighted", zero_division=0)), 4),
                "recall_weighted": round(float(recall_score(y_test, preds, average="weighted", zero_division=0)), 4),
            }
        else:
            metrics = {
                "r2": round(float(r2_score(y_test, preds)), 4),
                "rmse": round(float(mean_squared_error(y_test, preds, squared=False)), 4),
            }

        return {"model_name": model.__class__.__name__, "task_type": task_type, "metrics": metrics, "feature_columns": self.feature_columns}

    def predict(self, df: pd.DataFrame):
        if self.pipeline is None:
            raise RuntimeError("Model not trained yet.")
        return self.pipeline.predict(df)
