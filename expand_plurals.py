#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Expand German noun plural notations in mistral-markdown-clean.md."""

import re

INPUT = 'mistral-markdown-clean.md'
OUTPUT = 'mistral-markdown-clean-v2.md'

# Lookup table: (base_noun, suffix) → correct plural (no article)
# Only needed where mechanical suffix application would give wrong form (umlaut cases)
PLURAL_OVERRIDES = {
    # -e suffix WITH umlaut
    ("Anfang", "-e"): "Anfänge",
    ("Angst", "-e"): "Ängste",
    ("Ankunft", "-e"): "Ankünfte",
    ("Anschluss", "-e"): "Anschlüsse",
    ("Anzug", "-e"): "Anzüge",
    ("Aufzug", "-e"): "Aufzüge",
    ("Ausflug", "-e"): "Ausflüge",
    ("Ausgang", "-e"): "Ausgänge",
    ("Auskunft", "-e"): "Auskünfte",
    ("Bahnhof", "-e"): "Bahnhöfe",
    ("Ball", "-e"): "Bälle",
    ("Bank", "-e"): "Bänke",         # die Bank (bench); Bank -en stays mechanical
    ("Basketball", "-e"): "Basketbälle",
    ("Bauch", "-e"): "Bäuche",
    ("Baum", "-e"): "Bäume",
    ("Eingang", "-e"): "Eingänge",
    ("Flug", "-e"): "Flüge",
    ("Fluss", "-e"): "Flüsse",
    ("Fuß", "-e"): "Füße",
    ("Fußball", "-e"): "Fußbälle",
    ("Kopf", "-e"): "Köpfe",
    ("Markt", "-e"): "Märkte",
    ("Nacht", "-e"): "Nächte",
    ("Plan", "-e"): "Pläne",
    ("Platz", "-e"): "Plätze",
    ("Raum", "-e"): "Räume",
    ("Rock", "-e"): "Röcke",
    ("Rucksack", "-e"): "Rucksäcke",
    ("Rundgang", "-e"): "Rundgänge",
    ("Saft", "-e"): "Säfte",
    ("Satz", "-e"): "Sätze",
    ("Schluss", "-e"): "Schlüsse",
    ("Schrank", "-e"): "Schränke",
    ("Spaziergang", "-e"): "Spaziergänge",
    ("Sportplatz", "-e"): "Sportplätze",
    ("Stadt", "-e"): "Städte",
    ("Stadtplan", "-e"): "Stadtpläne",
    ("Strand", "-e"): "Strände",
    ("Stuhl", "-e"): "Stühle",
    ("Supermarkt", "-e"): "Supermärkte",
    ("Topf", "-e"): "Töpfe",
    ("Traum", "-e"): "Träume",
    ("Umzug", "-e"): "Umzüge",
    ("Unfall", "-e"): "Unfälle",
    ("Unterkunft", "-e"): "Unterkünfte",
    ("Vertrag", "-e"): "Verträge",
    ("Volleyball", "-e"): "Volleybälle",
    ("Vorschlag", "-e"): "Vorschläge",
    ("Wunsch", "-e"): "Wünsche",
    ("Wurst", "-e"): "Würste",
    ("Zahn", "-e"): "Zähne",
    ("Zug", "-e"): "Züge",
    ("Stock", "-e"): "Stöcke",
    # -er suffix WITH umlaut
    ("Bad", "-er"): "Bäder",
    ("Blatt", "-er"): "Blätter",
    ("Buch", "-er"): "Bücher",
    ("Dorf", "-er"): "Dörfer",
    ("Fach", "-er"): "Fächer",
    ("Glas", "-er"): "Gläser",
    ("Haus", "-er"): "Häuser",
    ("Krankenhaus", "-er"): "Krankenhäuser",
    ("Land", "-er"): "Länder",
    ("Passwort", "-er"): "Passwörter",
    ("Rathaus", "-er"): "Rathäuser",
    ("Schloss", "-er"): "Schlösser",
    ("Schwimmbad", "-er"): "Schwimmbäder",
    ("Wald", "-er"): "Wälder",
    ("Wort", "-er"): "Wörter",
    ("Wörterbuch", "-er"): "Wörterbücher",
    ("Ehemann", "-er"): "Ehemänner",
    # -¨ (umlaut only, no added suffix)
    ("Apfel", "-¨"): "Äpfel",
    ("Garten", "-¨"): "Gärten",
    ("Kindergarten", "-¨"): "Kindergärten",
    ("Laden", "-¨"): "Läden",
    ("Magen", "-¨"): "Mägen",
    ("Mantel", "-¨"): "Mäntel",
    ("Vogel", "-¨"): "Vögel",
    # Nouns where suffix isn't just appended (stem change)
    ("Pizza", "-en"): "Pizzen",
}


def apply_suffix(base, suffix):
    """Apply a plural suffix to a base noun, using lookup table first."""
    key = (base, suffix)
    if key in PLURAL_OVERRIDES:
        return PLURAL_OVERRIDES[key]

    # Mechanical rule
    if suffix == '-':
        return base
    elif suffix == '-¨':
        return apply_umlaut(base)
    elif suffix.startswith('-'):
        ending = suffix[1:]
        if ending.startswith('¨'):
            return apply_umlaut(base) + ending[1:]
        else:
            return base + ending
    return base


def apply_umlaut(word):
    """Apply umlaut to the last a, o, u, or au in a word."""
    for i in range(len(word) - 1, 0, -1):
        pair = word[i-1:i+1]
        if pair == 'au':
            return word[:i-1] + 'äu' + word[i+1:]
        if pair == 'Au':
            return word[:i-1] + 'Äu' + word[i+1:]
    for i in range(len(word) - 1, -1, -1):
        if word[i] in 'aouAOU':
            rep = {'a': 'ä', 'o': 'ö', 'u': 'ü', 'A': 'Ä', 'O': 'Ö', 'U': 'Ü'}
            return word[:i] + rep[word[i]] + word[i+1:]
    return word


def expand_noun_line(line):
    """
    Expand plural suffix notation on a line.
    Only processes segments that have an article (der/die/das) + Noun + , -suffix.
    Article-less entries (WORTGRUPPEN) are left unchanged.
    """
    if ', -' not in line:
        return line

    # We process each article+noun+suffix segment individually
    # Pattern: (der |die |das )CapitalNoun, -suffix
    pattern = re.compile(
        r'(der |die |das )'                          # article (required)
        r'([A-ZÄÖÜ][a-zA-ZäöüÄÖÜß\-]*(?:\s[A-ZÄÖÜ][a-zA-ZäöüÄÖÜß\-]*)?)'  # noun (1-2 words)
        r',\s*'
        r'(-[¨a-zA-ZäöüÄÖÜß]*)'                    # suffix like -n, -er, -¨, -s
        r'(\s*/\s*-[a-zA-ZäöüÄÖÜß]+)?'             # optional second suffix like / -n or /-n
    )

    def replace_match(m):
        article = m.group(1)   # "der ", "die ", "das "
        noun = m.group(2)      # e.g. "Adresse"
        suffix1 = m.group(3)   # e.g. "-n"
        suffix2_raw = m.group(4)  # e.g. " / -n" or None

        # Skip (Sg.) or similar markers
        if 'Sg.' in noun or 'Pl.' in noun:
            return m.group(0)

        # Handle multiple suffixes (e.g. "-s / -n")
        if suffix2_raw:
            s2 = re.sub(r'^\s*/\s*', '', suffix2_raw).strip()
            pl1 = apply_suffix(noun.strip(), suffix1)
            pl2 = apply_suffix(noun.strip(), s2)
            return f"{article}{noun}, die {pl1} / die {pl2}"

        plural = apply_suffix(noun.strip(), suffix1)
        return f"{article}{noun}, die {plural}"

    result = pattern.sub(replace_match, line)

    # Clean up any leftover orphaned "/ -suffix" after a fully-expanded entry
    # e.g. "der Ski, die Ski / -er" → "der Ski, die Ski / die Skier"
    def fix_orphan(m):
        # m.group(1) is the already-expanded "die PLURAL" part, m.group(2) is "/ -suffix"
        # We need the base noun from the expanded plural — too complex; just tidy the suffix text
        suffix = m.group(2).strip()
        # Can't expand without the noun; just remove the notation
        return m.group(1)

    result = re.sub(r'(die \w+)\s*/\s*(-[\w¨]+)', fix_orphan, result)

    return result


def process_file():
    with open(INPUT, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []
    for line in lines:
        stripped = line.rstrip('\n')
        expanded = expand_noun_line(stripped)
        output_lines.append(expanded + '\n')

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)

    print(f"Done. Written to {OUTPUT}")


if __name__ == '__main__':
    process_file()
