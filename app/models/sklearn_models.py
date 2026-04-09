from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor

class SklearnModel:
    def __init__(self, name):
        if name == "Linear":
            self.model = LinearRegression()
        elif name == "RandomForest":
            self.model = RandomForestRegressor()
        elif name == "Logistic":
            self.model = LogisticRegression(max_iter=1000)

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)