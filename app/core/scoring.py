from typing import Any, Dict, List

class RiskScorer:
    def score_training(self, training_result: Dict[str, Any]) -> Dict[str, Any]:
        metrics = training_result.get("metrics", {})
        task_type = training_result.get("task_type", "unknown")
        if task_type == "classification":
            acc = metrics.get("accuracy", 0)
            risk = "low" if acc >= 0.85 else ("medium" if acc >= 0.7 else "high")
        elif task_type == "regression":
            r2 = metrics.get("r2", 0)
            risk = "low" if r2 >= 0.75 else ("medium" if r2 >= 0.5 else "high")
        else:
            risk = "unknown"
        return {"task_type": task_type, "primary_metric": metrics, "risk_level": risk}

    def score_test_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        total = len(results)
        passed = sum(1 for r in results if r["status"] == "pass")
        failed = total - passed
        pass_rate = round((passed / total) * 100, 2) if total else 0.0
        by_category = {}
        for r in results:
            by_category.setdefault(r["category"], {"total": 0, "passed": 0})
            by_category[r["category"]]["total"] += 1
            by_category[r["category"]]["passed"] += 1 if r["status"] == "pass" else 0
        return {"total": total, "passed": passed, "failed": failed, "pass_rate_pct": pass_rate, "by_category": by_category}

    def weighted_risk(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        severity_map = {"low": 1, "medium": 2, "high": 3}
        total = 0
        for f in findings:
            sev = severity_map.get(f.get("severity", "medium"), 2)
            exploit = float(f.get("exploitability", 1))
            repeat = float(f.get("repeatability", 1))
            impact = float(f.get("impact", 1))
            total += sev * exploit * repeat * impact
        avg = round(total / max(len(findings), 1), 3)
        band = "low" if avg < 4 else ("medium" if avg < 8 else "high")
        return {"finding_count": len(findings), "weighted_score": avg, "risk_band": band}
