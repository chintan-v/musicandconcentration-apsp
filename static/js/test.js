/**
 * test.js — Shared client-side logic for Test 1 and Test 2.
 *
 * Handles:
 *   - Question navigation (one question at a time)
 *   - Countdown timer (20 minutes)
 *   - Answer tracking
 *   - Answer dot status updates
 *   - Auto-submit on timer expiry
 *   - Manual submit with confirmation
 *   - POST to Flask backend (JSON)
 *   - Music player toggle (Test 2 only)
 */

(function () {
  "use strict";

  // ── Configuration (set by inline script in each template) ────────────────
  // window.TEST_CONFIG = { submitUrl, breakUrl, totalQuestions, timeLimitSeconds }

  const CFG = window.TEST_CONFIG || {};
  const TOTAL_Q    = CFG.totalQuestions   || 20;
  const TIME_LIMIT = CFG.timeLimitSeconds || 1200; // 20 minutes

  // ── State ────────────────────────────────────────────────────────────────
  let currentIndex = 0;
  let answers      = {};          // { questionId: selectedOptionText }
  let startTime    = Date.now();
  let timerInterval = null;
  let submitted    = false;

  // ── DOM references ───────────────────────────────────────────────────────
  const questionCards = document.querySelectorAll(".question-card");
  const dots          = document.querySelectorAll(".q-dot");
  const timerEl       = document.getElementById("timer-display");
  const btnPrev       = document.getElementById("btn-prev");
  const btnNext       = document.getElementById("btn-next");
  const btnSubmit     = document.getElementById("btn-submit");
  const answeredCount = document.getElementById("answered-count");
  const progressFill  = document.getElementById("progress-fill");

  // ── Initialise ───────────────────────────────────────────────────────────
  function init() {
    showQuestion(0);
    startTimer();
    attachNavListeners();
    attachOptionListeners();
    attachDotListeners();
    attachSubmitListener();
  }

  // ── Show a specific question ──────────────────────────────────────────────
  function showQuestion(index) {
    questionCards.forEach(function (card, i) {
      card.style.display = i === index ? "block" : "none";
    });

    dots.forEach(function (dot, i) {
      dot.classList.toggle("current", i === index);
    });

    currentIndex = index;

    if (btnPrev) btnPrev.disabled = (index === 0);
    if (btnNext) btnNext.disabled = (index === TOTAL_Q - 1);
  }

  // ── Navigation listeners ──────────────────────────────────────────────────
  function attachNavListeners() {
    if (btnPrev) {
      btnPrev.addEventListener("click", function () {
        if (currentIndex > 0) showQuestion(currentIndex - 1);
      });
    }
    if (btnNext) {
      btnNext.addEventListener("click", function () {
        if (currentIndex < TOTAL_Q - 1) showQuestion(currentIndex + 1);
      });
    }
  }

  // ── Option selection ──────────────────────────────────────────────────────
  function attachOptionListeners() {
    questionCards.forEach(function (card) {
      const qid    = card.dataset.qid;
      const radios = card.querySelectorAll("input[type='radio']");

      radios.forEach(function (radio) {
        // Restore previously selected option
        if (answers[qid] && radio.value === answers[qid]) {
          radio.checked = true;
          highlightSelected(card, radio);
        }

        radio.addEventListener("change", function () {
          answers[qid] = radio.value;
          highlightSelected(card, radio);
          markDotAnswered(qid);
          updateProgress();
        });
      });
    });
  }

  function highlightSelected(card, selectedRadio) {
    card.querySelectorAll(".option-item").forEach(function (item) {
      item.classList.remove("selected");
    });
    if (selectedRadio && selectedRadio.checked) {
      selectedRadio.closest(".option-item").classList.add("selected");
    }
  }

  // ── Dot listeners ─────────────────────────────────────────────────────────
  function attachDotListeners() {
    dots.forEach(function (dot, i) {
      dot.addEventListener("click", function () {
        showQuestion(i);
      });
    });
  }

  function markDotAnswered(qid) {
    dots.forEach(function (dot) {
      if (dot.dataset.qid === qid) {
        dot.classList.add("answered");
      }
    });
  }

  // ── Progress ───────────────────────────────────────────────────────────────
  function updateProgress() {
    const count = Object.keys(answers).length;
    if (answeredCount) answeredCount.textContent = count;
    if (progressFill)  progressFill.style.width = ((count / TOTAL_Q) * 100) + "%";
  }

  // ── Timer ──────────────────────────────────────────────────────────────────
  function startTimer() {
    if (!timerEl) return;
    timerInterval = setInterval(function () {
      var elapsed  = Math.floor((Date.now() - startTime) / 1000);
      var remaining = Math.max(0, TIME_LIMIT - elapsed);
      var mins = Math.floor(remaining / 60);
      var secs = remaining % 60;
      timerEl.textContent = pad(mins) + ":" + pad(secs);

      timerEl.classList.remove("timer-warning", "timer-critical");
      if (remaining <= 120) timerEl.classList.add("timer-warning");
      if (remaining <= 30)  timerEl.classList.add("timer-critical");

      if (remaining === 0) {
        clearInterval(timerInterval);
        autoSubmit();
      }
    }, 1000);
  }

  function pad(n) {
    return n < 10 ? "0" + n : "" + n;
  }

  // ── Submit ─────────────────────────────────────────────────────────────────
  function attachSubmitListener() {
    if (btnSubmit) {
      btnSubmit.addEventListener("click", function () {
        var unanswered = TOTAL_Q - Object.keys(answers).length;
        if (unanswered > 0) {
          var ok = window.confirm(
            unanswered + " question(s) are unanswered. Submit anyway?"
          );
          if (!ok) return;
        }
        doSubmit();
      });
    }
  }

  function autoSubmit() {
    if (!submitted) doSubmit();
  }

  function doSubmit() {
    if (submitted) return;
    submitted = true;
    clearInterval(timerInterval);

    if (btnSubmit) btnSubmit.disabled = true;
    if (btnPrev)   btnPrev.disabled   = true;
    if (btnNext)   btnNext.disabled   = true;

    var elapsed = Math.floor((Date.now() - startTime) / 1000);

    fetch(CFG.submitUrl, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ answers: answers, elapsed_seconds: elapsed }),
    })
      .then(function (r) {
        return r.json().catch(function () {
          return { redirect: null };
        });
      })
      .then(function (data) {
        if (data && data.redirect) {
          window.location.href = data.redirect;
        } else {
          var fallback = CFG.submitUrl.indexOf("test1") !== -1 ? "/break" : "/results";
          window.location.href = fallback;
        }
      })
      .catch(function (err) {
        console.warn("Submit warning:", err);
        var fallback = CFG.submitUrl.indexOf("test1") !== -1 ? "/break" : "/results";
        window.location.href = fallback;
      });
  }

  // ── Music player (Test 2 only) ─────────────────────────────────────────────
  function initMusicPlayer() {
    var audio      = document.getElementById("study-audio");
    var toggleBtn  = document.getElementById("music-toggle");

    if (!audio || !toggleBtn) return;

    // Never autoplay — participant must start manually
    audio.volume = 0.6;

    toggleBtn.addEventListener("click", function () {
      if (audio.paused) {
        audio.play().then(function () {
          toggleBtn.textContent = "⏸ Pause Music";
        }).catch(function (e) {
          console.warn("Audio play error:", e);
        });
      } else {
        audio.pause();
        toggleBtn.textContent = "▶ Play Music";
      }
    });
  }

  // ── Boot ──────────────────────────────────────────────────────────────────
  document.addEventListener("DOMContentLoaded", function () {
    init();
    initMusicPlayer();
  });

})();
