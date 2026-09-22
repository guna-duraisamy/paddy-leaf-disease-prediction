"""Local SQLite prediction history; no image files or personal data are stored."""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def record_prediction(database: Path, disease: str, confidence: float, severity: str, visible_damage_percent: float) -> None:
    database.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database) as connection:
        connection.execute("""CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY, created_at TEXT NOT NULL, disease TEXT NOT NULL,
            confidence REAL NOT NULL, severity TEXT NOT NULL, visible_damage_percent REAL NOT NULL)""")
        connection.execute("INSERT INTO predictions (created_at, disease, confidence, severity, visible_damage_percent) VALUES (?, ?, ?, ?, ?)",
                           (datetime.now(timezone.utc).isoformat(), disease, confidence, severity, visible_damage_percent))
