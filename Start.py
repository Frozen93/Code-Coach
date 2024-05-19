import streamlit as st

st.set_page_config(layout="wide")
st.title("Willkommen zu deinem Coding Coach")

st.write("""
# Einführung

Diese App ist dein persönlicher Coding Coach, der von GPT-4 unterstützt wird. 
Egal, ob du gerade erst mit Python anfängst oder bereits Erfahrung hast, diese App 
hilft dir, deine Programmierfähigkeiten zu verbessern, indem sie dir Aufgaben stellt, 
dich unterstützt und dir Feedback gibt.

## Wie du die App benutzt

1. **Konzepte auswählen**: Wähle das Konzept, das du lernen möchtest, aus der Liste.
2. **Code und Aufgaben erhalten**: Die App generiert automatisch Code-Ausschnitte mit Aufgaben für dich.
3. **Aufgaben lösen**: Bearbeite die Aufgaben und stelle bei Bedarf Rückfragen.
4. **Feedback erhalten**: Lasse deine Lösung bewerten und hole Feedback ein.

Wir hoffen, dass diese App dir hilft, deine Programmierfähigkeiten zu verbessern und Spaß am Lernen zu haben!

## Über GPT-4

GPT-4 ist ein leistungsstarkes Sprachmodell, das von OpenAI entwickelt wurde. 
Es kann natürliche Sprache verstehen und generieren, was es ideal für 
Anwendungen wie diese macht.

Viel Spaß beim Programmieren!

""")

# Run the Streamlit app
if __name__ == "__main__":
    st.write("Gib unten deine Frage ein und klicke auf 'Senden', um zu starten:")
