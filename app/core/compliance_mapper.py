class ComplianceMapper:
    def map_tests(self, test_names):
        return {
            "OWASP_LLM_2025": [t for t in test_names if "prompt" in t or "tool" in t or "memory" in t or "privilege" in t],
            "NIST_AI_RMF": [t for t in test_names if "dataset" in t or "drift" in t or "model" in t or "risk" in t],
            "ISO_42001": [t for t in test_names if "experiment" in t or "analytics" in t or "replay" in t or "traceability" in t],
            "PRIVACY": [t for t in test_names if "pii" in t or "sensitive" in t or "consent" in t],
            "DATA_QUALITY": [t for t in test_names if "missing" in t or "duplicate" in t or "quality" in t],
        }
