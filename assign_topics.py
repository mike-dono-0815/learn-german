#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assign topic_ids to every word in vocabulary.json."""

import json

# 1=Familie  2=Essen  3=Wohnen  4=Arbeit  5=Schule  6=Reise
# 7=Gesundheit  8=Freizeit  9=Sport  10=Einkaufen  11=Kommunikation
# 12=Natur  13=Zeit  14=Gefühle  15=Stadt

ASSIGNMENTS = {
    "w0003": [5],           # abgeben
    "w0004": [1, 6],        # abholen
    "w0005": [4, 5],        # abschließen
    "w0007": [11, 15],      # Adresse
    "w0009": [9],           # aktiv
    "w0018": [6, 15],       # Ampel
    "w0020": [4, 10],       # anbieten
    "w0021": [10],          # Angebot
    "w0027": [14],          # Angst
    "w0028": [6],           # ankommen
    "w0029": [6],           # Ankunft
    "w0030": [3],           # anmachen
    "w0031": [4, 5],        # anmelden
    "w0032": [4, 5],        # Anmeldung
    "w0033": [11],          # Anrufbeantworter
    "w0034": [11],          # anrufen
    "w0035": [11],          # Anruf
    "w0036": [6, 11],       # Anschluss
    "w0037": [8],           # ansehen
    "w0038": [5],           # antworten
    "w0039": [5],           # Antwort
    "w0040": [4, 10],       # Anzeige
    "w0041": [10],          # Anzug
    "w0042": [2],           # Apfel
    "w0043": [7, 15],       # Apotheke
    "w0044": [11],          # Apparat
    "w0045": [4],           # arbeiten
    "w0046": [4],           # Arbeit
    "w0047": [4],           # arbeitslos
    "w0048": [14],          # ärgern
    "w0050": [7],           # Arm
    "w0051": [5],           # Artikel
    "w0058": [3],           # aufräumen
    "w0059": [14],          # aufregend
    "w0061": [3, 15],       # Aufzug
    "w0062": [7],           # Auge
    "w0064": [4, 5],        # Ausbildung
    "w0065": [6, 8],        # Ausflug
    "w0066": [4],           # ausfüllen
    "w0067": [15],          # Ausgang
    "w0068": [10],          # ausgeben
    "w0069": [8],           # ausgehen
    "w0070": [11, 15],      # Auskunft
    "w0071": [6],           # Ausland
    "w0072": [3],           # ausmachen
    "w0073": [6],           # auspacken
    "w0074": [7, 8],        # ausruhen
    "w0078": [15],          # außerhalb
    "w0079": [5],           # aussprechen
    "w0080": [6],           # aussteigen
    "w0081": [8, 15],       # Ausstellung
    "w0084": [6],           # Auto
    "w0085": [6],           # Autobahn
    "w0086": [6, 10],       # Automat
    "w0087": [11],          # automatisch
    "w0088": [1],           # Baby
    "w0089": [1],           # Babysitter
    "w0090": [2],           # backen
    "w0091": [2, 15],       # Bäckerei
    "w0092": [3],           # Bad
    "w0093": [9],           # baden
    "w0094": [6],           # Bahn
    "w0095": [6, 15],       # Bahnhof
    "w0096": [6],           # Bahnsteig
    "w0097": [13],          # bald
    "w0098": [3],           # Balkon
    "w0099": [9],           # Ball
    "w0100": [2],           # Banane
    "w0101": [8],           # Band
    "w0102": [10, 15],      # Bank (Banken - financial)
    "w0103": [15],          # Bank (Bänke - bench)
    "w0104": [10],          # bar
    "w0105": [9],           # Basketball
    "w0106": [8],           # basteln
    "w0107": [7],           # Bauch
    "w0108": [3],           # bauen
    "w0109": [12],          # Baum
    "w0110": [15],          # Baustelle
    "w0111": [5, 11],       # beantworten
    "w0120": [7],           # Bein
    "w0122": [1],           # Bekannte
    "w0127": [10],          # beraten
    "w0128": [12, 6],       # Berg
    "w0129": [11],          # berichten
    "w0130": [4],           # Beruf
    "w0135": [11],          # besetzt
    "w0136": [8, 6],        # besichtigen
    "w0139": [5],           # bestehen
    "w0140": [2, 10],       # bestellen
    "w0141": [1],           # Besuch
    "w0142": [1, 8],        # besuchen
    "w0143": [3],           # Bett
    "w0144": [4],           # bewerben
    "w0145": [4],           # Bewerbung
    "w0146": [12],          # bewölkt / Wolke
    "w0147": [10],          # bezahlen
    "w0148": [5, 15],       # Bibliothek
    "w0149": [2],           # Bier
    "w0150": [8],           # Bild
    "w0151": [10],          # billig
    "w0152": [2],           # Birne
    "w0153": [13],          # bis
    "w0158": [2],           # bitter
    "w0159": [12, 5],       # Blatt
    "w0161": [5],           # Bleistift
    "w0163": [11],          # Blog
    "w0165": [12],          # Blume
    "w0166": [10],          # Bluse
    "w0167": [2],           # Bohne
    "w0168": [14],          # böse
    "w0169": [2],           # braten
    "w0171": [11],          # Brief
    "w0172": [11],          # Briefmarke
    "w0173": [7],           # Brille
    "w0175": [2],           # Brot
    "w0176": [2],           # Brötchen
    "w0177": [15, 6],       # Brücke
    "w0178": [5, 8],        # Buch
    "w0179": [6],           # buchen
    "w0180": [5],           # Buchstabe
    "w0181": [5],           # buchstabieren
    "w0183": [4],           # Büro
    "w0184": [6],           # Bus
    "w0185": [2],           # Butter
    "w0186": [2, 15],       # Café
    "w0187": [2, 5],        # Cafeteria
    "w0188": [11],          # chatten
    "w0189": [4],           # Chef
    "w0190": [8],           # Club
    "w0191": [8],           # Comic
    "w0192": [11],          # Computer
    "w0193": [7],           # Creme
    "w0198": [13],          # damals
    "w0204": [13],          # dann
    "w0206": [11],          # Datei
    "w0207": [13],          # Datum
    "w0208": [13],          # dauern
    "w0216": [8],           # Disco
    "w0219": [6],           # Doppelzimmer
    "w0220": [15],          # Dorf
    "w0227": [11],          # drucken
    "w0228": [11],          # Drucker
    "w0234": [2],           # Durst
    "w0235": [3],           # Dusche
    "w0236": [7],           # duschen
    "w0237": [11, 5],       # E-Book
    "w0239": [15],          # Ecke
    "w0241": [1],           # Ehefrau
    "w0242": [2],           # Ei
    "w0245": [13],          # eilig
    "w0247": [15],          # Eingang
    "w0249": [10],          # einkaufen
    "w0250": [10, 15],      # Einkaufszentrum
    "w0251": [1, 8],        # einladen
    "w0252": [1, 8],        # Einladung
    "w0254": [6],           # einpacken
    "w0255": [6],           # einsteigen
    "w0256": [5],           # eintragen
    "w0257": [8],           # Eintritt
    "w0260": [3],           # einziehen
    "w0261": [2, 12],       # Eis
    "w0262": [11],          # E-Mail
    "w0263": [11],          # Empfänger
    "w0264": [2, 8],        # empfehlen
    "w0265": [13],          # Ende
    "w0266": [13],          # enden
    "w0267": [13],          # endlich
    "w0271": [3],           # Erdgeschoss
    "w0272": [4],           # Erfahrung
    "w0274": [7],           # erkältet sein
    "w0275": [5],           # erklären
    "w0279": [10],          # Ermäßigung
    "w0284": [2],           # essen
    "w0285": [2],           # Essen
    "w0287": [5],           # Fach
    "w0288": [6],           # (ab)fahren
    "w0289": [6],           # Abfahrt
    "w0290": [6],           # Fahrkarte
    "w0291": [6],           # Fahrplan
    "w0292": [6, 9],        # (Fahr)Rad
    "w0295": [1],           # Familie
    "w0296": [1],           # Familienname
    "w0297": [8, 9],        # Fan
    "w0301": [14],          # faul
    "w0303": [5],           # Fehler
    "w0304": [1, 8],        # Feier
    "w0305": [1, 8],        # feiern
    "w0306": [3],           # Fenster
    "w0307": [5, 6],        # Ferien
    "w0308": [8],           # fernsehen
    "w0309": [3, 8],        # Fernseher
    "w0311": [8],           # Fest
    "w0312": [8],           # Festival
    "w0313": [2],           # fett
    "w0314": [7],           # Fieber
    "w0315": [8],           # Film
    "w0317": [4],           # Firma
    "w0318": [2],           # Fisch
    "w0319": [9, 7],        # fit sein
    "w0320": [2],           # Flasche
    "w0321": [2],           # Fleisch
    "w0322": [14],          # fleißig
    "w0323": [6],           # (ab)fliegen
    "w0324": [10],          # Flohmarkt
    "w0325": [6],           # Flug
    "w0326": [6, 15],       # Flughafen
    "w0327": [6],           # Flugzeug
    "w0328": [12],          # Fluss
    "w0329": [4],           # Formular
    "w0330": [8],           # Fotoapparat
    "w0331": [8],           # fotografieren
    "w0332": [8],           # Foto
    "w0333": [5],           # Frage
    "w0335": [1],           # Frau
    "w0338": [8],           # Freizeit
    "w0340": [14],          # freuen
    "w0341": [1],           # Freund
    "w0342": [14],          # freundlich
    "w0343": [2],           # frisch
    "w0344": [14],          # froh
    "w0345": [13],          # früh
    "w0346": [13],          # früher
    "w0347": [2],           # Frühstück
    "w0348": [2],           # frühstücken
    "w0349": [7, 14],       # fühlen
    "w0350": [6],           # Führerschein
    "w0351": [8, 6],        # Führung
    "w0352": [15],          # Fundsachen
    "w0355": [7],           # Fuß
    "w0356": [9],           # Fußball
    "w0357": [2],           # Gabel
    "w0359": [3, 6],        # Garage
    "w0360": [3, 12],       # Garten
    "w0361": [1, 2],        # Gast
    "w0363": [1],           # geboren
    "w0364": [1],           # Geburtsjahr
    "w0365": [1],           # Geburtsort
    "w0366": [1, 13],       # Geburtstag
    "w0369": [14],          # gefallen
    "w0372": [15],          # gegenüber
    "w0373": [4],           # Gehalt
    "w0376": [10],          # Geld
    "w0377": [10],          # Geldbörse
    "w0378": [2],           # Gemüse
    "w0381": [6],           # Gepäck
    "w0383": [15],          # geradeaus
    "w0384": [11, 3],       # Gerät
    "w0385": [2],           # Gericht
    "w0387": [4, 10],       # Geschäft
    "w0388": [1],           # Geschenk
    "w0389": [5, 8],        # Geschichte
    "w0390": [2, 3],        # Geschirr
    "w0391": [7],           # Gesicht
    "w0392": [11],          # Gespräch
    "w0393": [13],          # gestern
    "w0394": [7],           # gesund
    "w0395": [7],           # Gesundheit
    "w0396": [2],           # Getränk
    "w0397": [9],           # gewinnen
    "w0398": [12],          # Gewitter
    "w0399": [8],           # Gitarre
    "w0400": [2],           # Glas
    "w0402": [13],          # gleich
    "w0403": [14],          # Glück
    "w0404": [14],          # glücklich
    "w0405": [1],           # Glückwunsch
    "w0406": [1],           # gratulieren
    "w0407": [2, 8],        # grillen
    "w0408": [7],           # Grippe
    "w0410": [10],          # Größe
    "w0413": [6],           # gültig sein
    "w0414": [10],          # günstig
    "w0416": [7],           # Haar
    "w0418": [2],           # Hähnchen
    "w0419": [9, 15],       # Halle
    "w0421": [7],           # Hals
    "w0422": [6],           # halten
    "w0423": [6, 15],       # Haltestelle
    "w0424": [2],           # Hamburger
    "w0425": [7],           # Hand
    "w0426": [3],           # Handtuch
    "w0427": [11],          # Handy
    "w0428": [3],           # hängen
    "w0431": [15],          # Hauptstadt
    "w0432": [3],           # Haus
    "w0433": [3],           # Haushalt
    "w0434": [5],           # Heft
    "w0435": [1],           # Heimat
    "w0436": [1],           # heiraten
    "w0437": [12],          # heiß
    "w0439": [3],           # Heizung
    "w0441": [3],           # hell (lighting context)
    "w0442": [10],          # Hemd
    "w0446": [3],           # Herd
    "w0448": [4],           # herstellen
    "w0449": [11],          # herunterladen
    "w0451": [13],          # heute
    "w0454": [12],          # Himmel
    "w0458": [8],           # Hobby
    "w0460": [1],           # Hochzeit
    "w0464": [11],          # Homepage
    "w0465": [8],           # hören
    "w0466": [10],          # Hose
    "w0467": [6],           # Hotel
    "w0468": [12],          # Hund
    "w0469": [2],           # Hunger
    "w0470": [7],           # husten
    "w0476": [12, 6],       # Insel
    "w0477": [8],           # Instrument
    "w0478": [14],          # intelligent
    "w0479": [8],           # Interesse
    "w0480": [8],           # interessieren
    "w0483": [11],          # Internet
    "w0484": [4, 11],       # Interview
    "w0486": [10],          # Jacke
    "w0487": [10],          # Jeans
    "w0490": [13],          # jetzt
    "w0491": [4],           # Job
    "w0492": [9],           # joggen
    "w0493": [6],           # Jugendherberge
    "w0496": [1],           # Junge
    "w0497": [2],           # Kaffee
    "w0498": [13],          # Kalender
    "w0499": [12],          # kalt
    "w0500": [8],           # Kamera
    "w0502": [6, 10],       # Karte
    "w0503": [2],           # Kartoffel
    "w0504": [2],           # Käse
    "w0505": [10],          # Kasse
    "w0506": [12],          # Katze
    "w0507": [10],          # kaufen
    "w0508": [10, 15],      # Kaufhaus
    "w0510": [3],           # Keller
    "w0512": [1],           # kennenlernen
    "w0513": [4, 5],        # Kenntnisse
    "w0514": [10],          # Kette
    "w0515": [1],           # Kind
    "w0516": [1, 5],        # Kindergarten
    "w0517": [8, 15],       # Kino
    "w0518": [10, 15],      # Kiosk
    "w0519": [15],          # Kirche
    "w0522": [8],           # Klavier
    "w0523": [10],          # Kleid
    "w0524": [10],          # Kleidung
    "w0526": [14],          # klug
    "w0527": [2],           # kochen
    "w0528": [6],           # Koffer
    "w0529": [4],           # Kollege
    "w0533": [1, 11],       # Kontakt
    "w0534": [10],          # Konto
    "w0536": [8],           # Konzert
    "w0537": [7],           # Kopf
    "w0538": [7],           # Körper
    "w0539": [7, 10],       # Kosmetik
    "w0540": [10],          # kosten
    "w0541": [10],          # kostenlos
    "w0542": [7],           # krank
    "w0543": [7, 15],       # Krankenhaus
    "w0544": [7],           # Krankenkasse
    "w0545": [7],           # Krankheit
    "w0546": [10],          # Kredit
    "w0547": [6, 15],       # Kreuzung
    "w0549": [8],           # Krimi
    "w0550": [2, 3],        # Küche
    "w0551": [2],           # Kuchen
    "w0552": [12],          # kühl
    "w0553": [3],           # Kühlschrank
    "w0554": [8],           # Kultur
    "w0555": [1],           # kümmern
    "w0556": [10],          # Kunde
    "w0557": [4],           # kündigen
    "w0558": [8],           # Kunst
    "w0559": [5],           # Kurs
    "w0561": [14],          # lachen
    "w0562": [10],          # Laden
    "w0563": [3],           # Lampe
    "w0564": [12, 6],       # Land
    "w0565": [12],          # Landschaft
    "w0567": [13],          # lange
    "w0569": [14],          # langweilig
    "w0570": [11],          # Laptop
    "w0572": [9],           # laufen
    "w0584": [5],           # lernen
    "w0585": [5, 8],        # lesen
    "w0586": [13],          # letzt-
    "w0588": [3],           # Licht
    "w0590": [1, 14],       # lieben
    "w0592": [8],           # Lied
    "w0593": [10],          # liefern
    "w0595": [11],          # Link
    "w0596": [15],          # links
    "w0597": [2],           # Löffel
    "w0598": [2],           # Lokal
    "w0601": [14],          # Lust
    "w0602": [14],          # lustig
    "w0604": [1],           # Mädchen
    "w0605": [7],           # Magen
    "w0606": [11],          # Mailbox
    "w0608": [8],           # malen
    "w0611": [13],          # manchmal
    "w0612": [1],           # Mann
    "w0614": [9],           # Mannschaft
    "w0615": [10],          # Mantel
    "w0616": [10, 15],      # Markt
    "w0617": [4],           # Maschine
    "w0618": [7],           # Medikament
    "w0619": [12, 6],       # Meer
    "w0628": [4],           # Messe
    "w0629": [2],           # Messer
    "w0630": [3],           # Miete
    "w0631": [3],           # mieten
    "w0632": [2],           # Milch
    "w0634": [2],           # Mineralwasser
    "w0636": [4],           # Mitarbeiter
    "w0637": [2],           # Mittagessen
    "w0640": [3],           # Möbel
    "w0641": [11],          # Mobiltelefon
    "w0643": [10],          # Mode
    "w0647": [13],          # Moment
    "w0648": [13],          # morgen
    "w0649": [6],           # Motor
    "w0650": [6],           # Motorroller
    "w0651": [7, 14],       # müde
    "w0652": [3],           # Müll
    "w0653": [7],           # Mund
    "w0654": [8, 15],       # Museum
    "w0655": [8],           # Musik
    "w0657": [10],          # Mütze
    "w0659": [3],           # Nachbar
    "w0660": [11],          # Nachricht
    "w0661": [13],          # nächste
    "w0662": [15],          # Nähe
    "w0664": [12],          # nass
    "w0665": [12],          # Natur
    "w0668": [3],           # nebenan
    "w0669": [12],          # neblig
    "w0673": [14],          # nervös
    "w0674": [14],          # nett
    "w0683": [5],           # Note
    "w0684": [5],           # notieren
    "w0685": [5],           # Notiz
    "w0687": [2],           # Nudel
    "w0695": [7],           # Ohr
    "w0696": [2],           # Öl
    "w0697": [11],          # online
    "w0698": [2],           # Orange
    "w0701": [15],          # Ort
    "w0702": [1],           # Paar
    "w0704": [6],           # packen
    "w0705": [11],          # Paket
    "w0706": [5],           # Papier
    "w0708": [10],          # Parfum
    "w0709": [15, 12],      # Park
    "w0710": [6],           # parken
    "w0711": [1],           # Partner
    "w0712": [8, 1],        # Party
    "w0713": [6],           # Pass
    "w0714": [10],          # passen
    "w0716": [11],          # Passwort
    "w0717": [4, 5],        # Pause
    "w0719": [12],          # Pferd
    "w0720": [12, 3],       # Pflanze
    "w0721": [2],           # Pizza
    "w0725": [15],          # Platz
    "w0727": [15],          # Polizei
    "w0728": [2],           # Pommes frites
    "w0729": [2],           # Portion
    "w0730": [11, 15],      # Post
    "w0731": [3],           # Poster
    "w0732": [6, 11],       # Postkarte
    "w0733": [11],          # Postleitzahl
    "w0734": [4],           # Praktikum
    "w0736": [7],           # Praxis
    "w0737": [10],          # Preis
    "w0738": [10],          # preiswert
    "w0741": [2],           # probieren
    "w0743": [10],          # Produkt
    "w0744": [8, 11],       # Programm
    "w0745": [4, 5],        # Projekt
    "w0746": [10],          # Prospekt
    "w0747": [5],           # prüfen
    "w0748": [5],           # Prüfung
    "w0749": [10],          # Pullover
    "w0750": [13, 6],       # pünktlich
    "w0751": [3],           # putzen
    "w0752": [10],          # Qualität
    "w0753": [8, 5],        # Quiz
    "w0754": [8],           # Radio
    "w0756": [15],          # Rathaus
    "w0757": [8],           # Rätsel
    "w0758": [7],           # rauchen
    "w0759": [3],           # Raum
    "w0760": [5],           # rechnen
    "w0761": [10],          # Rechnung
    "w0763": [15],          # rechts
    "w0765": [12],          # Regen
    "w0766": [12],          # regnen
    "w0768": [6],           # Reifen
    "w0770": [10],          # Reinigung
    "w0771": [2],           # Reis
    "w0772": [6],           # Reise
    "w0773": [6, 15],       # Reisebüro
    "w0774": [6],           # Reiseführer
    "w0775": [6],           # reisen
    "w0776": [9],           # reiten
    "w0777": [3],           # renovieren
    "w0778": [4],           # Rentner
    "w0781": [6, 2],        # reservieren
    "w0783": [2, 15],       # Restaurant
    "w0784": [2, 7],        # Rezept
    "w0785": [6],           # Rezeption
    "w0788": [2],           # Rind
    "w0789": [1, 10],       # Ring
    "w0790": [10],          # Rock
    "w0791": [1, 14],       # romantisch
    "w0792": [12],          # Rose
    "w0793": [7],           # Rücken
    "w0794": [6],           # Rucksack
    "w0796": [14],          # Ruhe
    "w0797": [14],          # ruhig
    "w0799": [8, 6],        # Rundgang
    "w0801": [2],           # Saft
    "w0803": [2],           # Salat
    "w0804": [2],           # Salz
    "w0805": [8],           # sammeln
    "w0806": [5],           # Satz
    "w0807": [3],           # sauber
    "w0808": [2, 14],       # sauer
    "w0810": [7],           # schädlich
    "w0812": [6],           # Schalter
    "w0813": [2],           # scharf
    "w0814": [12],          # scheinen
    "w0815": [1],           # schenken
    "w0816": [5],           # Schere
    "w0817": [11],          # schicken
    "w0818": [6],           # Schiff
    "w0819": [15, 6],       # Schild
    "w0821": [12],          # Schirm
    "w0823": [3],           # Schlafzimmer
    "w0827": [8],           # Schloss
    "w0829": [3],           # Schlüssel
    "w0830": [2],           # schmecken
    "w0831": [7],           # Schmerz
    "w0832": [3],           # schmutzig
    "w0833": [12],          # Schnee
    "w0834": [2, 7],        # schneiden
    "w0835": [12],          # schneien
    "w0837": [2],           # Schokolade
    "w0840": [3],           # Schrank
    "w0842": [5, 11],       # schreiben
    "w0843": [5],           # schriftlich
    "w0844": [10],          # Schuh
    "w0845": [5],           # Schule
    "w0846": [5],           # Schüler
    "w0849": [2],           # Schwein
    "w0848": [1, 7],        # schwanger
    "w0852": [9, 15],       # Schwimmbad
    "w0853": [9],           # schwimmen
    "w0854": [12],          # See (der - lake)
    "w0855": [12, 6],       # See (die - sea)
    "w0857": [8, 6],        # Sehenswürdigkeit
    "w0859": [3],           # Seife
    "w0861": [13],          # seit
    "w0862": [5],           # Seite
    "w0864": [8],           # Sendung
    "w0868": [8],           # singen
    "w0871": [9],           # Ski
    "w0873": [3],           # Sofa
    "w0874": [13],          # sofort
    "w0877": [12],          # Sonne
    "w0878": [12],          # sonnig
    "w0880": [8],           # spannend
    "w0881": [10],          # sparen
    "w0882": [8, 14],       # Spaß
    "w0883": [13],          # spät
    "w0884": [13],          # später
    "w0885": [8, 9],        # spazieren gehen
    "w0886": [8, 9],        # Spaziergang
    "w0887": [11],          # speichern
    "w0888": [2],           # Speisekarte
    "w0889": [8, 9],        # Spiel
    "w0890": [8, 9],        # spielen
    "w0891": [9],           # Sport
    "w0892": [9],           # sportlich
    "w0893": [9, 15],       # Sportplatz
    "w0894": [5],           # Sprache
    "w0895": [5],           # sprechen
    "w0896": [7, 4],        # Sprechstunde
    "w0897": [15],          # Stadt
    "w0898": [15, 6],       # Stadtplan
    "w0899": [8],           # Star
    "w0903": [4],           # Stelle
    "w0906": [10],          # Stiefel
    "w0907": [5],           # Stift
    "w0908": [5],           # Stipendium
    "w0909": [3],           # Stock
    "w0911": [12, 6],       # Strand
    "w0912": [15, 6],       # Straße
    "w0913": [6],           # Straßenbahn
    "w0914": [1, 14],       # streiten
    "w0916": [14, 4],       # Stress
    "w0917": [14, 4],       # stressig
    "w0918": [2],           # Stück
    "w0919": [5],           # Student
    "w0920": [5],           # studieren
    "w0921": [5],           # Studium
    "w0922": [3],           # Stuhl
    "w0925": [10, 15],      # Supermarkt
    "w0926": [2],           # Suppe
    "w0927": [9, 11],       # surfen
    "w0929": [2],           # Süßigkeiten
    "w0930": [14],          # sympathisch
    "w0931": [11],          # Tablet
    "w0932": [7],           # Tablette
    "w0933": [5],           # Tafel
    "w0934": [8],           # tanzen
    "w0935": [10],          # Tasche
    "w0936": [10, 1],       # Taschengeld
    "w0937": [2],           # Tasse
    "w0938": [10],          # (aus)tauschen
    "w0939": [6],           # Taxi
    "w0940": [4, 9],        # Team
    "w0941": [2],           # Tee
    "w0944": [11],          # Telefon
    "w0945": [11],          # telefonieren
    "w0946": [2],           # Teller
    "w0947": [9],           # Tennis
    "w0948": [7, 4],        # Termin
    "w0949": [10],          # teuer
    "w0950": [5, 11],       # Text
    "w0951": [8, 15],       # Theater
    "w0953": [6, 8],        # Ticket
    "w0955": [12],          # Tier
    "w0957": [2, 3],        # Tisch
    "w0959": [3],           # Toilette
    "w0961": [2],           # Tomate
    "w0962": [2],           # Topf
    "w0963": [2],           # Torte
    "w0966": [8, 6],        # Tour
    "w0967": [6],           # Tourist
    "w0968": [10],          # tragen
    "w0969": [9],           # trainieren
    "w0970": [9],           # Training
    "w0971": [14],          # Traum
    "w0972": [14],          # träumen
    "w0973": [14],          # traurig
    "w0974": [1],           # treffen
    "w0975": [3],           # Treppe
    "w0976": [2],           # trinken
    "w0977": [12],          # trocken
    "w0979": [10],          # T-Shirt
    "w0981": [3],           # Tür
    "w0983": [5, 9],        # üben
    "w0986": [13],          # übermorgen
    "w0987": [6],           # übernachten
    "w0988": [5],           # übersetzen
    "w0989": [5],           # Übersetzung
    "w0990": [10],          # überweisen
    "w0991": [13],          # Uhr
    "w0992": [13],          # um
    "w0993": [6],           # umsteigen
    "w0994": [3],           # umziehen
    "w0995": [3],           # Umzug
    "w0998": [6, 7],        # Unfall
    "w0999": [5, 15],       # Universität
    "w1002": [8],           # unterhalten
    "w1003": [6],           # Unterkunft
    "w1004": [8],           # unternehmen
    "w1005": [5],           # Unterricht
    "w1007": [4],           # unterschreiben
    "w1008": [4],           # Unterschrift
    "w1009": [7],           # untersuchen
    "w1010": [6],           # unterwegs sein
    "w1011": [6, 8],        # Urlaub
    "w1012": [1],           # verabredet sein
    "w1013": [8],           # Veranstaltung
    "w1015": [4],           # verdienen
    "w1016": [9, 8],        # Verein
    "w1017": [4],           # vereinbaren
    "w1019": [10],          # vergleichen
    "w1020": [10],          # verkaufen
    "w1021": [6],           # Verkehr
    "w1022": [6],           # Verkehrsmittel
    "w1023": [7, 9],        # verletzen
    "w1024": [1, 14],       # verlieben
    "w1025": [9],           # verlieren
    "w1026": [3],           # vermieten
    "w1027": [3],           # Vermieter
    "w1028": [6],           # verpassen
    "w1029": [6],           # verreisen
    "w1030": [13],          # verschieben
    "w1032": [6],           # Verspätung
    "w1033": [5],           # verstehen
    "w1035": [4],           # Vertrag
    "w1038": [12],          # Vogel
    "w1040": [9],           # Volleyball
    "w1044": [5, 4],        # vorbereiten
    "w1045": [13],          # vorgestern
    "w1046": [13],          # vorher
    "w1048": [1],           # Vorname
    "w1051": [1],           # vorstellen
    "w1054": [6],           # Wagen
    "w1058": [12],          # Wald
    "w1059": [9, 12],       # wandern
    "w1060": [13],          # wann
    "w1061": [12],          # warm
    "w1065": [3],           # Wäsche
    "w1066": [3],           # waschen
    "w1067": [2],           # Wasser
    "w1068": [11],          # Webseite
    "w1069": [10],          # wechseln
    "w1072": [15],          # Weg
    "w1074": [7],           # wehtun
    "w1078": [2],           # Wein
    "w1079": [14],          # weinen
    "w1089": [4],           # Werkstatt
    "w1090": [9, 5],        # Wettbewerb
    "w1091": [12],          # Wetter
    "w1096": [5],           # wiederholen
    "w1097": [11],          # Wiederhören
    "w1100": [12],          # Wind
    "w1101": [12],          # windig
    "w1104": [8],           # Witz
    "w1105": [14],          # witzig
    "w1109": [3],           # wohnen
    "w1110": [3],           # Wohnung
    "w1111": [3],           # Wohnzimmer
    "w1112": [12],          # Wolke
    "w1114": [4, 5],        # Workshop
    "w1115": [5],           # Wort
    "w1119": [2],           # Wurst
    "w1120": [5],           # Zahl
    "w1121": [10],          # zahlen
    "w1122": [7],           # Zahn
    "w1123": [8],           # zeichnen
    "w1125": [13],          # Zeit
    "w1126": [8],           # Zeitschrift
    "w1127": [8],           # Zeitung
    "w1128": [6],           # Zelt
    "w1129": [15],          # Zentrum
    "w1130": [5],           # Zettel
    "w1131": [5],           # Zeugnis
    "w1132": [10, 3],       # (an-) / (aus-)ziehen
    "w1133": [6],           # Ziel
    "w1134": [3, 6],        # Zimmer
    "w1135": [8],           # Zirkus
    "w1136": [2],           # Zitrone
    "w1137": [8, 15],       # Zoo
    "w1139": [2],           # Zucker
    "w1141": [14],          # zufrieden
    "w1142": [6],           # Zug
    "w1143": [5],           # zuhören
}


def main():
    with open('vocabulary.json', encoding='utf-8') as f:
        data = json.load(f)

    assigned = 0
    for w in data['words']:
        topics = ASSIGNMENTS.get(w['id'])
        if topics is not None:
            w['topic_ids'] = topics
            assigned += 1
        else:
            w['topic_ids'] = []

    with open('vocabulary.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'Done. {assigned} words assigned to topics.')

    # Print topic word counts
    counts = {}
    for w in data['words']:
        for t in w['topic_ids']:
            counts[t] = counts.get(t, 0) + 1
    for t in sorted(counts):
        print(f'  Topic {t:2d}: {counts[t]} words')


if __name__ == '__main__':
    main()
