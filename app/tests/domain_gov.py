def build_pack():
    tests = []
    variants = ["baseline", "pressure", "boundary", "drifted", "noisy", "evasive", "escalated", "multistep"]
    base_scenarios = ['benefit_eligibility_shift', 'procurement_override', 'policy_trace_loss', 'public_record_suppression', 'identity_verification_gap', 'decision_reasoning_drift', 'tier_misclassification', 'audit_visibility_failure']
    for scenario in base_scenarios:
        for variant in variants:
            tests.append({"name": f"{scenario}_{variant}", "category": "government"})
    return tests
