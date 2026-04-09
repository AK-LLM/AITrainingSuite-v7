from app.models.sklearn_models import SklearnModel
from app.models.torch_models import TorchModel

class ModelRegistry:
    @staticmethod
    def list_models(mode):
        base = ["Linear","RandomForest","Logistic"]
        if mode == "Local":
            base.append("TorchNN")
        return base

    @staticmethod
    def create(name):
        if name == "TorchNN":
            return TorchModel()
        return SklearnModel(name)