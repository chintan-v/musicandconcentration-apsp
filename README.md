# Background Music & Study Concentration — Research Website

**Project:** Does Background Music Affect Study Concentration? An ANOVA-Based Study  
**Course:** Advanced Probability and Stochastic Processes (APSP)

---

## Overview

A minimal Flask web application for conducting a controlled experiment that
examines whether background instrumental music influences cognitive task
performance. Participants complete two parallel cognitive tests under two
auditory conditions (silence and music). Results are stored in an SQLite
database and can be exported to CSV for ANOVA analysis.

---

## Project Structure

```
music_concentration/
│
├── app.py           — Flask routes and application logic
├── database.py      — SQLite helpers and CSV export
├── questions.py     — Form A and Form B question banks and answer keys
├── requirements.txt — Python dependencies
│
├── templates/
│   ├── index.html   — Home page (intro, consent, start)
│   ├── test1.html   — Test 1 (silence condition, Form A)
│   ├── break.html   — Rest page between tests
│   ├── test2.html   — Test 2 (music condition, Form B)
│   └── results.html — Individual results page
│
├── static/
│   ├── css/style.css     — All styles
│   ├── js/test.js        — Timer, navigation, submit logic
│   └── audio/            — Place study_music.mp3 here (see below)
│
└── data/
    └── research.db       — SQLite database (auto-created on first run)
```

---

## Quick Start

### 1. Prerequisites

- Python 3.10 or newer
- pip

### 2. Install dependencies

Open a terminal inside the `music_concentration/` folder and run:

```bash
pip install -r requirements.txt
```

### 3. Add the study music file

Place a royalty-free instrumental MP3 file in:

```
static/audio/study_music.mp3
```

Free sources:
- [Pixabay Music](https://pixabay.com/music/) — search "study" or "lofi"
- [Free Music Archive](https://freemusicarchive.org/) — filter by license
- [Mixkit](https://mixkit.co/free-stock-music/)

Then open `templates/test2.html` and **uncomment** this line:

```html
<!-- <source src="{{ url_for('static', filename='audio/study_music.mp3') }}" type="audio/mpeg"> -->
```

Remove the `<!--` and `-->` to activate the audio source.

> **Standardisation note:** All participants must use the same music file at a
> consistent, moderate volume. Before data collection begins, agree on a volume
> level and communicate it clearly in the on-screen instructions.

### 4. Run the application

```bash
python app.py
```

Open your browser and go to: **http://127.0.0.1:5000**

---

## Experiment Flow

1. **Home page** — Project description, instructions, consent checkbox.
2. **Test 1** — 20 questions, silence condition, Form A, 20-minute timer.
3. **Break page** — 2-minute countdown before Test 2 is accessible.
4. **Test 2** — 20 questions, music condition, Form B, 20-minute timer.
5. **Results page** — Individual scores and comparison. No group-level conclusion.

---

## Data Export

### JSON (quick inspection)

Open in a browser while the server is running:

```
http://127.0.0.1:5000/admin/data
```

### CSV (for ANOVA analysis)

```
http://127.0.0.1:5000/admin/export
```

The CSV is saved to `data/results_export.csv`.

### Python export script

```python
import sys
sys.path.insert(0, ".")   # run from music_concentration/
from database import export_to_csv

path = export_to_csv("data/results_export.csv")
print(f"Exported to {path}")
```

---

## Test Design Summary

Both forms use the same structure and equivalent difficulty:

| Category                  | Form A | Form B |
|---------------------------|:------:|:------:|
| Numerical Reasoning       |   5    |   5    |
| Logical Reasoning         |   5    |   5    |
| Pattern Recognition       |   5    |   5    |
| Attention & Working Memory|   5    |   5    |
| **Total**                 | **20** | **20** |

- Time limit: **20 minutes** per test  
- Scoring: **1 point per correct answer**, no penalty for wrong answers  
- Questions designed at equivalent medium difficulty  
- Tests are **not** validated psychometric instruments

---

## Modifying Questions

Edit `questions.py` to change, add, or remove questions. Maintain the
following invariants:

1. Both `FORM_A` and `FORM_B` must contain exactly **20** questions.
2. Each question must have exactly **4** options.
3. The `answer` field must match **exactly** one element in `options`.
4. After editing, update `ANSWER_KEY_A` and `ANSWER_KEY_B` if you change IDs
   (they are auto-generated from the list via dict comprehension).

---

## Notes on Statistical Analysis

After collecting data from sufficient participants, export to CSV and run a
one-way repeated-measures ANOVA in Python:

```python
import pandas as pd
from scipy import stats

df = pd.read_csv("data/results_export.csv")
silence = df[df["test_condition"] == "silence"]["score"]
music   = df[df["test_condition"] == "music"]["score"]

f_stat, p_value = stats.f_oneway(silence, music)
print(f"F = {f_stat:.4f}, p = {p_value:.4f}")
```

For a proper repeated-measures ANOVA, use `pingouin` or `statsmodels`:

```bash
pip install pingouin
```

```python
import pingouin as pg

aov = pg.rm_anova(data=df, dv="score", within="test_condition", subject="participant_id")
print(aov)
```

---

## License

This project was created for academic research purposes.  
Question content is original and not derived from any copyrighted test instrument.
