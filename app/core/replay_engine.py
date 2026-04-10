class ReplayEngine:
    def build_replay_payload(self, event_type, payload):
        return {"event_type": event_type, "payload": payload, "status": "stored"}

    def compare_replays(self, first, second):
        f_payload = first.get("payload", {})
        s_payload = second.get("payload", {})
        f_metrics = f_payload.get("metrics", {}) if isinstance(f_payload, dict) else {}
        s_metrics = s_payload.get("metrics", {}) if isinstance(s_payload, dict) else {}
        metric_delta = {}
        numeric_delta_sum = 0.0
        numeric_delta_count = 0
        for key in sorted(set(f_metrics.keys()) | set(s_metrics.keys())):
            try:
                delta = round(float(s_metrics.get(key, 0)) - float(f_metrics.get(key, 0)), 6)
                metric_delta[key] = delta
                numeric_delta_sum += abs(delta)
                numeric_delta_count += 1
            except Exception:
                metric_delta[key] = "n/a"
        f_schema = f_payload.get("feature_columns", []) if isinstance(f_payload, dict) else []
        s_schema = s_payload.get("feature_columns", []) if isinstance(s_payload, dict) else []
        schema_missing = sorted(list(set(f_schema) - set(s_schema)))
        schema_unexpected = sorted(list(set(s_schema) - set(f_schema)))
        schema_delta_size = len(schema_missing) + len(schema_unexpected)
        avg_metric_delta = round(numeric_delta_sum / max(numeric_delta_count, 1), 6)
        severity_score = round(avg_metric_delta * 10 + schema_delta_size, 4)
        severity_band = "low" if severity_score < 1 else ("medium" if severity_score < 4 else "high")
        return {
            "same_event_type": first.get("event_type") == second.get("event_type"),
            "same_payload": f_payload == s_payload,
            "schema_missing": schema_missing,
            "schema_unexpected": schema_unexpected,
            "metric_delta": metric_delta,
            "avg_metric_delta": avg_metric_delta,
            "severity_score": severity_score,
            "severity_band": severity_band,
        }
