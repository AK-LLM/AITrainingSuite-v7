import datetime

class ExperimentTracker:
    def __init__(self):
        if not hasattr(self.__class__, "runs"):
            self.__class__.runs = []

    def log_run(self, model, metrics):
        self.runs.append({
            "time": str(datetime.datetime.now()),
            "model": model,
            "metrics": metrics
        })

    def get_runs(self):
        return self.runs