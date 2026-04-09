class TorchModel:
    def __init__(self):
        import torch
        import torch.nn as nn
        self.torch = torch
        self.model = nn.Sequential(nn.Linear(10,32), nn.ReLU(), nn.Linear(32,1))

    def train(self, X, y):
        torch = self.torch
        X = torch.tensor(X, dtype=torch.float32)
        y = torch.tensor(y.values, dtype=torch.float32).view(-1,1)

        opt = torch.optim.Adam(self.model.parameters())
        loss_fn = torch.nn.MSELoss()

        for _ in range(20):
            pred = self.model(X)
            loss = loss_fn(pred, y)
            opt.zero_grad()
            loss.backward()
            opt.step()

    def predict(self, X):
        torch = self.torch
        X = torch.tensor(X, dtype=torch.float32)
        return self.model(X).detach().numpy()