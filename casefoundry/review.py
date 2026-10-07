"""SQLite human-review queue; generated cases never auto-enter a golden set."""

import json
import sqlite3
from pathlib import Path

from .models import TestCase


SCHEMA = """
CREATE TABLE IF NOT EXISTS reviews (
  case_id TEXT PRIMARY KEY, payload TEXT NOT NULL, status TEXT NOT NULL,
  reason TEXT, edited_expected TEXT, updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


class ReviewQueue:
    def __init__(self, path: str | Path):
        self.path = str(path)
        with sqlite3.connect(self.path) as db:
            db.executescript(SCHEMA)

    def add(self, cases: list[TestCase]) -> int:
        with sqlite3.connect(self.path) as db:
            before = db.total_changes
            db.executemany("INSERT OR IGNORE INTO reviews(case_id,payload,status) VALUES (?,?,?)",
                           [(c.id, json.dumps(c.to_dict(), sort_keys=True), "pending") for c in cases])
            return db.total_changes - before

    def decide(self, case_id: str, status: str, reason: str = "",
               edited_expected: str | None = None) -> None:
        if status not in {"accepted", "edited", "rejected"}:
            raise ValueError("invalid review status")
        if status == "edited" and not edited_expected:
            raise ValueError("edited cases require edited_expected")
        with sqlite3.connect(self.path) as db:
            result = db.execute("UPDATE reviews SET status=?,reason=?,edited_expected=?,updated_at=CURRENT_TIMESTAMP WHERE case_id=?",
                                (status, reason, edited_expected, case_id))
            if result.rowcount != 1:
                raise KeyError(case_id)

    def counts(self) -> dict[str, int]:
        with sqlite3.connect(self.path) as db:
            rows = db.execute("SELECT status,COUNT(*) FROM reviews GROUP BY status")
            result = {status: count for status, count in rows}
        return {key: result.get(key, 0) for key in ("pending", "accepted", "edited", "rejected")}

