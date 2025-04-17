# Coding Coach

**LLM-basierter Coding Coach für Schüler:innen**

---

## Übersicht

Der Coding Coach ist eine interaktive Lernplattform, die Schüler:innen beim Erlernen von Python unterstützt. Die App wird von GPT-4 (OpenAI) betrieben und bietet verständliche Tutorials, spannende Aufgaben und direktes Feedback zu deinen Lösungen. Zielgruppe sind vor allem deutschsprachige Schüler:innen, die ihre Programmierkenntnisse verbessern möchten.

---

## Hauptfunktionen

- **Konzepte auswählen:** Wähle Themen wie Variablen, Operatoren, if/else, Schleifen, Listen, Funktionen und mehr.
- **Mehrsprachigkeit:** Tutorials und Aufgaben sind in Deutsch, Englisch, Ukrainisch und Spanisch verfügbar.
- **Individuelle Aufgaben:** Die App generiert automatisch altersgerechte und spannende Coding-Aufgaben.
- **Integrierter Code-Editor:** Schreibe und teste deinen Code direkt im Browser.
- **Feedback & Hilfe:** Erhalte sofortige Rückmeldungen und stelle Fragen an die KI.
- **Skill-Level-Tracking:** Verfolge deinen Lernfortschritt und steigere dein Coding-Level.

---

## Installation

1. **Repository klonen**
   ```bash
   git clone https://github.com/Frozen93/Code-Coach.git
   cd Code-Coach
   ```

2. **Abhängigkeiten installieren**  
   Empfohlen: Mit [Poetry](https://python-poetry.org/)  
   ```bash
   poetry install
   ```

   Alternativ mit pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **API-Key einrichten**  
   Lege deinen OpenAI API-Key sicher ab.  
   Erstelle dazu eine Datei `.streamlit/secrets.toml` und füge Folgendes ein:
   ```toml
   openai_key = "DEIN_OPENAI_API_KEY"
   ```
   **WICHTIG:** Teile deinen API-Key niemals öffentlich und lade die Datei niemals ins öffentliche Repository hoch!

4. **App starten**
   ```bash
   streamlit run Start.py
   ```

---

## Sicherheitshinweis zu API-Keys

- **API-Keys dürfen niemals im Quellcode oder in öffentlich zugänglichen Dateien gespeichert werden.**
- Nutze immer die `.streamlit/secrets.toml`-Datei und stelle sicher, dass diese in `.gitignore` eingetragen ist (dies ist im Projekt bereits der Fall).
- Prüfe regelmäßig, dass keine sensiblen Daten versehentlich veröffentlicht wurden.
- Bei Verdacht auf einen geleakten Key: Sofort den Key bei OpenAI zurücksetzen!

---

## Mitmachen & Feedback

Du hast Ideen für neue Aufgaben, möchtest Bugs melden oder das Projekt mitentwickeln?  
Erstelle ein Issue oder einen Pull Request auf [GitHub](https://github.com/Frozen93/Code-Coach).

---

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

---

**Viel Spaß beim Programmieren und Lernen!**