"""
database.py — Database initialisation and helper functions.

Uses SQLite via Python's standard library.  No ORM required.
The database path is relative to this file so the project is self-contained.
Supports serverless / read-only deployment environments (e.g. Vercel, AWS Lambda).
"""

import sqlite3
import csv
import os
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _get_db_path() -> str:
    """
    Determine the database file path.
    If the deployment environment is serverless or the local directory is read-only,
    use a writable directory in /tmp.
    """
    is_serverless = any(
        os.environ.get(k) for k in [
            "VERCEL", "VERCEL_ENV", "VERCEL_REGION",
            "AWS_LAMBDA_FUNCTION_NAME", "LAMBDA_TASK_ROOT"
        ]
    )

    local_dir = os.path.join(BASE_DIR, "data")
    is_writable = False
    if not is_serverless:
        try:
            os.makedirs(local_dir, exist_ok=True)
            test_file = os.path.join(local_dir, ".test_write")
            with open(test_file, "w") as f:
                f.write("ok")
            os.remove(test_file)
            is_writable = True
        except (OSError, IOError, PermissionError):
            is_writable = False

    if is_writable:
        return os.path.join(local_dir, "research.db")
    else:
        tmp_dir = os.path.join("/tmp", "music_apsp_data")
        os.makedirs(tmp_dir, exist_ok=True)
        tmp_db = os.path.join(tmp_dir, "research.db")

        # Copy seed DB if available and destination does not exist
        if not os.path.exists(tmp_db):
            seed = os.path.join(BASE_DIR, "data", "research.db")
            if os.path.exists(seed):
                try:
                    shutil.copyfile(seed, tmp_db)
                    os.chmod(tmp_db, 0o666)
                except Exception:
                    pass

        return tmp_db


def _init_schema(conn: sqlite3.Connection) -> None:
    """Create tables if they do not already exist."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS participants (
            participant_id   TEXT PRIMARY KEY,
            participant_name TEXT,
            consent_status   INTEGER NOT NULL DEFAULT 1,
            created_at       TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS test_results (
            result_id         INTEGER PRIMARY KEY AUTOINCREMENT,
            participant_id    TEXT    NOT NULL REFERENCES participants(participant_id),
            participant_name  TEXT,
            test_condition    TEXT    NOT NULL CHECK(test_condition IN ('silence','music')),
            test_form         TEXT    NOT NULL CHECK(test_form IN ('A','B')),
            score             INTEGER NOT NULL,
            correct_answers   INTEGER NOT NULL,
            incorrect_answers INTEGER NOT NULL,
            completion_time   REAL    NOT NULL,
            completed_at      TEXT    NOT NULL
        );
    """)
    try:
        conn.execute("ALTER TABLE participants ADD COLUMN participant_name TEXT")
    except Exception:
        pass
    try:
        conn.execute("ALTER TABLE test_results ADD COLUMN participant_name TEXT")
    except Exception:
        pass


def get_connection() -> sqlite3.Connection:
    """Return a new SQLite connection with row_factory set and schema ensured."""
    db_path = _get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    _init_schema(conn)
    return conn


def init_db() -> None:
    """Explicit database initialization."""
    conn = get_connection()
    conn.close()


# ── Participant helpers ───────────────────────────────────────────────────────

def create_participant(participant_id: str, participant_name: str = "Anonymous") -> None:
    """Insert a new participant row with name."""
    conn = get_connection()
    with conn:
        conn.execute(
            "INSERT OR IGNORE INTO participants (participant_id, participant_name, consent_status, created_at) "
            "VALUES (?, ?, 1, ?)",
            (participant_id, participant_name, datetime.utcnow().isoformat()),
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

def send_to_google_sheet(payload: dict) -> bool:
    """Send a test result row to Google Sheets webhook if configured."""
    webhook_url = os.environ.get("GOOGLE_SHEET_WEBHOOK_URL")
    if not webhook_url:
        return False
    try:
        import requests
        response = requests.post(webhook_url, json=payload, timeout=8)
        return response.status_code in [200, 302]
    except Exception as e:
        print(f"Warning: Failed to sync with Google Sheet: {e}")
        return False


def save_result(
    participant_id: str,
    test_condition: str,
    test_form: str,
    score: int,
    correct_answers: int,
    incorrect_answers: int,
    completion_time: float,
    participant_name: str = "Anonymous",
) -> None:
    """Insert a test result row into SQLite and sync with Google Sheet."""
    completed_at = datetime.utcnow().isoformat()
    conn = get_connection()
    with conn:
        conn.execute(
            """INSERT INTO test_results
               (participant_id, participant_name, test_condition, test_form, score,
                correct_answers, incorrect_answers, completion_time, completed_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                participant_id,
                participant_name,
                test_condition,
                test_form,
                score,
                correct_answers,
                incorrect_answers,
                completion_time,
                completed_at,
            ),
        )
    conn.close()

    # Sync with Google Sheets
    send_to_google_sheet({
        "participant_id": participant_id,
        "participant_name": participant_name,
        "test_condition": test_condition,
        "test_form": test_form,
        "score": score,
        "correct_answers": correct_answers,
        "incorrect_answers": incorrect_answers,
        "completion_time": completion_time,
        "completed_at": completed_at,
    })


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
        db_path = _get_db_path()
        output_dir = os.path.dirname(db_path)
        output_path = os.path.join(output_dir, "results_export.csv")

    rows = get_all_results()
    if not rows:
        return output_path

    fieldnames = list(rows[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return output_path
