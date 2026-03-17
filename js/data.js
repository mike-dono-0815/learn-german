/**
 * data.js — Knowledge-base access and progress persistence.
 * Reads from KB_DATA (knowledge-base.js) and persists to localStorage.
 */
var App = window.App || {};

App.Data = (function () {

  var LS_PRG = 'ru_progress';     // per-word spaced-repetition state
  var LS_GLB = 'ru_global_stats'; // XP, level, session count

  /* ── Helpers ──────────────────────────────────────────────────── */

  function lsGet(key) {
    try { return JSON.parse(localStorage.getItem(key)); } catch(e) { return null; }
  }
  function lsSet(key, val) {
    try { localStorage.setItem(key, JSON.stringify(val)); } catch(e) {}
  }

  /* ── KNOWLEDGE-BASE ACCESS ────────────────────────────────────── */

  /**
   * All topics. topicId 0 is a synthetic "Alle Themen" entry.
   */
  function getTopics() {
    var topics = (KB_DATA.topics || []).slice();
    // Prepend "all topics"
    return [{ id: 0, name_de: 'Alle Themen', name_ru: '\u0432\u0441\u0435 \u0442\u0435\u043C\u044B' }].concat(topics);
  }

  /**
   * Vocabulary for a given topicId. topicId 0 = all vocabulary.
   */
  function getVocabulary(topicId) {
    if (topicId === 0) return KB_DATA.vocabulary.slice();
    return KB_DATA.vocabulary.filter(function(v) {
      return v.topic_ids && v.topic_ids.indexOf(topicId) !== -1;
    });
  }

  /**
   * Sentences for a given topicId. topicId 0 = all sentences.
   */
  function getSentences(topicId) {
    if (topicId === 0) return KB_DATA.sentences.slice();
    return KB_DATA.sentences.filter(function(s) {
      return s.topic_ids && s.topic_ids.indexOf(topicId) !== -1;
    });
  }

  /** Count of vocabulary words for a topic. */
  function getVocabCount(topicId) {
    return getVocabulary(topicId).length;
  }

  /** Count of sentences for a topic. */
  function getSentenceCount(topicId) {
    return getSentences(topicId).length;
  }

  /* ── PROGRESS PERSISTENCE ─────────────────────────────────────── */

  function getProgress() {
    return lsGet(LS_PRG) || { vocabulary: {}, sentences: {} };
  }

  function getWordProgress(type, id) {
    var prog    = getProgress();
    var section = prog[type] || {};
    return section[id] || { easeFactor: 1.0, correctCount: 0, wrongCount: 0, lastSeen: 0 };
  }

  function updateWordProgress(type, id, score) {
    var prog    = getProgress();
    var section = prog[type] || {};
    var entry   = section[id] || { easeFactor: 1.0, correctCount: 0, wrongCount: 0, lastSeen: 0 };

    entry.lastSeen = Date.now();

    if (score === 2) {
      entry.correctCount++;
      entry.easeFactor = Math.min(entry.easeFactor * 1.2, 4.0);
    } else if (score === 1) {
      entry.correctCount += 0.5;
    } else {
      entry.wrongCount++;
      entry.easeFactor = Math.max(entry.easeFactor * 0.6, 0.15);
    }

    section[id] = entry;
    prog[type]  = section;
    lsSet(LS_PRG, prog);
  }

  function getAllProgress() {
    return getProgress();
  }

  function resetAllStats() {
    lsSet(LS_PRG, null);
    lsSet(LS_GLB, null);
  }

  /* ── GLOBAL STATS ─────────────────────────────────────────────── */

  function getGlobalStats() {
    return lsGet(LS_GLB) || {
      totalXP: 0, level: 1, totalCorrect: 0, totalWrong: 0,
      bestStreak: 0, sessionsCompleted: 0
    };
  }

  function updateGlobalStats(patch) {
    var stats = getGlobalStats();
    Object.keys(patch).forEach(function(k) {
      if (k === 'totalXP' || k === 'totalCorrect' || k === 'totalWrong') {
        stats[k] = (stats[k] || 0) + patch[k];
      } else {
        stats[k] = patch[k];
      }
    });
    stats.level = xpToLevel(stats.totalXP);
    if (patch.streak && patch.streak > stats.bestStreak) {
      stats.bestStreak = patch.streak;
    }
    lsSet(LS_GLB, stats);
    return stats;
  }

  /* ── XP / LEVEL HELPERS ───────────────────────────────────────── */

  var XP_LEVELS = [0, 100, 250, 500, 900, 1500, 2500, 4000, 6000, 9000];

  function xpToLevel(xp) {
    for (var i = XP_LEVELS.length - 1; i >= 0; i--) {
      if (xp >= XP_LEVELS[i]) return i + 1;
    }
    return 1;
  }

  function xpForLevel(level) {
    return XP_LEVELS[Math.min(level - 1, XP_LEVELS.length - 1)];
  }

  function xpForNextLevel(level) {
    return XP_LEVELS[Math.min(level, XP_LEVELS.length - 1)];
  }

  /* ── PUBLIC API ───────────────────────────────────────────────── */
  return {
    getTopics:          getTopics,
    getVocabulary:      getVocabulary,
    getSentences:       getSentences,
    getVocabCount:      getVocabCount,
    getSentenceCount:   getSentenceCount,
    getWordProgress:    getWordProgress,
    updateWordProgress: updateWordProgress,
    getAllProgress:      getAllProgress,
    resetAllStats:      resetAllStats,
    getGlobalStats:     getGlobalStats,
    updateGlobalStats:  updateGlobalStats,
    xpToLevel:          xpToLevel,
    xpForLevel:         xpForLevel,
    xpForNextLevel:     xpForNextLevel
  };

}());

window.App = App;
