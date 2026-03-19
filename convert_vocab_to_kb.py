#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert vocabulary.json to data/knowledge-base.js format."""

import json, re

INPUT  = 'vocabulary.json'
OUTPUT = 'data/knowledge-base.js'

TOPICS = [
    {"id": 1,  "name_de": "Familie & Beziehungen",    "name_ru": "\u0441\u0435\u043c\u044c\u044f \u0438 \u043e\u0442\u043d\u043e\u0448\u0435\u043d\u0438\u044f"},
    {"id": 2,  "name_de": "Essen & Trinken",           "name_ru": "\u0435\u0434\u0430 \u0438 \u043d\u0430\u043f\u0438\u0442\u043a\u0438"},
    {"id": 3,  "name_de": "Wohnen & Einrichten",       "name_ru": "\u0436\u0438\u043b\u044c\u0451 \u0438 \u043e\u0431\u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u043e"},
    {"id": 4,  "name_de": "Arbeit & Beruf",            "name_ru": "\u0440\u0430\u0431\u043e\u0442\u0430 \u0438 \u043f\u0440\u043e\u0444\u0435\u0441\u0441\u0438\u044f"},
    {"id": 5,  "name_de": "Schule & Bildung",          "name_ru": "\u0448\u043a\u043e\u043b\u0430 \u0438 \u043e\u0431\u0440\u0430\u0437\u043e\u0432\u0430\u043d\u0438\u0435"},
    {"id": 6,  "name_de": "Reise & Transport",         "name_ru": "\u043f\u0443\u0442\u0435\u0448\u0435\u0441\u0442\u0432\u0438\u044f \u0438 \u0442\u0440\u0430\u043d\u0441\u043f\u043e\u0440\u0442"},
    {"id": 7,  "name_de": "Gesundheit & K\u00f6rper",  "name_ru": "\u0437\u0434\u043e\u0440\u043e\u0432\u044c\u0435 \u0438 \u0442\u0435\u043b\u043e"},
    {"id": 8,  "name_de": "Freizeit & Unterhaltung",   "name_ru": "\u0434\u043e\u0441\u0443\u0433 \u0438 \u0440\u0430\u0437\u0432\u043b\u0435\u0447\u0435\u043d\u0438\u044f"},
    {"id": 9,  "name_de": "Sport & Bewegung",          "name_ru": "\u0441\u043f\u043e\u0440\u0442 \u0438 \u0430\u043a\u0442\u0438\u0432\u043d\u043e\u0441\u0442\u044c"},
    {"id": 10, "name_de": "Einkaufen & Geld",          "name_ru": "\u043f\u043e\u043a\u0443\u043f\u043a\u0438 \u0438 \u0434\u0435\u043d\u044c\u0433\u0438"},
    {"id": 11, "name_de": "Kommunikation & Technik",   "name_ru": "\u043e\u0431\u0449\u0435\u043d\u0438\u0435 \u0438 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438"},
    {"id": 12, "name_de": "Natur & Wetter",            "name_ru": "\u043f\u0440\u0438\u0440\u043e\u0434\u0430 \u0438 \u043f\u043e\u0433\u043e\u0434\u0430"},
    {"id": 13, "name_de": "Zeit & Kalender",           "name_ru": "\u0432\u0440\u0435\u043c\u044f \u0438 \u043a\u0430\u043b\u0435\u043d\u0434\u0430\u0440\u044c"},
    {"id": 14, "name_de": "Gef\u00fchle & Charakter",  "name_ru": "\u0447\u0443\u0432\u0441\u0442\u0432\u0430 \u0438 \u0445\u0430\u0440\u0430\u043a\u0442\u0435\u0440"},
    {"id": 15, "name_de": "Stadt & Orientierung",      "name_ru": "\u0433\u043e\u0440\u043e\u0434 \u0438 \u043e\u0440\u0438\u0435\u043d\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435"},
]


def make_german(w):
    """Build the German display word (what shows in the question)."""
    word    = w['word']
    article = w.get('article')
    if article:
        return article + ' ' + word
    return word


def make_grammar(w):
    """Build the grammar hint string."""
    word    = w['word']
    article = w.get('article')
    plural  = w.get('plural')
    forms   = w.get('forms') or []

    if article and plural:
        return article + ' ' + word + ', die ' + plural
    if article and not plural:
        return article + ' ' + word
    if forms:
        return ', '.join(forms)
    return None


def convert():
    with open(INPUT, encoding='utf-8') as f:
        data = json.load(f)

    vocab_out = []
    for w in data['words']:
        german  = make_german(w)
        grammar = make_grammar(w)
        entry = {
            "id":                 w['id'],
            "topic_ids":          [],
            "german":             german,
            "grammar":            grammar,
            "russian":            w.get('translation_ru') or '',
            "alternates_german":  [],
            "alternates_russian": [],
        }
        vocab_out.append(entry)

    kb = {
        "topics":     TOPICS,
        "vocabulary": vocab_out,
        "sentences":  [],
    }

    js_content = 'var KB_DATA = ' + json.dumps(kb, ensure_ascii=False, indent=2) + ';\n'

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f'Done. {len(vocab_out)} vocabulary entries written to {OUTPUT}')


if __name__ == '__main__':
    convert()
