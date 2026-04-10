import json
import csv
from pathlib import Path

class ReportExporter:
    def __init__(self, export_dir: str):
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def export_json(self, filename: str, payload):
        path = self.export_dir / filename
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return str(path)

    def export_csv(self, filename: str, rows):
        path = self.export_dir / filename
        if not rows:
            path.write_text("", encoding="utf-8")
            return str(path)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        return str(path)
