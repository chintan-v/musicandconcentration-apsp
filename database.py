"""
database.py — Database initialisation and helper functions.

Uses SQLite via Python's standard library.  No ORM required.
The database path is relative to this file so the project is self-contained.
"""

import sqlite3
import csv
import os
from datetime import datetime

# ── Path ──────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "data", "research.db")


def get_connection():
    """Return a new SQLite connection with row_factory set."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create tables if they do not already exist."""
    conn = get_connection()
    with conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS participants (
                participant_id  TEXT PRIMARY KEY,
                consent_status  INTEGER NOT NULL DEFAULT 1,
                created_at      TEXT    NOT NULL
            );

            CREATE TABLE IF NOT EXISTS test_results (
                result_id         INTEGER PRIMARY KEY AUTOINCREMENT,
                participant_id    TEXT    NOT NULL REFERENCES participants(participant_id),
                test_condition    TEXT    NOT NULL CHECK(test_condition IN ('silence','music')),
                test_form         TEXT    NOT NULL CHECK(test_form IN ('A','B')),
                score             INTEGER NOT NULL,
                correct_answers   INTEGER NOT NULL,
                incorrect_answers INTEGER NOT NULL,
                completion_time   REAL    NOT NULL,
                completed_at      TEXT    NOT NULL
            );
        """)
    conn.close()


# ── Participant helpers ───────────────────────────────────────────────────────

def create_participant(participant_id: str) -> None:
    """Insert a new participant row."""
    conn = get_connection()
    with conn:
        conn.execute(
            "INSERT OR IGNORE INTO participants (participant_id, consent_status, created_at) "
            "VALUES (?, 1, ?)",
            (participant_id, datetime.utcnow().isoformat()),
        )
    conn.close()


def participant_exists(participant_id: str) -> bool:
    conn = get_connection()
    row = conn.execute(
        "SELECT 1 FROM participants WHERE participant_id = ?", (participant_id,)
    ).fetchone()
    conn.close()
    return row is not None


# ── Result helpers ────────────────────────────────────────────────────────────

def save_result(
    participant_id: str,
    test_condition: str,
    test_form: str,
    score: int,
    correct_answers: int,
    incorrect_answers: int,
    completion_time: float,
) -> None:
    """Insert a test result row."""
    conn = get_connection()
    with conn:
        conn.execute(
            """INSERT INTO test_results
               (participant_id, test_condition, test_form, score,
                correct_answers, incorrect_answers, completion_time, completed_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                participant_id,
                test_condition,
                test_form,
                score,
                correct_answers,
                incorrect_answers,
                completion_time,
                datetime.utcnow().isoformat(),
            ),
        )
    conn.close()


def get_results_for_participant(participant_id: str) -> list:
    """Return all test result rows for one participant."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM test_results WHERE participant_id = ? ORDER BY completed_at",
        (participant_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_results() -> list:
    """Return every test result row — for admin / export use."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM test_results ORDER BY completed_at"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── CSV export ────────────────────────────────────────────────────────────────

def export_to_csv(output_path: str = None) -> str:
    """
    Write all test_results rows to a CSV file.
    Returns the path of the written file.
    """
    if output_path is None:
        output_path = os.path.join(BASE_DIR, "data", "results_export.csv")

    rows = get_all_results()
    if not rows:
        return output_path

    fieldnames = list(rows[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return output_path
