import json

VOCAB_PATH = 'C:/Users/micha/OneDrive/Root/Code/learn-german/vocabulary.json'

# Step 1: IDs to delete
DELETE_IDS = {
    20, 24, 28, 34, 53, 77,
    100, 114, 118, 120, 127, 129, 142, 143, 144, 146, 150, 167, 170, 185, 187, 192, 197, 224, 234, 239, 244, 249, 257, 260, 261, 263, 279, 287, 288, 292, 293, 296, 298, 299, 305, 307, 310, 315, 317, 318, 329, 338, 351, 365, 370, 379, 388, 389, 390, 396, 401, 412, 420, 426, 431, 432, 436, 438, 456, 460, 461, 468, 476, 482, 486, 494, 498, 509, 512, 513, 531, 533, 535, 539, 540, 543, 544, 552, 558, 560, 566, 569, 573, 598, 599, 600, 601, 605, 606, 607, 611, 617, 618, 619, 630, 636, 639, 640, 654, 670, 676, 677, 678, 679, 680, 681, 702, 707, 713, 717, 721, 731, 737, 739, 752, 758, 765, 773, 775, 781, 789, 800, 803, 805, 807, 811, 815, 820, 824, 827, 833, 838, 850, 893, 927, 978, 991,
}

# Step 2: Fix both word_de and grammar
# Values: (new_word_de, new_grammar)
WORD_FIXES = {
    38: ('rosa', 'rosa'),
    40: ('schwarz', 'schwarz'),
    41: ('weiß', 'weiß'),
    44: ('Deutschland', 'Deutschland'),
    46: ('deutsch', 'deutsch'),
    47: ('Österreich', 'Österreich'),
    48: ('österreichisch', 'österreichisch'),
    49: ('die Schweiz', 'die Schweiz'),
    50: ('schweizerisch', 'schweizerisch'),
    51: ('Luxemburg', 'Luxemburg'),
    54: ('luxemburgisch', 'luxemburgisch'),
    55: ('Europa', 'Europa'),
    57: ('europäisch', 'europäisch'),
    64: ('Karneval', 'Karneval, -e'),
    65: ('Ostern', 'Ostern (Pl.)'),
    66: ('Weihnachten', 'Weihnachten (Pl.)'),
    67: ('Neujahr/Silvester', 'Neujahr/Silvester'),
    70: ('Frühling', 'Frühling, -e'),
    71: ('Sommer', 'Sommer, -'),
    72: ('Herbst', 'Herbst, -e'),
    73: ('Winter', 'Winter, -'),
}

# Step 3: Fix grammar only
GRAMMAR_FIXES = {
    18: 'Onkel, -',
    19: 'Schwester, -n',
    23: 'Tochter, ¨-',
    26: 'Antwortbogen, ¨-',
    27: 'Angestellter, -e / Angestellte, -n',
    29: 'Beispiel, -e',
    30: 'Lösung, -en',
    33: 'Krankenpfleger, - / Krankenschwester, -n',
    45: 'Deutsche, -n',
    52: 'Luxemburger, - / Luxemburgerin, -nen',
    56: 'Europäer, - / Europäerin, -nen',
    63: 'Datum, Daten',
    75: 'ein Gramm / ein Kilogramm',
    83: 'täglich',
    122: 'die Angst, ¨-e',
    124: 'der Anruf, -e',
    135: 'der Apparat, -e',
    137: 'arbeitslos',
    152: 'der Ausflug, ¨-e',
    153: 'der Ausgang, ¨-e',
    155: 'das Ausland',
    158: 'außerhalb',
    159: 'die Ausstellung, -en',
    181: 'der Basketball, ¨-e',
    182: 'der Bauch, ¨-e',
    184: 'die Baustelle, -n',
    193: 'der Berg, -e',
    199: 'besonders',
    200: 'der Besuch, -e',
    201: 'das Bett, -en',
    203: 'die Wolke, -n',
    220: 'böse',
    229: 'der Buchstabe, -n',
    235: 'die Cafeteria, -s',
    237: 'der Club, -s',
    246: 'der Dank',
    248: 'das Datum, Daten',
    272: 'schwer',
    302: 'das Ende, -n',
    312: 'die Ermäßigung, -en',
    324: 'der Fahrplan, ¨-e',
    327: 'der Familienname, -n',
    333: 'faul',
    335: 'die Feier, -n',
    339: 'der Fernseher, -',
    344: 'der Film, -e',
    353: 'der Flughafen, ¨-',
    357: 'der Fotoapparat, -e',
    359: 'die Frage, -n',
    364: 'fremd',
    373: 'das Frühstück',
    386: 'der Garten, ¨-',
    387: 'der Gast, ¨-e',
    391: 'gefährlich',
    395: 'das Gehalt, ¨-er',
    397: 'zu',
    422: 'das Glas, ¨-er',
    428: 'Glückwunsch, ¨-e',
    440: 'das Hähnchen, -',
    442: 'der Hals, ¨-e',
    454: 'die Heimat',
    457: 'die Heizung, -en',
    463: 'der Herr, -en',
    473: 'die Hochzeit, -en',
    474: 'hoffentlich',
    480: 'der Hunger',
    517: 'die Katze, -n',
    523: 'der Kindergarten, ¨-',
    542: 'das Konto, -s',
    548: 'tun',
    556: 'die Kreuzung, -en',
    562: 'der Schokoladenkuchen, -',
    565: 'die Woche, -n',
    571: 'kurz',
    580: 'langweilig',
    581: 'laut',
    584: 'leer',
    586: 'leise',
    591: 'das Lied, -er',
    603: 'mehr',
    613: 'das Messer, -',
    614: 'die Miete, -n',
    637: 'das Museum, Museen',
    650: 'neblig',
    660: 'die Note, -n',
    671: 'offen',
    689: 'der Plan, ¨-e',
    699: 'das Praktikum, Praktika',
    714: 'der Prospekt, -e',
    723: 'das Rätsel, -',
    724: 'der Raum, ¨-e',
    726: 'rechts',
    727: 'der Regen',
    736: 'der Reiseführer, -',
    738: 'die Reparatur, -en',
    743: 'die Rezeption, -en',
    745: 'das Rind, -er',
    759: 'der Saft, ¨-e',
    761: 'das Salz, -e',
    769: 'scharf',
    770: 'die Schere, -n',
    776: 'das Schlafzimmer, -',
    784: 'der Schnee',
    790: 'schrecklich',
    804: 'die Seife, -n',
    813: 'sicher',
    825: 'spannend',
    844: 'die Stelle, -n',
    849: 'das Stockwerk, -e',
    859: 'der Stuhl, ¨-e',
    861: 'der Supermarkt, ¨-e',
    874: 'der Tee, -s',
    875: 'das Telefon, -e',
    899: 'der Traum, ¨-e',
    900: 'traurig',
    901: 'die Treppe, -n',
    917: 'unter',
    918: 'die Unterkunft, ¨-e',
    920: 'der Unterschied, -e',
    921: 'die Unterschrift, -en',
    924: 'der Verein, -e',
    930: 'die Verspätung, -en',
    933: 'der Vogel, ¨-',
    948: 'der Wald, ¨-er',
    950: 'die Wäsche',
    952: 'die Webseite, -n',
    957: 'der Wein, -e',
    964: 'der Wettbewerb, -e',
    984: 'die Zahl, -en',
    985: 'der Zahn, ¨-e',
    995: 'das Zimmer, -',
    1003: 'der Zug, ¨-e',
    1005: 'zum',
}

# Additional word_de fixes (alongside grammar fixes above)
WORD_DE_FIXES = {
    124: 'der Anruf',
    339: 'Fernseher',
    440: 'Hähnchen',
    562: 'Schokoladenkuchen',
    565: 'Woche',
    613: 'Messer',
    995: 'Zimmer',
}

def main():
    with open(VOCAB_PATH, encoding='utf-8') as f:
        data = json.load(f)

    vocab = data['vocabulary']
    original_count = len(vocab)

    # Step 1: Delete entries
    deleted_ids = set()
    new_vocab = []
    for entry in vocab:
        if entry['id'] in DELETE_IDS:
            deleted_ids.add(entry['id'])
        else:
            new_vocab.append(entry)

    deleted_count = len(deleted_ids)
    missing_deletes = DELETE_IDS - deleted_ids
    if missing_deletes:
        print(f"WARNING: Could not find entries to delete with IDs: {sorted(missing_deletes)}")

    # Build lookup by ID for steps 2 and 3
    entry_by_id = {e['id']: e for e in new_vocab}

    # Step 2: Fix word_de AND grammar
    word_de_fixed_count = 0
    grammar_step2_fixed_count = 0
    for entry_id, (new_word_de, new_grammar) in WORD_FIXES.items():
        if entry_id in entry_by_id:
            entry = entry_by_id[entry_id]
            if entry['word_de'] != new_word_de:
                entry['word_de'] = new_word_de
                word_de_fixed_count += 1
            if entry['grammar'] != new_grammar:
                entry['grammar'] = new_grammar
                grammar_step2_fixed_count += 1
        else:
            print(f"WARNING: WORD_FIXES entry ID {entry_id} not found (may have been deleted or missing)")

    # Step 3: Fix grammar only (and additional word_de fixes)
    grammar_step3_fixed_count = 0
    for entry_id, new_grammar in GRAMMAR_FIXES.items():
        if entry_id in entry_by_id:
            entry = entry_by_id[entry_id]
            if entry['grammar'] != new_grammar:
                entry['grammar'] = new_grammar
                grammar_step3_fixed_count += 1
        else:
            print(f"WARNING: GRAMMAR_FIXES entry ID {entry_id} not found (may have been deleted or missing)")

    # Additional word_de fixes
    extra_word_de_fixed = 0
    for entry_id, new_word_de in WORD_DE_FIXES.items():
        if entry_id in entry_by_id:
            entry = entry_by_id[entry_id]
            if entry['word_de'] != new_word_de:
                entry['word_de'] = new_word_de
                extra_word_de_fixed += 1
        else:
            print(f"WARNING: WORD_DE_FIXES entry ID {entry_id} not found (may have been deleted or missing)")

    total_word_de_fixed = word_de_fixed_count + extra_word_de_fixed
    total_grammar_fixed = grammar_step2_fixed_count + grammar_step3_fixed_count

    # Update vocabulary and metadata
    data['vocabulary'] = new_vocab
    new_total = len(new_vocab)
    if 'metadata' in data:
        data['metadata']['total_vocab'] = new_total

    with open(VOCAB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Entries deleted:   {deleted_count}")
    print(f"word_de fixed:     {total_word_de_fixed}")
    print(f"grammar fixed:     {total_grammar_fixed}")
    print(f"Total remaining:   {new_total}  (was {original_count})")

if __name__ == '__main__':
    main()
