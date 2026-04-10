from typing import Dict, List
import pandas as pd

class DriftDetector:
    def compare_training_prediction_schema(self, training_columns: List[str], prediction_columns: List[str]) -> Dict[str, object]:
        training_set = set(training_columns)
        prediction_set = set(prediction_columns)
        return {
            "match": training_set == prediction_set,
            "missing_columns": sorted(list(training_set - prediction_set)),
            "unexpected_columns": sorted(list(prediction_set - training_set)),
        }

    def simple_distribution_flags(self, df: pd.DataFrame) -> Dict[str, object]:
        numeric = df.select_dtypes(include=["number"])
        flags = []
        for col in numeric.columns:
            series = numeric[col].dropna()
            if series.empty:
                continue
            if series.std() == 0:
                flags.append({"column": col, "flag": "zero_variance"})
            if abs(series.skew()) > 3:
                flags.append({"column": col, "flag": "extreme_skew"})
        return {"flag_count": len(flags), "flags": flags}
