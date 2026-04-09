import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class DataProcessor:
    def __init__(self, df, target):
        self.df = df
        self.target = target

    def process(self):
        X = self.df.drop(columns=[self.target])
        y = self.df[self.target]

        X = pd.get_dummies(X)
        X = StandardScaler().fit_transform(X)

        return train_test_split(X, y, test_size=0.2)