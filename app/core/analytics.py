class AnalyticsEngine:
    def summarize_runs(self, runs):
        if not runs:
            return {"run_count": 0, "models": [], "task_types": [], "avg_metric_count": 0}
        metric_counts = [len(r["metrics"]) for r in runs]
        return {
            "run_count": len(runs),
            "models": sorted({r["model_name"] for r in runs}),
            "task_types": sorted({r["task_type"] for r in runs}),
            "avg_metric_count": round(sum(metric_counts) / len(metric_counts), 2),
        }
