#!/usr/bin/env python3
"""
parse_vocab.py  –  Goethe A2 vocabulary parser
Reads : Deutsch_Russisch_Cut.txt
Writes: vocabulary.json
"""

import json, re, sys, os

TXT_FILE = "Deutsch_Russisch_Cut.txt"
OUT_FILE = "vocabulary.json"

# ── TOPICS ────────────────────────────────────────────────────────────────────
TOPICS = [
    {"id":  1, "name_de": "Familie & Beziehungen",  "name_ru": "семья и отношения"},
    {"id":  2, "name_de": "Essen & Trinken",         "name_ru": "еда и напитки"},
    {"id":  3, "name_de": "Wohnen & Einrichten",     "name_ru": "жильё и обустройство"},
    {"id":  4, "name_de": "Arbeit & Beruf",          "name_ru": "работа и профессия"},
    {"id":  5, "name_de": "Schule & Bildung",        "name_ru": "школа и образование"},
    {"id":  6, "name_de": "Reise & Transport",       "name_ru": "путешествия и транспорт"},
    {"id":  7, "name_de": "Gesundheit & Körper",     "name_ru": "здоровье и тело"},
    {"id":  8, "name_de": "Freizeit & Unterhaltung", "name_ru": "досуг и развлечения"},
    {"id":  9, "name_de": "Sport & Bewegung",        "name_ru": "спорт и активность"},
    {"id": 10, "name_de": "Einkaufen & Geld",        "name_ru": "покупки и деньги"},
    {"id": 11, "name_de": "Kommunikation & Technik", "name_ru": "общение и технологии"},
    {"id": 12, "name_de": "Natur & Wetter",          "name_ru": "природа и погода"},
    {"id": 13, "name_de": "Zeit & Kalender",         "name_ru": "время и календарь"},
    {"id": 14, "name_de": "Gefühle & Charakter",     "name_ru": "чувства и характер"},
    {"id": 15, "name_de": "Stadt & Orientierung",    "name_ru": "город и ориентирование"},
]

TOPIC_KW = {
    1:  ["bruder","schwester","mutter","vater","kind","familie","eltern","tochter",
         "sohn","großeltern","oma","opa","onkel","tante","cousin","enkelin","enkel",
         "verwandte","heirat","hochzeit","verheiratet","ledig","geschieden","freund",
         "freundin","bekannt","beziehung","haushalt"],
    2:  ["essen","trinken","kochen","küche","restaurant","mahlzeit","frühstück",
         "mittagessen","abendessen","speise","getränk","obst","gemüse","fleisch",
         "fisch","brot","milch","kaffee","tee","wein","bier","wasser","salat","suppe",
         "kuchen","butter","käse","ei","zucker","salz","öl","apfel","banane","bohne",
         "kartoffel","nudel","reis","brötchen","hunger","durst","schmeck","rezept",
         "portion","kellner","speisekarte","braten","würst","snack","vegetarisch",
         "vegan","allergie","zutaten"],
    3:  ["wohnen","wohnung","haus","zimmer","bad","schlafzimmer","wohnzimmer",
         "möbel","tisch","stuhl","bett","schrank","sofa","fenster","tür","miete",
         "einricht","putzen","kühlschrank","waschmaschine","aufräumen","aufzug",
         "keller","garten","balkon","heizung","lampe","boden","decke","wand",
         "dusche","badewanne","toilette","garage","hausflur","einzug","umzug",
         "renovier","einwohner","haustür","nachbar","quadratmeter"],
    4:  ["arbeit","beruf","stelle","büro","firma","kollege","ausbildung","bewerb",
         "gehalt","lohn","kündigen","arbeitslos","rente","angestellter","doktor",
         "kellner","friseur","polizist","mechaniker","lehrer","lehrerin","bäcker",
         "fahrer","rentner","musiker","sänger","arzt","ärztin","journalist",
         "hausfrau","hausmann","verkäufer","techniker","handwerker","autor"],
    5:  ["schule","klasse","unterricht","schüler","lernen","studieren","universität",
         "hausaufgabe","prüfung","test","deutsch","mathematik","biologie","physik",
         "chemie","abitur","studium","bildung","stundenplan","direktor","sekretariat",
         "klassenfahrt","latein","kunst","religion","sozialkunde","geografie",
         "geschichte","fremdsprache","vokabel","grammatik","wörterbuch","übung"],
    6:  ["reise","fahren","fliegen","zug","bus","auto","flugzeug","bahnhof",
         "flughafen","ticket","fahrkarte","hotel","koffer","abfahrt","ankunft",
         "anschluss","gleis","taxi","u-bahn","fahrrad","schiff","ausland","ausflug",
         "gepäck","abfahren","ankommen","bahn","fähre","hafen","reisebüro",
         "unterkunft","pension","campingplatz","mietwagen","autobahn","stau"],
    7:  ["gesundheit","krank","arzt","krankenhaus","medikament","apotheke","schmerz",
         "fieber","körper","kopf","arm","bein","auge","ohr","nase","mund","zahn",
         "rücken","bauch","herz","blut","verletzt","unfall","notfall","weh",
         "erkältung","husten","grippe","allergie","operation","rezept","tablette",
         "pflaster","fieber","temperatur","müde","erschöpft"],
    8:  ["freizeit","film","kino","musik","konzert","theater","buch","lesen",
         "spielen","party","tanzen","singen","hobby","fernsehen","spiel","camping",
         "festival","ausgehen","veranstaltung","programm","klavier","gitarre",
         "spaß","witzig","unterhaltung","museum","ausstellung","comic","zeichnen",
         "basteln","fotografieren","blog","serie","tatort","sendung"],
    9:  ["sport","fußball","schwimmen","laufen","radfahren","fitness","training",
         "mannschaft","turnen","tennis","ski","wandern","joggen","stadion",
         "schwimmbad","sportplatz","schiedsrichter","tor","treffer","spieler"],
    10: ["kaufen","einkaufen","zahlen","kosten","preis","geld","euro","bank","kasse",
         "rechnung","angebot","rabatt","geschäft","supermarkt","markt","laden",
         "kreditkarte","wechselgeld","quittung","ausgabe","cent","frank","rappen",
         "bar","münze","schein","haushaltsgeld","sparen","schulden",
         "kredit","konto","überweisung","girokonto","sparkasse"],
    11: ["telefon","handy","anrufen","nachricht","sms","email","internet","computer",
         "app","schreiben","brief","post","anrufbeantworter","drucker","wifi","pc",
         "laptop","bildschirm","tastatur","netzwerk","passwort","nutzername",
         "social","chatten","video","foto","kamera","speicher","cloud","lkw"],
    12: ["natur","wetter","regen","sonne","schnee","wind","baum","blume","wald",
         "berg","see","meer","strand","tier","hund","katze","vogel","pferd",
         "temperatur","grad","wolke","sturm","gewitter","eis","frost","hitze",
         "landschaft","fluss","wiese","feld","acker","umwelt","jahreszeit"],
    13: ["uhr","heute","morgen","gestern","monat","jahr","woche","datum","kalender",
         "januar","februar","märz","april","mai","juni","juli","august","september",
         "oktober","november","dezember","frühling","sommer","herbst","winter",
         "feiertag","geburtstag","weihnachten","ostern","silvester","neujahr",
         "minute","stunde","sekunde","tageszeit","morgens","abends","täglich",
         "wochentag","montag","dienstag","mittwoch","donnerstag","freitag","samstag",
         "sonntag","karneval","datum","jahrestag"],
    14: ["gefühl","glück","traurig","freude","angst","liebe","ärgern","zufrieden",
         "stolz","nervös","überrascht","enttäuscht","nett","freundlich","höflich",
         "fleißig","faul","lustig","ernst","ruhig","böse","fröhlich","sympathisch",
         "ehrlich","mutig","schüchtern","neugierig","geduldig","selbstbewusst",
         "aufgeregt","überglücklich","dankbar","eifersüchtig","wütend","einsam"],
    15: ["stadt","straße","platz","gebäude","rathaus","kirche","museum","park",
         "brücke","kreuzung","ampel","rechts","links","geradeaus","norden","süden",
         "osten","westen","adresse","ausgang","eingang","richtung","postleitzahl",
         "stadtviertel","viertel","bezirk","hauptstadt","dorf","gemeinde",
         "tankstelle","bushaltestelle","haltestelle","fußgänger",
         "zebrastreifen","unterführung","orientierung"],
}

# ── PAGE HEADERS TO SKIP ──────────────────────────────────────────────────────
SKIP_RE = re.compile(
    r'^(WORTLISTE|GOETHE-ZERTIFIKAT|A2_Wortliste_|ALPHABETISCHER|WORTGRUPPEN|'
    r'Abk.rzungen|Familienmitglieder|Anweisungssprache|Himmelsrichtungen|'
    r'Familienstand|Farben|L.nder|Nationalit.ten|Schule|Schulf.cher|Zeitangaben|'
    r'Feiertage|Monate|Jahreszeiten|W.hrungen|Ma.e|Tageszeiten|Uhrzeit|Zahlen|'
    r'Wochentage|zur Pr.fung|Berufe).*$',
    re.I,
)
SECTION_HEADER_RE = re.compile(r'^[A-ZÄÖÜ]\s*$')

# ── CONJUGATION-ONLY LINE ─────────────────────────────────────────────────────
# matches lines that are ONLY conjugation info, no sentence text
CONJ_ONLY_RE = re.compile(
    r'^(hat|ist|wird|war|haben|sind)\s+\w[\w\-äöüÄÖÜß]*\s*$'
    r'|^\w[\w\-äöüß]*\s+(ab|auf|an|aus|bei|ein|mit|nach|vor|zu|hin|her|weg|los|weiter)\s*,?\s*$',
    re.I,
)

# Conjugation prefix followed by a sentence, e.g. "hat abgeholt Wir müssen noch …"
CONJ_PREFIX_RE = re.compile(
    r'^((?:hat|ist|hat sich|ist sich)\s+\w[\w\-äöüÄÖÜß]*)\s+([A-ZÄÖÜ].+)$'
)

# ── SENTENCE STARTERS ─────────────────────────────────────────────────────────
SENT_STARTERS = {
    "ich","wir","er","sie","es","du","ihr","man",
    "was","wo","wie","wann","warum","wer",
    "bitte","danke","entschuldigung",
    "hast","haben","habt","hatte","hatten",
    "ist","sind","war","waren","wird","werden",
    "kann","können","muss","müssen","soll","sollen",
    "darf","dürfen","möchte","möchten","mag",
    "fahren","gehen","kommen","machen","packen","rufen",
    "leider","natürlich","schon","noch","nicht","immer",
    "hier","da","dort","seit","vor","ab","nach","bei",
    "ja","nein","oh","ach","hallo","tschüss","guten","auf","beim",
    "schau","sieh","hör","pass","bleib","ruh","fang","steh",
    "damit","obwohl","weil","dass","wenn","ob","als",
    "alle","alles","mein","meine","dein","deine","sein","seine",
    "unser","euer","ihr","ihre","kein","keine",
    "heute","morgen","gestern","jetzt","dann","dort",
    "zahlen","vielen","herzlichen","willkommen",
}

def is_conj_only(line):
    return bool(CONJ_ONLY_RE.match(line.strip()))

def is_page_header(line):
    s = line.strip()
    return bool(SKIP_RE.match(s)) or bool(SECTION_HEADER_RE.match(s))

def looks_like_sentence(line):
    s = line.strip()
    if not s:
        return False
    first = s.split()[0].rstrip(".,!?").lower()
    return first in SENT_STARTERS

# ── VOCAB ENTRY PATTERNS ──────────────────────────────────────────────────────
ARTICLE_NOUN_RE = re.compile(
    r'^(der|die|das)\s+([A-ZÄÖÜ][a-zäöüß\-]+(?:\s+[a-zäöüß]+)?(?:,\s*[^\s,A-Z][^,\n]*?)?)\s+(.*)',
    re.S,
)
LOWER_WORD_RE = re.compile(
    r'^([a-zäöüß][a-zäöüß\-]*(?:\s+\(sich\))?(?:,\s*[a-z][^,\n]*?)*?)\s+([A-Z].*)',
    re.S,
)
LOWER_ONLY_RE = re.compile(
    r'^([a-zäöüß][a-zäöüß\-]*(?:\s+\(sich\))?(?:,\s*[a-z][^,\n]*?)*)\s*$'
)
CAP_NOUN_RE = re.compile(
    r'^([A-ZÄÖÜ][a-zäöüß\-]+(?:\s+\([^)]+\))?(?:,\s*[^\s,A-Z][^,\n]*?)?)\s+(.*)',
    re.S,
)

def try_parse_entry(line):
    """
    Try to parse line as a new vocab entry start.
    Returns (lemma, grammar_info, sentence_text) or None.
    """
    s = line.strip()
    if not s or looks_like_sentence(s):
        return None

    # Article + Noun
    m = ARTICLE_NOUN_RE.match(s)
    if m:
        article = m.group(1)
        noun_part = m.group(2).strip()
        rest = m.group(3).strip()
        lemma = article + " " + noun_part.split(",")[0].strip()
        grammar = article + " " + noun_part
        return (lemma, grammar, rest)

    # Lowercase word (possibly with conjugation info on same line)
    m = LOWER_WORD_RE.match(s)
    if m:
        grammar = m.group(1).strip()
        rest = m.group(2).strip()
        lemma = grammar.split(",")[0].strip()
        first_w = lemma.split()[0].lower()
        if first_w not in SENT_STARTERS:
            return (lemma, grammar, rest)

    # Lowercase word only (no sentence on this line)
    m = LOWER_ONLY_RE.match(s)
    if m:
        grammar = m.group(1).strip()
        lemma = grammar.split(",")[0].strip()
        first_w = lemma.split()[0].lower()
        if first_w not in SENT_STARTERS and len(lemma) <= 30:
            return (lemma, grammar, "")

    # Capitalised noun without article (Achtung, Anfang, etc.)
    m = CAP_NOUN_RE.match(s)
    if m:
        noun_part = m.group(1).strip()
        rest = m.group(2).strip()
        lemma = noun_part.split(",")[0].split("(")[0].strip()
        first_w = lemma.split()[0].lower()
        if (first_w not in SENT_STARTERS
                and len(lemma) <= 35
                and not re.search(r"[.!?]$", noun_part)):
            return (lemma, noun_part, rest)

    return None


# ── READ & CLEAN TXT ──────────────────────────────────────────────────────────
def read_clean_lines(path):
    lines = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            cleaned = re.sub(r"^\s*\d+\u2192", "", line).strip()
            if cleaned:
                lines.append(cleaned)
    return lines


def find_alpha_start(lines):
    for i, l in enumerate(lines):
        if re.match(r"^ALPHABETISCHER WORTSCHATZ", l, re.I):
            return i + 1
    return 0


# ── PARSE ALPHABETICAL VOCAB ──────────────────────────────────────────────────
def _add_sentence(entry, text):
    text = text.strip()
    if not text:
        return
    if entry["sentences"]:
        last = entry["sentences"][-1]
        if last and not re.search(r"[.!?]$", last):
            entry["sentences"][-1] = last + " " + text
            return
    entry["sentences"].append(text)


def parse_entries(lines):
    entries = []
    current = None

    def flush():
        if current:
            current["sentences"] = [s for s in current["sentences"] if s.strip()]
            entries.append(current)

    for line in lines:
        if is_page_header(line):
            continue

        # Conjugation-only line → merge into current entry grammar
        if is_conj_only(line):
            if current is not None:
                current["grammar"] = (current["grammar"] + ", " + line.rstrip(",").strip()).strip(", ")
            continue

        # Conjugation prefix + sentence on same line
        cp = CONJ_PREFIX_RE.match(line)
        if cp and current is not None:
            conj = cp.group(1).strip()
            sentence = cp.group(2).strip()
            current["grammar"] = (current["grammar"] + ", " + conj).strip(", ")
            if sentence:
                _add_sentence(current, sentence)
            continue

        result = try_parse_entry(line)
        if result:
            flush()
            lemma, grammar, sentence_text = result
            current = {"word": lemma, "grammar": grammar, "sentences": []}
            if sentence_text.strip():
                current["sentences"].append(sentence_text.strip())
        else:
            if current is not None:
                _add_sentence(current, line)

    flush()
    return entries


# ── PARSE WORTGRUPPEN ─────────────────────────────────────────────────────────
WORTGRUPPEN_TOPIC_MAP = {
    "familienmitglieder": 1, "familienstand": 1,
    "berufe": 4,
    "farben": None,
    "himmelsrichtungen": 15,
    "länder": 6, "nationalitäten": 6,
    "schule": 5, "schulfächer": 5,
    "zeitangaben": 13, "feiertage": 13, "monate": 13,
    "jahreszeiten": 12, "tageszeiten": 13,
    "uhrzeit": 13, "zahlen": 13, "wochentage": 13,
    "abkürzungen": None,
    "währungen": 10, "maße": None,
}


def parse_wortgruppen(lines):
    entries = []
    alpha_start = find_alpha_start(lines)
    current_group_topic = None

    for line in lines[:alpha_start]:
        ls = line.strip().lower()
        for key, tid in WORTGRUPPEN_TOPIC_MAP.items():
            if key in ls and len(ls) < 40:
                current_group_topic = tid
                break

        if is_page_header(line):
            continue
        if looks_like_sentence(line):
            continue
        if re.match(r"^\d", line):
            continue
        if "=" in line:
            continue

        word = line.strip().rstrip(",").strip()
        if word and len(word.split()) <= 5 and not re.search(r"[.!?]$", word):
            parts = [p.strip() for p in re.split(r",\s*(?=[A-ZÄÖÜ])", word) if p.strip()]
            for part in parts:
                if re.match(r"^[A-ZÄÖÜ][a-z]+_", part):
                    continue
                entries.append({
                    "word": part.split(",")[0].strip(),
                    "grammar": part,
                    "sentences": [],
                    "_wg_topic": current_group_topic,
                })
    return entries


# ── TOPIC ASSIGNMENT ──────────────────────────────────────────────────────────
def assign_topics(word, sentences, wg_topic=None):
    text = (word + " " + " ".join(sentences)).lower()
    scores = {}
    for tid, kws in TOPIC_KW.items():
        score = sum(1 for kw in kws if kw in text)
        if score > 0:
            scores[tid] = score

    if wg_topic is not None:
        scores[wg_topic] = scores.get(wg_topic, 0) + 2  # boost word-group hint

    if not scores:
        return [1]

    max_score = max(scores.values())
    threshold = max(1, max_score * 0.6)
    result = sorted(k for k, v in scores.items() if v >= threshold)
    return result or [1]




# ── DEDUPLICATE ───────────────────────────────────────────────────────────────
def deduplicate(entries):
    seen = {}
    for e in entries:
        key = e["word"].lower()
        if key in seen:
            for s in e["sentences"]:
                if s not in seen[key]["sentences"]:
                    seen[key]["sentences"].append(s)
        else:
            seen[key] = e
    return list(seen.values())


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    print(f"Reading {TXT_FILE} …")
    lines = read_clean_lines(TXT_FILE)
    print(f"  {len(lines)} non-empty lines")

    alpha_start = find_alpha_start(lines)
    print(f"  Alphabetical section starts at line index {alpha_start}")

    print("Parsing Wortgruppen section …")
    wg_entries = parse_wortgruppen(lines)
    print(f"  {len(wg_entries)} word-group entries")

    print("Parsing alphabetical vocabulary …")
    alpha_entries = parse_entries(lines[alpha_start:])
    print(f"  {len(alpha_entries)} alphabetical entries")

    all_entries = wg_entries + alpha_entries
    all_entries = deduplicate(all_entries)
    print(f"  {len(all_entries)} entries after deduplication")

    print("Assigning topics …")
    for e in all_entries:
        e["topic_ids"] = assign_topics(e["word"], e["sentences"], e.get("_wg_topic"))

    # Assemble output
    vocab_out = []
    sentence_out = []
    sent_id = 1

    for ei, e in enumerate(all_entries):
        entry_sent_ids = []
        for si, s in enumerate(e["sentences"]):
            sentence_out.append({
                "id": sent_id,
                "text_de": s,
                "text_ru": None,
                "topic_ids": e["topic_ids"],
            })
            entry_sent_ids.append(sent_id)
            sent_id += 1

        vocab_out.append({
            "id": ei + 1,
            "word_de": e["word"],
            "grammar": e["grammar"],
            "word_ru": None,
            "topic_ids": e["topic_ids"],
            "sentence_ids": entry_sent_ids,
        })

    from collections import Counter
    import datetime
    topic_counts = Counter()
    for v in vocab_out:
        for tid in v["topic_ids"]:
            topic_counts[tid] += 1

    output = {
        "metadata": {
            "source": TXT_FILE,
            "total_vocab": len(vocab_out),
            "total_sentences": len(sentence_out),
            "topics_count": len(TOPICS),
            "generated": datetime.date.today().isoformat(),
        },
        "topics": TOPICS,
        "vocabulary": vocab_out,
        "sentences": sentence_out,
    }

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nWrote {OUT_FILE}")
    print(f"  {len(vocab_out)} vocabulary items")
    print(f"  {len(sentence_out)} sentences")
    print(f"\nTopic distribution (vocab mentions):")
    for t in TOPICS:
        print(f"  [{t['id']:2d}] {t['name_de']:<30s} {topic_counts[t['id']]:4d}")


if __name__ == "__main__":
    main()
