import json
import sqlite3
from datetime import datetime
from typing import Any, Dict, List

class ExperimentDB:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    model_name TEXT NOT NULL,
                    task_type TEXT NOT NULL,
                    metrics_json TEXT NOT NULL,
                    risk_json TEXT NOT NULL,
                    notes_json TEXT NOT NULL
                )
            ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS datasets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    schema_fingerprint TEXT NOT NULL,
                    profile_json TEXT NOT NULL
                )
            ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS campaigns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    campaign_name TEXT NOT NULL,
                    result_json TEXT NOT NULL
                )
            ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS replays (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    replay_type TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                )
            ''')
            conn.commit()

    def _insert(self, table: str, fields: list, values: tuple) -> None:
        with self._connect() as conn:
            placeholders = ",".join(["?"] * len(fields))
            conn.execute(
                f"INSERT INTO {table} ({','.join(fields)}) VALUES ({placeholders})",
                values,
            )
            conn.commit()

    def log_dataset(self, profile: Dict[str, Any]) -> None:
        self._insert("datasets", ["created_at", "schema_fingerprint", "profile_json"],
                     (datetime.utcnow().isoformat(), profile["schema_fingerprint"], json.dumps(profile)))

    def log_run(self, model_name: str, task_type: str, metrics: Dict[str, Any], risk_summary: Dict[str, Any], notes: Dict[str, Any]) -> None:
        self._insert("runs", ["created_at", "model_name", "task_type", "metrics_json", "risk_json", "notes_json"],
                     (datetime.utcnow().isoformat(), model_name, task_type, json.dumps(metrics), json.dumps(risk_summary), json.dumps(notes)))

    def log_campaign(self, campaign_name: str, result: Dict[str, Any]) -> None:
        self._insert("campaigns", ["created_at", "campaign_name", "result_json"],
                     (datetime.utcnow().isoformat(), campaign_name, json.dumps(result)))

    def log_replay(self, replay_type: str, payload: Dict[str, Any]) -> None:
        self._insert("replays", ["created_at", "replay_type", "payload_json"],
                     (datetime.utcnow().isoformat(), replay_type, json.dumps(payload)))

    def _list(self, query: str):
        with self._connect() as conn:
            return conn.execute(query).fetchall()

    def list_runs(self) -> List[Dict[str, Any]]:
        rows = self._list("SELECT id, created_at, model_name, task_type, metrics_json, risk_json, notes_json FROM runs ORDER BY id DESC")
        return [{"id": r[0], "created_at": r[1], "model_name": r[2], "task_type": r[3], "metrics": json.loads(r[4]), "risk": json.loads(r[5]), "notes": json.loads(r[6])} for r in rows]

    def list_campaigns(self) -> List[Dict[str, Any]]:
        rows = self._list("SELECT id, created_at, campaign_name, result_json FROM campaigns ORDER BY id DESC")
        return [{"id": r[0], "created_at": r[1], "campaign_name": r[2], "result": json.loads(r[3])} for r in rows]

    def list_replays(self) -> List[Dict[str, Any]]:
        rows = self._list("SELECT id, created_at, replay_type, payload_json FROM replays ORDER BY id DESC")
        return [{"id": r[0], "created_at": r[1], "replay_type": r[2], "payload": json.loads(r[3])} for r in rows]

    def count_runs(self) -> int:
        return self._list("SELECT COUNT(*) FROM runs")[0][0]

    def count_datasets(self) -> int:
        return self._list("SELECT COUNT(*) FROM datasets")[0][0]

    def count_campaigns(self) -> int:
        return self._list("SELECT COUNT(*) FROM campaigns")[0][0]
