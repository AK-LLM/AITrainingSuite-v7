def build_pack():
    tests = []
    variants = ["baseline", "pressure", "boundary", "drifted", "noisy", "evasive", "escalated", "multistep"]
    base_scenarios = ['citation_fabrication_risk', 'jurisdiction_shift', 'privilege_boundary_break', 'advice_strength_escalation', 'evidence_context_loss', 'case_fact_drift', 'document_conflict_handling', 'ethics_override_chain']
    for scenario in base_scenarios:
        for variant in variants:
            tests.append({"name": f"{scenario}_{variant}", "category": "legal"})
    return tests
