/**
 * scoring.js — Weighted random word selection (spaced repetition).
 *
 * Words you struggle with get a higher weight and appear more often.
 * A recency boost ensures unseen words eventually resurface.
 */
var App = window.App || {};

App.Scoring = (function () {

  function selectNext(items, progressMap, lastId) {
    if (!items || items.length === 0) return null;

    var pool = items.length > 1
      ? items.filter(function(it) { return it.id !== lastId; })
      : items;

    var weights = pool.map(function(item) {
      return computeWeight(progressMap[item.id]);
    });

    var total = weights.reduce(function(s, w) { return s + w; }, 0);
    var r = Math.random() * total;
    var cumulative = 0;

    for (var i = 0; i < pool.length; i++) {
      cumulative += weights[i];
      if (r <= cumulative) return pool[i];
    }
    return pool[pool.length - 1];
  }

  function computeWeight(prog) {
    if (!prog) return 3.0;

    var total   = prog.correctCount + prog.wrongCount;
    var mastery = total > 0 ? prog.correctCount / total : 0;
    var base    = Math.max(1 - mastery, 0.05);

    var daysSince = prog.lastSeen
      ? (Date.now() - prog.lastSeen) / 86400000
      : 30;
    var recency = Math.min(1 + daysSince * 0.15, 2.5);

    var wrongBoost = prog.wrongCount > 0
      ? 1 + Math.min(prog.wrongCount * 0.1, 0.8)
      : 1;

    return base * recency * wrongBoost;
  }

  function masteryPercent(prog) {
    if (!prog) return 0;
    var total = prog.correctCount + prog.wrongCount;
    if (total === 0) return 0;
    return Math.round((prog.correctCount / total) * 100);
  }

  function isMastered(prog) {
    if (!prog) return false;
    var total = prog.correctCount + prog.wrongCount;
    return total >= 5 && (prog.correctCount / total) >= 0.85;
  }

  function shuffle(arr) {
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
    }
    return arr;
  }

  return {
    selectNext:    selectNext,
    computeWeight: computeWeight,
    masteryPercent:masteryPercent,
    isMastered:    isMastered,
    shuffle:       shuffle
  };

}());

window.App = App;
