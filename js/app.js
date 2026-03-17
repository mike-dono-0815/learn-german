/**
 * app.js — Main application controller.
 * Handles navigation, the practice loop, and statistics screen.
 */
var App = window.App || {};

/* ════════════════════════════════════════════════════════════════════
   GLOBAL STATE
═══════════════════════════════════════════════════════════════════ */
App.state = {
  screen:    'home',
  mode:      'vocabulary',   // 'vocabulary' | 'sentences'
  topicId:   1,              // 0 = all topics
  direction: 'de-to-ru',    // 'de-to-ru' | 'ru-to-de'
  session:   null
};

/* ════════════════════════════════════════════════════════════════════
   NAVIGATION
═══════════════════════════════════════════════════════════════════ */
App.navigate = function (screenName) {
  document.querySelectorAll('.screen').forEach(function (s) {
    s.classList.remove('active');
  });

  var target = document.getElementById('screen-' + screenName);
  if (target) target.classList.add('active');
  App.state.screen = screenName;

  if (screenName === 'home')  App._initHome();
  if (screenName === 'stats') App.Stats.render();
};

/* ════════════════════════════════════════════════════════════════════
   HOME SCREEN
═══════════════════════════════════════════════════════════════════ */
App._initHome = function () {
  var gs = App.Data.getGlobalStats();
  el('home-xp').textContent    = '\u2B50 ' + gs.totalXP + ' XP';
  el('home-level').textContent = 'Lv.' + gs.level;
  App._populateTopicSelect();
  App._updateTopicHint();
};

App._populateTopicSelect = function () {
  var sel = el('topic-select');
  if (!sel || sel.dataset.populated) return;
  sel.dataset.populated = '1';

  var topics = App.Data.getTopics();
  topics.forEach(function (t) {
    var opt = document.createElement('option');
    opt.value       = t.id;
    opt.textContent = t.name_de + (t.id === 0 ? '' : ' \u2014 ' + t.name_ru);
    sel.appendChild(opt);
  });

  // Restore last topic
  try {
    var saved = localStorage.getItem('ru_last_topic');
    if (saved !== null) {
      sel.value = saved;
      App.state.topicId = parseInt(saved, 10) || 0;
    }
  } catch(e) {}
};

App.setMode = function (mode) {
  App.state.mode = mode;
  document.querySelectorAll('#mode-group .btn-toggle').forEach(function (b) {
    b.classList.toggle('active', b.dataset.mode === mode);
  });
  App._updateTopicHint();
};

App.setTopic = function (topicId) {
  App.state.topicId = parseInt(topicId, 10) || 0;
  try { localStorage.setItem('ru_last_topic', App.state.topicId); } catch(e) {}
  App._updateTopicHint();
};

App.setDirection = function (dir) {
  App.state.direction = dir;
  document.querySelectorAll('#dir-group .btn-toggle').forEach(function (b) {
    b.classList.toggle('active', b.dataset.dir === dir);
  });
};

App._updateTopicHint = function () {
  var hint = el('topic-hint');
  if (!hint) return;
  var tid = App.state.topicId;
  if (App.state.mode === 'vocabulary') {
    hint.textContent = 'Содержит ' + App.Data.getVocabCount(tid) + ' слов';
  } else {
    hint.textContent = 'Содержит ' + App.Data.getSentenceCount(tid) + ' предложений';
  }
};

/* ════════════════════════════════════════════════════════════════════
   SESSION MANAGEMENT
═══════════════════════════════════════════════════════════════════ */
App.startSession = function () {
  var mode    = App.state.mode;
  var topicId = App.state.topicId;
  var items;

  if (mode === 'vocabulary') {
    items = App.Data.getVocabulary(topicId);
  } else {
    items = App.Data.getSentences(topicId);
  }

  if (!items || items.length === 0) {
    App.Celebration.showToast('\u26A0\uFE0F Записей не найдено', 'info');
    return;
  }

  var progressMap = {};
  var allProgress = App.Data.getAllProgress();
  var section     = (mode === 'vocabulary' ? allProgress.vocabulary : allProgress.sentences) || {};
  items.forEach(function (item) {
    progressMap[item.id] = section[item.id] || null;
  });

  // For large sets (>50), skip fixed rounds and go straight to weighted selection
  var largeSet = items.length > 50;

  App.state.session = {
    mode:        mode,
    topicId:     topicId,
    direction:   App.state.direction,
    items:       items,
    progressMap: progressMap,
    currentItem: null,
    lastItemId:  null,
    hintLevel:   0,
    streak:      0,
    bestStreak:  0,
    correct:     0,
    wrong:       0,
    partial:     0,
    xpEarned:    0,
    missedItems: [],
    roundsCompleted: largeSet ? 2 : 0,
    roundQueue:      largeSet ? [] : App.Scoring.shuffle(items.slice()),
    roundIndex:      0
  };

  App.navigate('practice');
  App._showNextItem();
};

App.quitSession = function () {
  App._endSession();
};

App._endSession = function () {
  var s = App.state.session;
  if (!s) { App.navigate('home'); return; }

  var oldLevel = App.Data.getGlobalStats().level;

  var gs = App.Data.updateGlobalStats({
    totalXP:           s.xpEarned,
    totalCorrect:      s.correct + s.partial,
    totalWrong:        s.wrong,
    streak:            s.bestStreak,
    sessionsCompleted: 1
  });

  if (gs.level > oldLevel) {
    App.Celebration.onLevelUp(gs.level);
  }

  el('se-correct').textContent = s.correct + (s.partial ? '+' + s.partial : '');
  el('se-wrong').textContent   = s.wrong;
  el('se-streak').textContent  = s.bestStreak;
  el('se-xp').textContent      = s.xpEarned;

  var missedSec  = el('se-missed-section');
  var missedList = el('se-missed-list');
  missedList.innerHTML = '';

  if (s.missedItems.length > 0) {
    missedSec.classList.remove('hidden');
    s.missedItems.forEach(function (item) {
      var li = document.createElement('li');
      li.innerHTML =
        '<span class="missed-de">' + esc(item.german  || item.text_de  || '') + '</span>' +
        '<span class="missed-ru">' + esc(item.russian || item.text_ru  || '') + '</span>';
      missedList.appendChild(li);
    });
  } else {
    missedSec.classList.add('hidden');
  }

  App.navigate('session-end');
};

/* ════════════════════════════════════════════════════════════════════
   PRACTICE LOOP
═══════════════════════════════════════════════════════════════════ */
App._pickNextItem = function (s) {
  if (s.roundsCompleted < 2) {
    if (s.roundIndex >= s.roundQueue.length) {
      s.roundsCompleted++;
      if (s.roundsCompleted < 2) {
        s.roundQueue = App.Scoring.shuffle(s.items.slice());
        s.roundIndex = 0;
      }
    }
    if (s.roundsCompleted < 2) {
      return s.roundQueue[s.roundIndex++];
    }
  }
  return App.Scoring.selectNext(s.items, s.progressMap, s.lastItemId);
};

App._showNextItem = function () {
  var s    = App.state.session;
  var item = App._pickNextItem(s);
  if (!item) { App._endSession(); return; }

  s.currentItem = item;
  s.lastItemId  = item.id;
  s.hintLevel   = 0;

  el('ph-streak').textContent  = s.streak;
  el('ph-correct').textContent = s.correct;
  el('ph-total').textContent   = s.correct + s.wrong;
  el('ph-xp').textContent      = s.xpEarned;

  var isVocab = s.mode === 'vocabulary';
  var dir     = s.direction;

  el('q-direction').textContent = dir === 'de-to-ru' ? 'DE \u2192 RU' : 'RU \u2192 DE';

  if (isVocab) {
    if (dir === 'de-to-ru') {
      el('q-text').textContent = item.german || '';
      el('q-grammar').textContent = item.grammar ? '(' + item.grammar + ')' : '';
      el('q-grammar').classList.toggle('hidden', !item.grammar);
    } else {
      el('q-text').textContent = item.russian || '';
      el('q-grammar').textContent = '';
      el('q-grammar').classList.add('hidden');
    }
  } else {
    el('q-text').textContent = dir === 'de-to-ru' ? (item.german || '') : (item.russian || '');
    el('q-grammar').textContent = '';
    el('q-grammar').classList.add('hidden');
  }

  el('q-hint-line').textContent = '';
  el('q-hint-line').classList.add('hidden');
  el('hint-btn').disabled = false;

  if (isVocab) {
    showPhase('input');
    var inp = el('answer-input');
    inp.value = '';
    setTimeout(function () { inp.focus(); }, 80);
  } else {
    showPhase('sentence-input');
    var sinp = el('sentence-input');
    sinp.value = '';
    setTimeout(function () { sinp.focus(); }, 80);
  }
};

/* ── Vocabulary: check answer ─────────────────────────────────── */
App.checkAnswer = function () {
  var s    = App.state.session;
  var item = s.currentItem;
  var inp  = el('answer-input');
  var raw  = inp.value;

  var result = App.Checker.check(raw, item, s.direction);

  App.Data.updateWordProgress('vocabulary', item.id, result.score);
  s.progressMap[item.id] = App.Data.getWordProgress('vocabulary', item.id);

  var xp = [0, 5, 10][result.score] + (s.streak >= 5 ? 2 : 0);
  s.xpEarned += xp;

  if (result.score === 2) {
    s.correct++;
    s.streak++;
  } else if (result.score === 1) {
    s.partial++;
    s.streak++;
  } else {
    s.wrong++;
    if (s.missedItems.indexOf(item) === -1) s.missedItems.push(item);
    s.streak = 0;
  }
  if (s.streak > s.bestStreak) s.bestStreak = s.streak;

  el('ph-streak').textContent  = s.streak;
  el('ph-correct').textContent = s.correct;
  el('ph-total').textContent   = s.correct + s.wrong;
  el('ph-xp').textContent      = s.xpEarned;

  var fbResult  = el('fb-result');
  var fbCorrect = el('fb-correct');
  var fbTranslit = el('fb-translit');
  var fbGrammar = el('fb-grammar');
  var fbAlts    = el('fb-alts');

  fbResult.className = 'fb-result ' + (['wrong','partial','correct'][result.score]);
  fbResult.textContent = result.label;

  if (result.score < 2) {
    // Show correct answer
    var correctStr = s.direction === 'de-to-ru' ? item.russian : item.german;
    fbCorrect.textContent = '\u2192 ' + correctStr;
  } else {
    var shownStr = s.direction === 'de-to-ru' ? item.russian : item.german;
    fbCorrect.textContent = shownStr;
  }

  // Transliteration (for Russian answers)
  if (s.direction === 'de-to-ru' && item.russian) {
    var translit = App.Checker.displayTranslit(item.russian);
    fbTranslit.textContent = translit;
    fbTranslit.classList.remove('hidden');
  } else {
    fbTranslit.classList.add('hidden');
  }

  // Grammar hint
  if (item.grammar) {
    fbGrammar.textContent = item.grammar;
    fbGrammar.classList.remove('hidden');
  } else {
    fbGrammar.classList.add('hidden');
  }

  // Alternates
  var alts = (item.alternates_russian || []).concat(item.alternates_german || []);
  if (alts.length > 0 && result.score > 0) {
    fbAlts.textContent = 'Также: ' + alts.slice(0,3).join(', ');
    fbAlts.classList.remove('hidden');
  } else {
    fbAlts.classList.add('hidden');
  }

  showPhase('feedback');

  App.Celebration.onStreakUpdate(s.streak);

  if (App.Scoring.isMastered(s.progressMap[item.id])) {
    App.Celebration.onWordMastered(item.german);
  }

  if (result.score === 0) {
    var card = el('question-card');
    card.classList.add('anim-shake');
    setTimeout(function() { card.classList.remove('anim-shake'); }, 500);
  }
};

App.nextWord = function () {
  App._showNextItem();
};

/* ── Sentences: reveal & self-grade ──────────────────────────── */
App.revealSentence = function () {
  var s    = App.state.session;
  var item = s.currentItem;
  var inp  = el('sentence-input');

  el('sg-attempt').textContent = inp.value.trim() || '(нет ввода)';

  var answerStr = s.direction === 'de-to-ru' ? item.russian : item.german;
  el('sg-answer').textContent = answerStr;

  // Show transliteration for Russian answers
  var sgTranslit = el('sg-translit');
  if (s.direction === 'de-to-ru' && item.russian) {
    sgTranslit.textContent = App.Checker.displayTranslit(item.russian);
    sgTranslit.classList.remove('hidden');
  } else {
    sgTranslit.classList.add('hidden');
  }

  showPhase('selfgrade');
};

App.skipSentence = function () {
  App.selfGrade(0);
};

App.selfGrade = function (score) {
  var s    = App.state.session;
  var item = s.currentItem;

  App.Data.updateWordProgress('sentences', item.id, score);
  s.progressMap[item.id] = App.Data.getWordProgress('sentences', item.id);

  var xp = [0, 5, 10][score] + (s.streak >= 5 ? 2 : 0);
  s.xpEarned += xp;

  if (score >= 1) {
    s.correct++;
    s.streak++;
  } else {
    s.wrong++;
    if (s.missedItems.indexOf(item) === -1) s.missedItems.push(item);
    s.streak = 0;
  }
  if (s.streak > s.bestStreak) s.bestStreak = s.streak;

  el('ph-streak').textContent  = s.streak;
  el('ph-correct').textContent = s.correct;
  el('ph-total').textContent   = s.correct + s.wrong;
  el('ph-xp').textContent      = s.xpEarned;

  App.Celebration.onStreakUpdate(s.streak);
  App._showNextItem();
};

/* ── Hint ─────────────────────────────────────────────────────── */
App.showHint = function () {
  var s = App.state.session;
  if (!s || !s.currentItem) return;

  s.hintLevel = Math.min(s.hintLevel + 1, 2);
  var hint = App.Checker.getHint(s.currentItem, s.direction, s.hintLevel);

  var hintLine = el('q-hint-line');
  hintLine.textContent = hint;
  hintLine.classList.remove('hidden');

  if (s.hintLevel >= 2) el('hint-btn').disabled = true;
};

/* ── Quick-grade ─────────────────────────────────────────────── */
App.autoGrade = function (score) {
  var s    = App.state.session;
  var item = s.currentItem;
  if (!item) return;

  var correctAnswer = s.direction === 'de-to-ru'
    ? item.russian
    : item.german;

  el('answer-input').value = score === 2 ? (correctAnswer || '') : '';
  App.checkAnswer();
};

/* ── Input key handler ────────────────────────────────────────── */
App.onInputKey = function (event) {
  if (event.key !== 'Enter') return;
  event.stopPropagation();
  App.checkAnswer();
};

/* ════════════════════════════════════════════════════════════════════
   STATS SCREEN
═══════════════════════════════════════════════════════════════════ */
App.Stats = {

  render: function () {
    var container = el('stats-main');
    if (!container) return;

    var gs     = App.Data.getGlobalStats();
    var prg    = App.Data.getAllProgress();
    var lv     = gs.level;
    var xp     = gs.totalXP;
    var xpThis = xp - App.Data.xpForLevel(lv);
    var xpNext = App.Data.xpForNextLevel(lv) - App.Data.xpForLevel(lv);
    var pct    = xpNext > 0 ? Math.min(Math.round((xpThis / xpNext) * 100), 100) : 100;

    var html =
      '<div class="stats-section-title">Общий обзор</div>' +
      '<div class="stats-grid">' +
        stat('\u2B50', xp + ' XP',       'Всего XP')          +
        stat('\uD83C\uDFC5', 'Level ' + lv, 'Текущий уровень') +
        stat('\u2705', gs.totalCorrect,   'Верно')             +
        stat('\u274C', gs.totalWrong,     'Неверно')           +
        stat('\uD83D\uDD25', gs.bestStreak, 'Лучшая серия')    +
        stat('\uD83D\uDCDA', gs.sessionsCompleted, 'Сессии')   +
      '</div>' +
      '<div class="xp-bar-wrap">' +
        '<div class="xp-bar-bg"><div class="xp-bar-fill" style="width:' + pct + '%"></div></div>' +
        '<div class="xp-bar-label">Level ' + lv + ' \u2192 Level ' + (lv+1) + ' \u00B7 ' + pct + '%</div>' +
      '</div>';

    // Per-word progress
    var vocabSection = prg.vocabulary || {};
    var wordItems = [];
    KB_DATA.vocabulary.forEach(function(item) {
      if (vocabSection[item.id]) {
        wordItems.push({ item: item, prog: vocabSection[item.id] });
      }
    });

    if (wordItems.length > 0) {
      wordItems.sort(function(a,b) {
        return App.Scoring.masteryPercent(a.prog) - App.Scoring.masteryPercent(b.prog);
      });

      html += '<div class="stats-section-title" style="margin-top:8px">Слова по уровню владения</div>';
      html += '<div class="word-progress-list">';
      wordItems.slice(0, 80).forEach(function(w) {
        var p     = App.Scoring.masteryPercent(w.prog);
        var color = p < 40 ? '#ef4444' : p < 70 ? '#ffd166' : '#06d6a0';
        html += '<div class="word-progress-item">' +
          '<span class="wpi-de">'  + esc(w.item.german)  + '</span>' +
          '<span class="wpi-ru">'  + esc(w.item.russian) + '</span>' +
          '<div class="wpi-bar"><div class="wpi-bar-fill" style="width:' + p + '%;background:' + color + '"></div></div>' +
          '<span class="wpi-pct">' + p + '%</span>' +
          '</div>';
      });
      html += '</div>';
    }

    container.innerHTML = html;

    function stat(icon, val, lbl) {
      return '<div class="stats-card">' +
        '<span style="font-size:1.4rem">' + icon + '</span>' +
        '<span class="stats-card-val">' + val + '</span>' +
        '<span class="stats-card-lbl">' + lbl + '</span>' +
        '</div>';
    }
  },

  resetAll: function () {
    if (!confirm('Сбросить весь прогресс и статистику?')) return;
    App.Data.resetAllStats();
    App.Celebration.showToast('\u21BA Статистика сброшена', 'info');
    App.Stats.render();
    App._initHome();
  }
};

/* ════════════════════════════════════════════════════════════════════
   UTILITY HELPERS
═══════════════════════════════════════════════════════════════════ */

function el(id) { return document.getElementById(id); }

function esc(str) {
  return (str || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function showPhase(name) {
  ['input','feedback','selfgrade','sentence-input'].forEach(function(n) {
    var ph = el('phase-' + n);
    if (ph) {
      if (n === name) ph.classList.add('active');
      else            ph.classList.remove('active');
    }
  });
  var qgi = el('quick-grade-inline');
  if (qgi) qgi.style.display = (name === 'input') ? 'flex' : 'none';
}

/* ════════════════════════════════════════════════════════════════════
   BOOT
═══════════════════════════════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', function () {
  App.setMode('vocabulary');
  App.setDirection('de-to-ru');

  // Restore last direction
  try {
    var savedDir = localStorage.getItem('ru_last_direction');
    if (savedDir === 'ru-to-de' || savedDir === 'de-to-ru') {
      App.setDirection(savedDir);
    }
  } catch(e) {}

  // Save direction on change
  document.querySelectorAll('#dir-group .btn-toggle').forEach(function(btn) {
    btn.addEventListener('click', function() {
      try { localStorage.setItem('ru_last_direction', btn.dataset.dir); } catch(e) {}
    });
  });

  App.navigate('splash');

  // Global Enter: advance from feedback phase
  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Enter') return;
    var feedback = el('phase-feedback');
    if (feedback && feedback.classList.contains('active')) {
      event.preventDefault();
      App.nextWord();
    }
  });
});

window.App = App;
