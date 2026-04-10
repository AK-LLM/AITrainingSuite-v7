class CampaignEngine:
    def __init__(self):
        self._campaigns = {
            "dataset_poisoning_cascade": ["initialize", "inject_rows", "measure_schema_shift", "score_risk", "finalize"],
            "feature_drift_escalation": ["initialize", "drop_columns", "add_unknown_columns", "measure_schema_break", "finalize"],
            "model_failure_loop": ["initialize", "degrade_training_quality", "retrain", "measure_metric_drop", "finalize"],
            "memory_injection_chain": ["initialize", "seed_memory", "reapply_context", "measure_instability", "finalize"],
            "toolchain_mismatch": ["initialize", "alter_contract", "inject_bad_payload", "measure_handler_failure", "finalize"],
            "prediction_schema_break": ["initialize", "drop_inference_feature", "permute_columns", "measure_contract_break", "finalize"],
            "data_quality_degradation": ["initialize", "inflate_missingness", "inject_duplicates", "score_quality_drop", "finalize"],
            "class_imbalance_stress": ["initialize", "simulate_skew", "retrain", "measure_stability", "finalize"],
            "outlier_pressure": ["initialize", "inject_outliers", "retrain", "compare_shift", "finalize"],
            "replay_consistency_check": ["initialize", "store_reference", "rerun", "compare_outcomes", "finalize"],
            "multiturn_pressure_chain": ["initialize", "assert_policy", "apply_pressure", "measure_consistency", "finalize"],
            "prompt_injection_starter": ["initialize", "seed_override", "escalate_instruction", "measure_stability", "finalize"],
            "pii_exposure_probe": ["initialize", "scan_sensitive_columns", "request_sensitive_fields", "assess_blocking", "finalize"],
            "schema_confusion_chain": ["initialize", "rename_headers", "shuffle_headers", "assess_break", "finalize"],
            "training_regression_check": ["initialize", "baseline_train", "modified_train", "compare_metrics", "finalize"],
            "governance_override_probe": ["initialize", "weaken_constraints", "trigger_action", "assess_logging", "finalize"],
            "campaign_repro_check": ["initialize", "run_once", "run_again", "compare_summaries", "finalize"],
            "inference_stress_cycle": ["initialize", "run_batch_predictions", "count_errors", "flag_instability", "finalize"],
            "distribution_shift_chain": ["initialize", "shift_numeric_ranges", "retest", "measure_drift", "finalize"],
            "missingness_escalation": ["initialize", "inject_sparse_nulls", "inject_dense_nulls", "measure_failures", "finalize"],
            "duplicate_proliferation_chain": ["initialize", "seed_duplicates", "recompute_profile", "measure_quality_drop", "finalize"],
            "governance_logging_gap": ["initialize", "suppress_notes", "run_action", "assess_visibility", "finalize"],
            "prediction_contract_break": ["initialize", "drop_headers", "shuffle_columns", "measure_break", "finalize"],
            "replay_divergence_probe": ["initialize", "store_reference", "store_modified", "compare_replays", "finalize"],
        }

    def available_campaigns(self):
        return list(self._campaigns.keys())

    def run_campaign(self, name: str):
        phases = self._campaigns.get(name, [])
        results = []
        next_step = "complete"
        current_path = "normal"
        for phase in phases:
            status = "executed"
            if phase in ("measure_schema_break", "measure_metric_drop", "measure_failures", "measure_handler_failure"):
                status = "elevated"
                current_path = "escalated"
                next_step = "escalate_review"
            if current_path == "escalated" and phase == "finalize":
                status = "escalated_finalize"
            results.append({"phase": phase, "status": status, "path": current_path})
        return {"campaign": name, "phase_count": len(phases), "results": results, "next_step": next_step, "summary": "Adaptive-style campaign executed with branching state."}
