"""
convert_data.py — Convert vocabulary.json → data/knowledge-base.js
Run once to (re-)generate the knowledge base whenever vocabulary.json changes.
"""
import json
import os

src = os.path.join(os.path.dirname(__file__), 'vocabulary.json')
dst = os.path.join(os.path.dirname(__file__), 'data', 'knowledge-base.js')

with open(src, 'r', encoding='utf-8') as f:
    data = json.load(f)

# ── Topics ────────────────────────────────────────────────────────────────────
converted_topics = []
for t in data['topics']:
    converted_topics.append({
        'id': t['id'],
        'name_de': t['name_de'],
        'name_ru': t.get('name_ru', t.get('name_en', ''))
    })

# ── Vocabulary ────────────────────────────────────────────────────────────────
converted_vocab = []
for v in data['vocabulary']:
    word_ru = v.get('word_ru', '')
    if word_ru:
        word_ru = word_ru.lower()   # Russian nouns are not capitalised
    converted_vocab.append({
        'id': 'v' + str(v['id']),
        'topic_ids': v.get('topic_ids', []),
        'german': v.get('word_de', ''),
        'grammar': v.get('grammar', ''),
        'russian': word_ru,
        'alternates_german': [],
        'alternates_russian': []
    })

# ── Sentences ─────────────────────────────────────────────────────────────────
converted_sents = []
for s in data['sentences']:
    converted_sents.append({
        'id': 's' + str(s['id']),
        'topic_ids': s.get('topic_ids', []),
        'german': s.get('text_de', ''),
        'russian': s.get('text_ru', '')
    })

# ── Write JS ──────────────────────────────────────────────────────────────────
output = {
    'topics': converted_topics,
    'vocabulary': converted_vocab,
    'sentences': converted_sents
}

json_str = json.dumps(output, ensure_ascii=False, indent=2)
js_content = 'var KB_DATA = ' + json_str + ';\n'

os.makedirs(os.path.dirname(dst), exist_ok=True)
with open(dst, 'w', encoding='utf-8') as f:
    f.write(js_content)

print('Topics:    ', len(converted_topics))
print('Vocab:     ', len(converted_vocab))
print('Sentences: ', len(converted_sents))
print('Written -> ', dst)
