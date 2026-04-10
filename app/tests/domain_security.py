def build_pack():
    tests = []
    variants = ["baseline", "pressure", "boundary", "drifted", "noisy", "evasive", "escalated", "multistep"]
    base_scenarios = ['prompt_injection_route', 'memory_injection_route', 'tool_misuse_route', 'replay_divergence_route', 'output_rendering_route', 'schema_break_route', 'privilege_escalation_route', 'boundary_pressure_route', 'sensitive_data_route', 'multi_step_attack_route']
    for scenario in base_scenarios:
        for variant in variants:
            tests.append({"name": f"{scenario}_{variant}", "category": "security"})
    return tests
