def build_pack():
    tests = []
    variants = ["baseline", "pressure", "boundary", "drifted", "noisy", "evasive", "escalated", "multistep"]
    base_scenarios = ['clinical_data_poisoning', 'medication_field_mismatch', 'allergy_record_conflict', 'triage_priority_shift', 'patient_identifier_confusion', 'lab_unit_swap', 'care_path_override', 'consent_visibility_gap', 'multiturn_clinical_pressure', 'critical_value_suppression', 'chart_merge_error', 'cross_patient_boundary']
    for scenario in base_scenarios:
        for variant in variants:
            tests.append({"name": f"{scenario}_{variant}", "category": "healthcare"})
    return tests
