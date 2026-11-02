"""
app.py — Flask application entry point for the APSP research website.

Run with:
    python app.py
Then open http://127.0.0.1:5000 in your browser.
"""

import os
import uuid
import json
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
    jsonify,
    send_file,
)

import database as db
from questions import FORM_A, FORM_B, ANSWER_KEY_A, ANSWER_KEY_B

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)
# Change this to a long random string in production
app.secret_key = "apsp-research-secret-key-2024"

# ── Initialise the database on startup ───────────────────────────────────────
db.init_db()


# ── Helpers ──────────────────────────────────────────────────────────────────

def _score_answers(submitted: dict, answer_key: dict) -> tuple[int, int, int]:
    """
    Compare submitted answers against the answer key.
    Returns (score, correct_count, incorrect_count).
    Score = 1 point per correct answer (no penalty).
    """
    correct = 0
    incorrect = 0
    for qid, correct_answer in answer_key.items():
        given = submitted.get(qid, "").strip()
        if given == correct_answer:
            correct += 1
        else:
            incorrect += 1
    return correct, correct, incorrect


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Home page — project description, instructions, consent, and start button."""
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    """
    Participant gives consent and is assigned a unique ID.
    Session stores participant_id so it persists across pages.
    """
    consent = request.form.get("consent")
    if consent != "yes":
        return redirect(url_for("index"))

    participant_name = request.form.get("participant_name", "").strip() or "Anonymous"
    participant_id = str(uuid.uuid4())[:8].upper()
    session["participant_id"] = participant_id
    session["participant_name"] = participant_name
    session["test1_done"] = False
    session["test2_done"] = False
    try:
        db.create_participant(participant_id, participant_name)
    except Exception as e:
        app.logger.warning(f"Could not record participant to db: {e}")

    return redirect(url_for("test1"))


@app.route("/test1")
def test1():
    """Test 1 — silence condition (Form A)."""
    if "participant_id" not in session:
        return redirect(url_for("index"))
    return render_template("test1.html", questions=FORM_A)


@app.route("/submit_test1", methods=["POST"])
def submit_test1():
    """Receive Test 1 answers, score them, and store the result."""
    if "participant_id" not in session:
        return redirect(url_for("index"))

    data = request.get_json(force=True)
    submitted  = data.get("answers", {})
    elapsed    = float(data.get("elapsed_seconds", 0))

    score, correct, incorrect = _score_answers(submitted, ANSWER_KEY_A)

    db.save_result(
        participant_id    = session["participant_id"],
        participant_name  = session.get("participant_name", "Anonymous"),
        test_condition    = "silence",
        test_form         = "A",
        score             = score,
        correct_answers   = correct,
        incorrect_answers = incorrect,
        completion_time   = elapsed,
    )

    session["test1_done"]  = True
    session["test1_score"] = score
    session["test1_time"]  = elapsed
    session["test1_correct"] = correct

    return jsonify({"status": "ok", "redirect": url_for("break_page")})


@app.route("/break")
def break_page():
    """Short rest between the two tests."""
    if "participant_id" not in session or not session.get("test1_done"):
        return redirect(url_for("index"))
    return render_template("break.html")


@app.route("/test2")
def test2():
    """Test 2 — music condition (Form B)."""
    if "participant_id" not in session or not session.get("test1_done"):
        return redirect(url_for("index"))
    return render_template("test2.html", questions=FORM_B)


@app.route("/submit_test2", methods=["POST"])
def submit_test2():
    """Receive Test 2 answers, score them, and store the result."""
    if "participant_id" not in session:
        return redirect(url_for("index"))

    data = request.get_json(force=True)
    submitted  = data.get("answers", {})
    elapsed    = float(data.get("elapsed_seconds", 0))

    score, correct, incorrect = _score_answers(submitted, ANSWER_KEY_B)

    db.save_result(
        participant_id    = session["participant_id"],
        participant_name  = session.get("participant_name", "Anonymous"),
        test_condition    = "music",
        test_form         = "B",
        score             = score,
        correct_answers   = correct,
        incorrect_answers = incorrect,
        completion_time   = elapsed,
    )

    session["test2_done"]  = True
    session["test2_score"] = score
    session["test2_time"]  = elapsed
    session["test2_correct"] = correct

    return jsonify({"status": "ok", "redirect": url_for("results")})


@app.route("/results")
def results():
    """Individual results page — shown after both tests are complete."""
    if "participant_id" not in session:
        return redirect(url_for("index"))
    if not session.get("test1_done") or not session.get("test2_done"):
        return redirect(url_for("index"))

    t1_score   = session.get("test1_score", 0)
    t2_score   = session.get("test2_score", 0)
    t1_time    = session.get("test1_time", 0)
    t2_time    = session.get("test2_time", 0)
    t1_correct = session.get("test1_correct", 0)
    t2_correct = session.get("test2_correct", 0)
    total_q    = 20

    t1_pct = round((t1_correct / total_q) * 100, 1)
    t2_pct = round((t2_correct / total_q) * 100, 1)

    def fmt_time(seconds):
        m = int(seconds) // 60
        s = int(seconds) % 60
        return f"{m}m {s:02d}s"

    return render_template(
        "results.html",
        participant_id   = session["participant_id"],
        participant_name = session.get("participant_name", "Anonymous"),
        t1_score   = t1_score,
        t2_score   = t2_score,
        t1_pct     = t1_pct,
        t2_pct     = t2_pct,
        t1_time    = fmt_time(t1_time),
        t2_time    = fmt_time(t2_time),
        total_q    = total_q,
    )


# ── Admin / Data export ───────────────────────────────────────────────────────

@app.route("/admin/export")
def admin_export():
    """
    Export all results to CSV and return a confirmation message.
    Access: http://127.0.0.1:5000/admin/export
    The CSV is saved to data/results_export.csv
    """
    path = db.export_to_csv()
    return jsonify({
        "status": "exported",
        "file": path,
        "rows": len(db.get_all_results()),
    })


@app.route("/admin/data")
def admin_data():
    """Return all results as JSON for quick inspection."""
    rows = db.get_all_results()
    return jsonify(rows)


@app.route("/admin/download")
def admin_download():
    """Download results CSV file directly."""
    path = db.export_to_csv()
    return send_file(path, as_attachment=True, download_name="results_export.csv", mimetype="text/csv")


@app.route("/admin/test-sheet")
def test_sheet():
    """Test sending a test row to Google Sheet webhook."""
    webhook_url = os.environ.get("GOOGLE_SHEET_WEBHOOK_URL")
    if not webhook_url:
        return jsonify({
            "status": "not_configured",
            "message": "GOOGLE_SHEET_WEBHOOK_URL is not set yet in Vercel environment variables."
        }), 400

    payload = {
        "participant_id": "TEST_DEMO",
        "participant_name": "Demo Student",
        "test_condition": "silence",
        "test_form": "A",
        "score": 20,
        "correct_answers": 20,
        "incorrect_answers": 0,
        "completion_time": 120.5,
        "completed_at": datetime.utcnow().isoformat(),
    }
    success = db.send_to_google_sheet(payload)
    if success:
        return jsonify({
            "status": "success",
            "message": "Test row successfully sent to your Google Sheet!"
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Could not connect to Google Sheet. Check your Webhook URL."
        }), 500


# ── Main ──────────────────────────────────────────────────────────────────────

@app.errorhandler(500)
def handle_500(e):
    import traceback
    return f"<h3>Application Error (500)</h3><pre>{traceback.format_exc()}</pre>", 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
