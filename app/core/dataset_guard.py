import hashlib
from typing import Any, Dict
import pandas as pd

class DatasetGuard:
    def profile(self, df: pd.DataFrame) -> Dict[str, Any]:
        schema = {col: str(dtype) for col, dtype in df.dtypes.items()}
        schema_text = "|".join(f"{k}:{v}" for k, v in schema.items())
        return {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "column_names": list(df.columns),
            "missing_values_total": int(df.isna().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum()),
            "schema": schema,
            "schema_fingerprint": hashlib.sha256(schema_text.encode("utf-8")).hexdigest(),
        }
