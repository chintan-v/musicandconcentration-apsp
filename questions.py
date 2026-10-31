"""
questions.py — Cognitive test question banks for the APSP research project.

Both Form A (Test 1, silence) and Form B (Test 2, music) are designed to be
parallel in structure, difficulty, and cognitive demand, following principles of
equivalent / parallel test forms used in psychometric research.

Categories per form:
  Numerical Reasoning          — 5 questions  (IDs *1–*5)
  Logical Reasoning            — 5 questions  (IDs *6–*10)
  Pattern Recognition          — 5 questions  (IDs *11–*15)
  Attention & Working Memory   — 5 questions  (IDs *16–*20)
  Total: 20 questions per form, 20-minute time limit.

Each question dict:
  id        : unique identifier within the form  (e.g. "A1", "B7")
  category  : human-readable category name
  text      : question stem shown to the participant
  options   : list of exactly 4 answer strings
  answer    : correct option (must match exactly one element in options)
  difficulty: both forms calibrated to equivalent medium difficulty
"""

# ─────────────────────────────────────────────────────────────────────────────
# Form A  — Test 1 (silence condition)
# ─────────────────────────────────────────────────────────────────────────────

FORM_A = [

    # ── Numerical Reasoning (A1–A5) ──────────────────────────────────────────
    {
        "id": "A1",
        "category": "Numerical Reasoning",
        "text": (
            "A researcher records 5 reaction times (in ms): 340, 280, 310, 295, 275. "
            "What is the mean reaction time?"
        ),
        "options": ["295 ms", "300 ms", "285 ms", "310 ms"],
        "answer": "300 ms",
        "difficulty": "medium",
    },
    {
        "id": "A2",
        "category": "Numerical Reasoning",
        "text": (
            "A student scores 64 out of 80 on a test. "
            "What percentage did the student score?"
        ),
        "options": ["78%", "80%", "75%", "70%"],
        "answer": "80%",
        "difficulty": "medium",
    },
    {
        "id": "A3",
        "category": "Numerical Reasoning",
        "text": (
            "If 3 tasks take 45 minutes in total and each task takes the same time, "
            "how long does it take to complete 7 tasks?"
        ),
        "options": ["90 min", "95 min", "100 min", "105 min"],
        "answer": "105 min",
        "difficulty": "medium",
    },
    {
        "id": "A4",
        "category": "Numerical Reasoning",
        "text": (
            "A value increases from 120 to 156. "
            "What is the percentage increase?"
        ),
        "options": ["25%", "30%", "36%", "20%"],
        "answer": "30%",
        "difficulty": "medium",
    },
    {
        "id": "A5",
        "category": "Numerical Reasoning",
        "text": (
            "The sum of three consecutive even integers is 78. "
            "What is the largest of the three integers?"
        ),
        "options": ["24", "26", "28", "30"],
        "answer": "28",
        "difficulty": "medium",
    },

    # ── Logical Reasoning (A6–A10) ────────────────────────────────────────────
    {
        "id": "A6",
        "category": "Logical Reasoning",
        "text": (
            "All researchers are scientists. Some scientists are professors. "
            "Which conclusion is definitely true?"
        ),
        "options": [
            "All researchers are professors.",
            "Some researchers may be professors.",
            "No researchers are professors.",
            "All professors are researchers.",
        ],
        "answer": "Some researchers may be professors.",
        "difficulty": "medium",
    },
    {
        "id": "A7",
        "category": "Logical Reasoning",
        "text": (
            "If it rains, the ground gets wet. The ground is not wet. "
            "Which conclusion follows?"
        ),
        "options": [
            "It is raining.",
            "It did not rain.",
            "It may or may not have rained.",
            "The ground is dry because it is sunny.",
        ],
        "answer": "It did not rain.",
        "difficulty": "medium",
    },
    {
        "id": "A8",
        "category": "Logical Reasoning",
        "text": (
            "A is taller than B. C is shorter than B. "
            "Which statement is definitely true?"
        ),
        "options": [
            "C is taller than A.",
            "B is the tallest.",
            "A is taller than C.",
            "C and B are the same height.",
        ],
        "answer": "A is taller than C.",
        "difficulty": "medium",
    },
    {
        "id": "A9",
        "category": "Logical Reasoning",
        "text": (
            "Every weekday, Maya either walks or cycles to work. "
            "On Monday she did not walk. "
            "What can be concluded about Monday?"
        ),
        "options": [
            "Maya did not go to work on Monday.",
            "Maya cycled to work on Monday.",
            "Maya drove to work on Monday.",
            "No conclusion can be drawn.",
        ],
        "answer": "Maya cycled to work on Monday.",
        "difficulty": "medium",
    },
    {
        "id": "A10",
        "category": "Logical Reasoning",
        "text": (
            "Statement: 'Only if a participant gives consent will their data be used.' "
            "A participant's data IS being used. What follows?"
        ),
        "options": [
            "The participant has given consent.",
            "The participant has not given consent.",
            "Consent is not required.",
            "No conclusion is possible.",
        ],
        "answer": "The participant has given consent.",
        "difficulty": "medium",
    },

    # ── Pattern Recognition (A11–A15) ─────────────────────────────────────────
    {
        "id": "A11",
        "category": "Pattern Recognition",
        "text": "What is the next number in the sequence?  2, 6, 18, 54, ___",
        "options": ["108", "160", "162", "180"],
        "answer": "162",
        "difficulty": "medium",
    },
    {
        "id": "A12",
        "category": "Pattern Recognition",
        "text": "What is the next number in the sequence?  1, 4, 9, 16, 25, ___",
        "options": ["32", "36", "49", "30"],
        "answer": "36",
        "difficulty": "medium",
    },
    {
        "id": "A13",
        "category": "Pattern Recognition",
        "text": (
            "The letters skip an increasing number of positions in the alphabet: "
            "A (+2) C (+3) F (+4) J  ___"
        ),
        "options": ["M", "N", "O", "P"],
        "answer": "O",
        "difficulty": "medium",
    },
    {
        "id": "A14",
        "category": "Pattern Recognition",
        "text": (
            "In a sequence, each term equals twice the previous term minus 5. "
            "The first term is 4. What is the fourth term?"
        ),
        "options": ["7", "9", "19", "23"],
        "answer": "19",
        "difficulty": "medium",
    },
    {
        "id": "A15",
        "category": "Pattern Recognition",
        "text": "What is the missing number?  3,  7,  13,  21,  ___,  43",
        "options": ["29", "31", "33", "35"],
        "answer": "31",
        "difficulty": "medium",
    },

    # ── Attention & Working Memory (A16–A20) ──────────────────────────────────
    {
        "id": "A16",
        "category": "Attention & Working Memory",
        "text": (
            "Study the list below, then answer without re-reading it:\n"
            "Pen, Clock, Apple, Train, Shoe, River, Lamp\n\n"
            "How many items in the list are living things or natural objects?"
        ),
        "options": ["1", "2", "3", "4"],
        "answer": "2",
        "difficulty": "medium",
    },
    {
        "id": "A17",
        "category": "Attention & Working Memory",
        "text": (
            "Memorise this digit string:  8  3  7  1  5\n\n"
            "What is the correct reverse order of those digits?"
        ),
        "options": [
            "5, 1, 7, 3, 8",
            "1, 5, 3, 8, 7",
            "8, 5, 1, 7, 3",
            "5, 7, 3, 8, 1",
        ],
        "answer": "5, 1, 7, 3, 8",
        "difficulty": "medium",
    },
    {
        "id": "A18",
        "category": "Attention & Working Memory",
        "text": (
            "Study this mixed sequence carefully:  B  4  M  9  T  2  K\n\n"
            "Which letter immediately follows the number 9?"
        ),
        "options": ["M", "B", "T", "K"],
        "answer": "T",
        "difficulty": "medium",
    },
    {
        "id": "A19",
        "category": "Attention & Working Memory",
        "text": (
            "Count every occurrence of the letter E in the sentence below "
            "(uppercase and lowercase):\n\n"
            "'The experiment measures the effect of background noise on performance.'"
        ),
        "options": ["7", "8", "9", "10"],
        "answer": "9",
        "difficulty": "medium",
    },
    {
        "id": "A20",
        "category": "Attention & Working Memory",
        "text": (
            "A participant presses a button for every vowel (A, E, I, O, U) they see.\n"
            "Sequence:  G  A  T  E  R  I  K  O  P\n\n"
            "How many button presses are required?"
        ),
        "options": ["3", "4", "5", "6"],
        "answer": "4",
        "difficulty": "medium",
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Form B  — Test 2 (music condition)
# ─────────────────────────────────────────────────────────────────────────────

FORM_B = [

    # ── Numerical Reasoning (B1–B5) ──────────────────────────────────────────
    {
        "id": "B1",
        "category": "Numerical Reasoning",
        "text": (
            "A researcher records 5 response times (in ms): 320, 260, 300, 285, 285. "
            "What is the mean response time?"
        ),
        "options": ["285 ms", "290 ms", "295 ms", "300 ms"],
        "answer": "290 ms",
        "difficulty": "medium",
    },
    {
        "id": "B2",
        "category": "Numerical Reasoning",
        "text": (
            "A student scores 57 out of 75 on a test. "
            "What percentage did the student score?"
        ),
        "options": ["72%", "74%", "76%", "80%"],
        "answer": "76%",
        "difficulty": "medium",
    },
    {
        "id": "B3",
        "category": "Numerical Reasoning",
        "text": (
            "If 4 tasks take 60 minutes in total and each task takes the same time, "
            "how long does it take to complete 9 tasks?"
        ),
        "options": ["120 min", "125 min", "130 min", "135 min"],
        "answer": "135 min",
        "difficulty": "medium",
    },
    {
        "id": "B4",
        "category": "Numerical Reasoning",
        "text": (
            "A value decreases from 200 to 155. "
            "What is the percentage decrease?"
        ),
        "options": ["20%", "22.5%", "25%", "27.5%"],
        "answer": "22.5%",
        "difficulty": "medium",
    },
    {
        "id": "B5",
        "category": "Numerical Reasoning",
        "text": (
            "The sum of three consecutive odd integers is 81. "
            "What is the largest of the three integers?"
        ),
        "options": ["25", "27", "29", "31"],
        "answer": "29",
        "difficulty": "medium",
    },

    # ── Logical Reasoning (B6–B10) ────────────────────────────────────────────
    {
        "id": "B6",
        "category": "Logical Reasoning",
        "text": (
            "All statisticians use data. Some data analysts are statisticians. "
            "Which conclusion is definitely true?"
        ),
        "options": [
            "All data analysts use data.",
            "Some statisticians are data analysts.",
            "No data analysts use data.",
            "All statisticians are data analysts.",
        ],
        "answer": "Some statisticians are data analysts.",
        "difficulty": "medium",
    },
    {
        "id": "B7",
        "category": "Logical Reasoning",
        "text": (
            "If the alarm sounds, participants must stop the test. "
            "Participants did not stop the test. "
            "Which conclusion follows?"
        ),
        "options": [
            "The alarm sounded.",
            "The alarm did not sound.",
            "Participants ignored the alarm.",
            "The test ended early.",
        ],
        "answer": "The alarm did not sound.",
        "difficulty": "medium",
    },
    {
        "id": "B8",
        "category": "Logical Reasoning",
        "text": (
            "X scores higher than Y. Z scores lower than Y. "
            "Which statement is definitely true?"
        ),
        "options": [
            "Z scores higher than X.",
            "Y scores the highest.",
            "X scores higher than Z.",
            "Z and Y have the same score.",
        ],
        "answer": "X scores higher than Z.",
        "difficulty": "medium",
    },
    {
        "id": "B9",
        "category": "Logical Reasoning",
        "text": (
            "Every day, a lab assistant either emails or calls the supervisor. "
            "On Thursday the assistant did not send an email. "
            "What can be concluded about Thursday?"
        ),
        "options": [
            "The assistant did not contact the supervisor on Thursday.",
            "The assistant called the supervisor on Thursday.",
            "The assistant sent a text message on Thursday.",
            "No conclusion can be drawn.",
        ],
        "answer": "The assistant called the supervisor on Thursday.",
        "difficulty": "medium",
    },
    {
        "id": "B10",
        "category": "Logical Reasoning",
        "text": (
            "Statement: 'Only if a study is peer-reviewed will it be published.' "
            "A study IS published. What follows?"
        ),
        "options": [
            "The study has been peer-reviewed.",
            "The study has not been peer-reviewed.",
            "Peer review is optional.",
            "No conclusion is possible.",
        ],
        "answer": "The study has been peer-reviewed.",
        "difficulty": "medium",
    },

    # ── Pattern Recognition (B11–B15) ─────────────────────────────────────────
    {
        "id": "B11",
        "category": "Pattern Recognition",
        "text": "What is the next number in the sequence?  3, 9, 27, 81, ___",
        "options": ["162", "243", "270", "324"],
        "answer": "243",
        "difficulty": "medium",
    },
    {
        "id": "B12",
        "category": "Pattern Recognition",
        "text": "What is the next number in the sequence?  1, 3, 6, 10, 15, ___",
        "options": ["18", "20", "21", "24"],
        "answer": "21",
        "difficulty": "medium",
    },
    {
        "id": "B13",
        "category": "Pattern Recognition",
        "text": (
            "The letters skip an increasing number of positions in the alphabet: "
            "B (+3) E (+4) I (+5) N  ___"
        ),
        "options": ["S", "T", "U", "V"],
        "answer": "T",
        "difficulty": "medium",
    },
    {
        "id": "B14",
        "category": "Pattern Recognition",
        "text": (
            "In a sequence, each term equals twice the previous term plus 3. "
            "The first term is 2. What is the fourth term?"
        ),
        "options": ["31", "35", "38", "45"],
        "answer": "38",
        "difficulty": "medium",
    },
    {
        "id": "B15",
        "category": "Pattern Recognition",
        "text": "What is the missing number?  2,  5,  10,  17,  ___,  37",
        "options": ["24", "25", "26", "28"],
        "answer": "26",
        "difficulty": "medium",
    },

    # ── Attention & Working Memory (B16–B20) ──────────────────────────────────
    {
        "id": "B16",
        "category": "Attention & Working Memory",
        "text": (
            "Study the list below, then answer without re-reading it:\n"
            "Desk, Sun, Bottle, Cloud, Chair, Stone, Pencil\n\n"
            "How many items in the list are natural objects?"
        ),
        "options": ["1", "2", "3", "4"],
        "answer": "3",
        "difficulty": "medium",
    },
    {
        "id": "B17",
        "category": "Attention & Working Memory",
        "text": (
            "Memorise this digit string:  6  2  9  4  7\n\n"
            "What is the correct reverse order of those digits?"
        ),
        "options": [
            "7, 4, 9, 2, 6",
            "4, 7, 2, 9, 6",
            "6, 9, 4, 2, 7",
            "7, 9, 4, 2, 6",
        ],
        "answer": "7, 4, 9, 2, 6",
        "difficulty": "medium",
    },
    {
        "id": "B18",
        "category": "Attention & Working Memory",
        "text": (
            "Study this mixed sequence carefully:  D  7  N  3  R  5  W\n\n"
            "Which letter immediately follows the number 3?"
        ),
        "options": ["N", "D", "R", "W"],
        "answer": "R",
        "difficulty": "medium",
    },
    {
        "id": "B19",
        "category": "Attention & Working Memory",
        "text": (
            "Count every occurrence of the letter T in the sentence below "
            "(uppercase and lowercase):\n\n"
            "'Attention and concentration tests target the participant's thinking ability.'"
        ),
        "options": ["7", "8", "9", "10"],
        "answer": "9",
        "difficulty": "medium",
    },
    {
        "id": "B20",
        "category": "Attention & Working Memory",
        "text": (
            "A participant presses a button for every consonant they see.\n"
            "Sequence:  A  M  E  K  U  R  I  S  O\n\n"
            "How many button presses are required?"
        ),
        "options": ["3", "4", "5", "6"],
        "answer": "4",
        "difficulty": "medium",
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Answer keys — keyed by question id for O(1) lookup during scoring
# ─────────────────────────────────────────────────────────────────────────────

ANSWER_KEY_A = {q["id"]: q["answer"] for q in FORM_A}
ANSWER_KEY_B = {q["id"]: q["answer"] for q in FORM_B}
