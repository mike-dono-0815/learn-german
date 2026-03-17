/**
 * checker.js — Answer validation for vocabulary mode.
 *
 * For DE→RU: accepts Cyrillic input OR Latin transliteration.
 * For RU→DE: accepts German (with lenient umlaut/diacritic handling).
 *
 * Returns { score: 0|1|2, label: string }
 *   2 = correct, 1 = partial, 0 = wrong
 */
var App = window.App || {};

App.Checker = (function () {

  /* ── Transliteration maps ─────────────────────────────────────── */

  // International / English-style (privet, zhizn, khorosho)
  var TRANSLIT_ISO = {
    '\u0430':'a', '\u0431':'b', '\u0432':'v', '\u0433':'g', '\u0434':'d',
    '\u0435':'e', '\u0451':'yo','\u0436':'zh','\u0437':'z', '\u0438':'i',
    '\u0439':'y', '\u043A':'k', '\u043B':'l', '\u043C':'m', '\u043D':'n',
    '\u043E':'o', '\u043F':'p', '\u0440':'r', '\u0441':'s', '\u0442':'t',
    '\u0443':'u', '\u0444':'f', '\u0445':'kh','\u0446':'ts','\u0447':'ch',
    '\u0448':'sh','\u0449':'shch','\u044A':'','\u044B':'y', '\u044C':'',
    '\u044D':'e', '\u044E':'yu','\u044F':'ya'
  };

  // German-style (privet/priwest, schisn, choroscho)
  var TRANSLIT_DE = {
    '\u0430':'a', '\u0431':'b', '\u0432':'w', '\u0433':'g', '\u0434':'d',
    '\u0435':'e', '\u0451':'jo','\u0436':'sch','\u0437':'s','\u0438':'i',
    '\u0439':'j', '\u043A':'k', '\u043B':'l', '\u043C':'m', '\u043D':'n',
    '\u043E':'o', '\u043F':'p', '\u0440':'r', '\u0441':'s', '\u0442':'t',
    '\u0443':'u', '\u0444':'f', '\u0445':'ch', '\u0446':'z', '\u0447':'tsch',
    '\u0448':'sch','\u0449':'schtsch','\u044A':'','\u044B':'y','\u044C':'',
    '\u044D':'e', '\u044E':'ju','\u044F':'ja'
  };

  function cyrillicToTranslit(str, map) {
    return str.toLowerCase().split('').map(function(c) {
      return map.hasOwnProperty(c) ? map[c] : c;
    }).join('');
  }

  /* ── Normalisation ────────────────────────────────────────────── */

  /** Detect if input is primarily Cyrillic. */
  function isCyrillicInput(str) {
    var cyrCount = (str.match(/[\u0400-\u04FF]/g) || []).length;
    return cyrCount >= 1;
  }

  /** Normalise Cyrillic for comparison: lowercase, collapse spaces. */
  function normCyrillic(str) {
    return (str || '').toLowerCase().replace(/\s+/g, ' ').trim();
  }

  /** Normalise German: lowercase, strip diacritics, collapse spaces. */
  function normGerman(str) {
    return (str || '')
      .toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/\s+/g, ' ')
      .trim();
  }

  /**
   * Normalise a Latin transliteration so that common variants match.
   * Applied to both the user's input and the transliterated answer
   * before comparing, so the match is lenient.
   */
  function normTranslit(str) {
    return str.toLowerCase()
      .replace(/schtsch/g, 'sc') // щ (German long form)
      .replace(/shch/g,    'sc') // щ (international)
      .replace(/tsch/g,    'c')  // ч (German)
      .replace(/sch/g,     's')  // ш (German)
      .replace(/sh/g,      's')  // ш (international)
      .replace(/zh/g,      'z')  // ж (international)
      .replace(/kh/g,      'h')  // х (international)
      .replace(/ts/g,      'z')  // ц (international)
      .replace(/yo/g,      'o')  // ё
      .replace(/jo/g,      'o')  // ё (German)
      .replace(/yu/g,      'u')  // ю
      .replace(/ju/g,      'u')  // ю (German)
      .replace(/ya/g,      'a')  // я
      .replace(/ja/g,      'a')  // я (German)
      .replace(/ye/g,      'e')  // е with y prefix
      .replace(/je/g,      'e')  // е (German)
      .replace(/w/g,       'v')  // в (German w → v)
      .replace(/\s+/g,     ' ')
      .trim();
  }

  /* ── Russian answer candidates ────────────────────────────────── */

  function russianCandidates(item) {
    var candidates = [item.russian || ''];
    (item.alternates_russian || []).forEach(function(alt) {
      candidates.push(alt);
    });
    // Split comma-separated primary (e.g. "да, конечно")
    (item.russian || '').split(',').forEach(function(part) {
      candidates.push(part.trim());
    });
    return candidates.filter(Boolean);
  }

  function germanCandidates(item) {
    var candidates = [item.german || ''];
    (item.alternates_german || []).forEach(function(alt) {
      candidates.push(alt);
    });
    (item.german || '').split(',').forEach(function(part) {
      candidates.push(part.trim());
    });
    return candidates.filter(Boolean);
  }

  /* ── Main check ───────────────────────────────────────────────── */

  function check(userAnswer, item, direction) {
    var raw = (userAnswer || '').trim();
    if (!raw) return { score: 0, label: 'Нет ответа' };

    if (direction === 'de-to-ru') {
      return checkDeToRu(raw, item);
    } else {
      return checkRuToDe(raw, item);
    }
  }

  /** DE→RU: accept Cyrillic or Latin transliteration. */
  function checkDeToRu(raw, item) {
    var candidates = russianCandidates(item);

    if (isCyrillicInput(raw)) {
      // Direct Cyrillic comparison
      var userCyr = normCyrillic(raw);
      for (var i = 0; i < candidates.length; i++) {
        if (userCyr === normCyrillic(candidates[i])) {
          return { score: 2, label: '\u2705 Верно!' };
        }
      }
      // Partial: matched one of comma-separated parts
      var primaryParts = (item.russian || '').split(',').map(function(p) { return p.trim(); });
      if (primaryParts.length > 1) {
        for (var pi = 0; pi < primaryParts.length; pi++) {
          if (userCyr === normCyrillic(primaryParts[pi])) {
            return { score: 1, label: '\u26A0\uFE0F Почти! (+½)' };
          }
        }
      }
    } else {
      // Latin transliteration comparison
      var userNorm = normTranslit(raw);
      for (var j = 0; j < candidates.length; j++) {
        var isoTranslit = cyrillicToTranslit(candidates[j], TRANSLIT_ISO);
        var deTranslit  = cyrillicToTranslit(candidates[j], TRANSLIT_DE);
        if (userNorm === normTranslit(isoTranslit) ||
            userNorm === normTranslit(deTranslit)) {
          return { score: 2, label: '\u2705 Верно!' };
        }
      }
      // Partial
      var primaryPartsList = (item.russian || '').split(',').map(function(p) { return p.trim(); });
      if (primaryPartsList.length > 1) {
        for (var pk = 0; pk < primaryPartsList.length; pk++) {
          var isoP = cyrillicToTranslit(primaryPartsList[pk], TRANSLIT_ISO);
          var deP  = cyrillicToTranslit(primaryPartsList[pk], TRANSLIT_DE);
          if (userNorm === normTranslit(isoP) ||
              userNorm === normTranslit(deP)) {
            return { score: 1, label: '\u26A0\uFE0F Почти! (+½)' };
          }
        }
      }
    }

    return { score: 0, label: '\u274C Неверно' };
  }

  /** RU→DE: accept German with lenient diacritic handling. */
  function checkRuToDe(raw, item) {
    var userNorm   = normGerman(raw);
    var candidates = germanCandidates(item);

    for (var i = 0; i < candidates.length; i++) {
      if (userNorm === normGerman(candidates[i])) {
        return { score: 2, label: '\u2705 Верно!' };
      }
    }

    // Partial: one of several comma-separated meanings
    var primaryParts = (item.german || '').split(',').map(function(p) { return p.trim(); });
    if (primaryParts.length > 1) {
      for (var j = 0; j < primaryParts.length; j++) {
        if (userNorm === normGerman(primaryParts[j])) {
          return { score: 1, label: '\u26A0\uFE0F Почти! (+½)' };
        }
      }
    }

    return { score: 0, label: '\u274C Неверно' };
  }

  /* ── Hint generation ──────────────────────────────────────────── */

  function getHint(item, direction, level) {
    if (direction === 'de-to-ru') {
      var ru = item.russian || '';
      if (level === 1) {
        return '\uD83D\uDD24 ' + (ru.charAt(0) || '?') + '\u2026';
      }
      return '\uD83D\uDD24 ' + ru.substring(0, 3) + '\u2026';
    } else {
      var de = item.german || '';
      if (level === 1) {
        return '\uD83D\uDD21 ' + de.charAt(0).toUpperCase() + '\u2026';
      }
      return '\uD83D\uDD21 ' + de.substring(0, 3) + '\u2026';
    }
  }

  /* ── Transliteration display ──────────────────────────────────── */

  /** Return a readable ISO transliteration of a Russian string for display. */
  function displayTranslit(str) {
    if (!str) return '';
    return cyrillicToTranslit(str, TRANSLIT_ISO);
  }

  return {
    check:          check,
    getHint:        getHint,
    displayTranslit:displayTranslit,
    normGerman:     normGerman,
    normCyrillic:   normCyrillic
  };

}());

window.App = App;
