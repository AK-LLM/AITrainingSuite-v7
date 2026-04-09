from sklearn.metrics import mean_squared_error, accuracy_score

class Evaluator:
    def __init__(self, model):
        self.model = model

    def evaluate(self, X, y):
        preds = self.model.predict(X)
        try:
            return {"MSE": mean_squared_error(y, preds)}
        except:
            return {"Accuracy": accuracy_score(y, preds)}