def build_pack():
    tests = []
    variants = ["baseline", "pressure", "boundary", "drifted", "noisy", "evasive", "escalated", "multistep"]
    base_scenarios = ['credit_score_shift', 'identity_signal_mismatch', 'aml_pattern_suppression', 'fraud_feature_drop', 'account_risk_masking', 'transaction_spike_obfuscation', 'suitability_override', 'predatory_offer_bias', 'customer_profile_drift', 'policy_exception_chain']
    for scenario in base_scenarios:
        for variant in variants:
            tests.append({"name": f"{scenario}_{variant}", "category": "finance"})
    return tests
