from app.core.model_engine import ModelEngine

class ModelComparisonHarness:
    def compare(self, df, target, first_algo: str, second_algo: str, task: str = "auto"):
        left = ModelEngine().train(df, target, algorithm=first_algo, task=task)
        right = ModelEngine().train(df, target, algorithm=second_algo, task=task)
        return {
            "left": {"algorithm": first_algo, "result": left},
            "right": {"algorithm": second_algo, "result": right},
        }
