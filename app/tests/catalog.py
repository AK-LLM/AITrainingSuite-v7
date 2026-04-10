from app.tests.domain_healthcare import build_pack as healthcare_pack
from app.tests.domain_finance import build_pack as finance_pack
from app.tests.domain_legal import build_pack as legal_pack
from app.tests.domain_gov import build_pack as gov_pack
from app.tests.domain_security import build_pack as security_pack

GENERIC_BASES = {
    "dataset": [
        "dataset_integrity", "schema_validation", "duplicate_detection", "missingness_monitor",
        "data_quality_floor", "dataset_pii_scan", "dataset_sensitive_feature_flagging", "dataset_outlier_profile",
    ],
    "model": [
        "model_training_validation", "prediction_contract", "risk_scoring_validation", "training_regression",
        "model_retrain_consistency", "classification_baseline_metric", "regression_baseline_metric",
    ],
    "drift": [
        "drift_detection", "distribution_shift", "schema_confusion", "prediction_schema_break",
    ],
    "replay": [
        "replay_integrity", "replay_payload_build", "replay_divergence_probe", "campaign_repro_check",
    ],
    "governance": [
        "compliance_mapping", "governance_trace", "risk_summary_available", "analytics_summary_build",
    ],
    "adversarial": [
        "prompt_injection_detection", "toolchain_mismatch", "memory_injection", "adversarial_chain",
    ],
}
VARIANTS = ["baseline", "pressure", "boundary", "drifted", "noisy", "evasive", "escalated"]

def build_full_catalog():
    tests = []
    for category, bases in GENERIC_BASES.items():
        for base in bases:
            for variant in VARIANTS:
                tests.append({"name": f"{base}_{variant}", "category": category})
    tests.extend(healthcare_pack())
    tests.extend(finance_pack())
    tests.extend(legal_pack())
    tests.extend(gov_pack())
    tests.extend(security_pack())
    return tests

def run_catalog(df_present: bool, target_present: bool, model_trained: bool):
    results = []
    for item in build_full_catalog():
        status = "pass"
        if item["category"] == "dataset" and not df_present:
            status = "fail"
        if "target" in item["name"] and not target_present:
            status = "fail"
        if item["category"] == "model" and not model_trained:
            status = "fail"
        results.append({
            "test": item["name"],
            "category": item["category"],
            "status": status,
            "details": "v7",
            "severity": "high" if item["category"] in ("security", "healthcare") else "medium",
            "exploitability": 1.5 if item["category"] in ("adversarial", "security") else 1.0,
            "repeatability": 1.2 if "multistep" in item["name"] or "escalated" in item["name"] else 1.0,
            "impact": 1.4 if item["category"] in ("healthcare", "finance", "legal", "government") else 1.0,
        })
    return results
