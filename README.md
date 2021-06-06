# PodcastNLP

Podcast Analyse Tool zur NLP Untersuchung von deutschsprachigen Corona Podcasts.

## TODOS
    
- [x] Entwicklungsumgebung schaffen
- [x] Datenerfassung
  - [x] automatisierter Download von MP3 und Transkript
  - [x] BUG : NDR nur 39 pdfs
- [ ] Datenaufbereitung
  - [x] Ordnung
  - [ ] Unicode / ASCII Problem
  - [ ] Annotation (?)
- [ ] Auswertung
  - [ ] Wordcount per Person
  - [ ] Sentinentanalyse
    - [ ] TextBlob-de Standard
    - [ ] eigenes Wörterbuch
  - [ ] Wortartvergleich
- [ ] Visualisierung

## 0 Setup

Es wird Python >= 3.9 benötigt.
Mit `pip install -r requirements.txt` werden die nötigen Module installiert.

## 1. Datensammlung

Mit `python dataTools.py` können bei bestehender Internetverbindung die Podcast-Transkripte von MDR und NDR heruntergeladen werden.

## 2. Datenauswertung

## 3. Fazit
