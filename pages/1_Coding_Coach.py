import streamlit as st
import sys
import io
from code_editor import code_editor
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from prompts import prompts, tutorials

# Setup LLM and API key
openai_api_key = st.secrets["openai_key"]
llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4o")

#TODO Aufgabenstellung nicht in kommentare sondern links in sidebar und mit Markdown erstellen?!

st.set_page_config(layout="wide")
# Define main function
def main():
    if "exercises" not in st.session_state:
        st.session_state["exercises"] = []
    if "skill_level" not in st.session_state:
        st.session_state["skill_level"] = 0
    st.title("Coding Coach")

    l,_, r = st.columns(3)
    with l:
        # User input for topic and language
        topic = st.selectbox("Wähle ein Thema", ["Variablen & Operatoren", "if/else", "Klassen", "Schleifen", "Listen & Dicts", "Funktionen"])
        language = st.selectbox("Wähle eine Sprache", ["Deutsch", "Englisch", "Ukrainisch", "Spanisch"])
    with r:
        show_skill_level()
    # Initialize exercises in session state if not present
    if "exercises" not in st.session_state:
        st.session_state["exercises"] = []
    if "skill_level" not in st.session_state:
        st.session_state["skill_level"] = 0
    # Generate exercise based on user input
    if topic and language:
        if topic == "Variablen & Operatoren":
            with st.sidebar.popover(f"Tutorial {topic}"):
                st.markdown(tutorials["variablen_operatoren"])
        if topic == "if/else":
            with st.sidebar.popover(f"Tutorial {topic}"):
                st.markdown(tutorials["if_else"])
        generate_exercise(topic, language)
        user_code = display_code_editor()

        # User input for question
        question = st.text_input("Stelle eine Frage")
        if st.button("Frage absenden"):
            ask_ai_question(question, user_code, language)
        st.divider()
        # Button to execute user code
        if st.button("Code ausführen + Feedback erhalten"):
            evaluate_correctnes(user_code)
            run_and_display_code(user_code, language)
            
@st.experimental_fragment(run_every="5s")
def show_skill_level():
    st.progress(st.session_state["skill_level"], f"Dein Coding Level: {st.session_state['skill_level']}")
    #st.metric(label="Aktuelles Coding-Level", value=st.session_state["skill_level"], delta=0)

def update_skill_level(user_code):
    st.session_state["skill_level"] += evaluate_correctnes(user_code)
      
# Generate exercise using LLM
def generate_exercise(topic, language):
    prompt = (
        f"You output python engaging and interesting coding exercises by providing incomplete code-snippet about the topic of {topic} "
        f"which uses {language} and shows where the student needs to complete the code and what the task is. "
        f"Make sure there are 1-3 tasks for the student and don't implement the solution yourself! You output only code! Make sure you dont solve the tasks in the comments yourself. The comments should clearly state the task and the number of the task e.g. task1, be specific!"
        f"The context of the task should be interesting and engaging for school students. The difficulty should be based on the skill level of the learner which is between 1 -new to Python- and 100 -intermediate-. The current skill level is {st.session_state['skill_level']}"
        """Beispiel: #Something is off with the code provided. We were hoping it would print the text "Greetings, Python #learners!". However, upon running, it seems to produce an error. Can you spot where the issue is #and fix the code?

print("Greetings,
 Python learner!")  # This prints a string"""
    )
    if st.button("Erstelle Übung"):
        # Todo provide fixed tutorials!
        #generate_tutorial(topic, language)
        exercise_code = llm.invoke([HumanMessage(content=prompt)]).content
        st.session_state["exercises"].append(exercise_code)
    elif len(st.session_state["exercises"]) > 0:
        exercise_code = st.session_state["exercises"][-1]
    else:
        exercise_code = ""

    return exercise_code

# Display the code editor
def display_code_editor():
    exercise_code = st.session_state["exercises"][-1] if st.session_state["exercises"] else ""
    response_dict = code_editor(
        exercise_code[10:-4],
        height=[10, 20],
        buttons=[
            {
                "name": "Ausführen",
                "feather": "Play",
                "primary": True,
                "hasText": True,
                "showWithIcon": True,
                "commands": ["submit"],
                "style": {"bottom": "0.44rem", "right": "0.4rem"}
            },
            {
                "name": "Copy",
                "feather": "Copy",
                "alwaysOn": True,
                "commands": ["copyAll"],
                "style": {"top": "0.46rem", "right": "0.4rem"}
            }
        ],
        allow_reset=True,
        options={"showLineNumbers": "True"},
        key="e1"
    )
    user_code = response_dict["text"]

    # Prüfen, ob der "Ausführen"-Button gedrückt wurde
    if response_dict.get("button") == "Ausführen":
        st.write("**Ausgabe:**")
        result = execute_code(user_code)
        st.code(result)

    return user_code

# Ask AI a question about the current task
def ask_ai_question(question, user_code, language):
    response = llm.stream([
        HumanMessage(
            content=f"Antworte in der Sprache {language} auf die Frage {question} im Bezug auf die aktuelle Aufgabe: {user_code}. "
                    "Gib aber keine Lösungen zu den Aufgaben an! Nutze Markdown und Emojis um deine Antwort strukturiert darzustellen. "
                    "Deine Zielgruppe sind Schüler, passe das Niveau an."
        )
    ])
    st.write_stream(response)

def evaluate_correctnes(user_code):
    response = llm.invoke([
        HumanMessage(
            content=f"Evaluiere, wie gut der Code des Schülers die Aufgaben löst und bewerte das Resultat mit 1-5 Punkten, wobei 5 Punkte bei vollständiger und richtiger Lösung der Aufgabe gegeben werden. Falls die Aufgaben nicht gelöst wurden, oder nur die Variablennamen/Funktionsnamen aufgeschrieben wurden gib 1 Punkt. Hier der Code: {user_code}. Antworte nur mit der Zahl zwischen 1-5!"
        )
    ])
    return int(response.content)

# Execute the user code and display the result
def run_and_display_code(user_code, language):
    update_skill_level(user_code)
    result = execute_code(user_code)
    st.write("**Output:**")
    st.code(result)

    st.markdown("Evaluierung")
    response = llm.stream([
        HumanMessage(
            content=f"""Überprüfe, ob der folgende Code, angegebenen Aufgaben korrekt implementiert: {user_code}. 
                    Wichtig: Gib konstruktives, motivierendes Feedback in der Sprache {language}. 
                    Gib an welche Aufgaben korrekt abgeschlossen wurden, und Hinweise, wie die nicht abgeschlossenen Aufgaben zu beenden sind. 
                    Gib keine Teillösungen oder Lösungen an, sondern nur nützliche Hinweise, oder allgemeine Beispiele! 
                    Strukturiere deine Antwort mit Markdown und Emojis. Das Niveau der Antwort soll für Schüler verständlich sein. 
                    Nutze Emojis um zu zeigen, welche Aufgaben vollständig gelöst wurden und welche nicht. Halte dich kurz und denke daran nur auf {language} zu schreiben! Hier ein Beispiel: 
                    Feedback zu deinem Code
                    Aufgabe 1: Zahlen von 1 bis 10 ausgeben
                    for i in range(1, 11):
                        # TODO: Ausgabe der Zahl i
                        pass

                    🔄 Nicht abgeschlossen: Du hast die Schleife korrekt erstellt, die Zahlen von 1 bis 10 durchläuft. Jetzt musst du nur noch den print-Befehl verwenden, um die Zahl i auszugeben. Schau dir an, wie man in Python Ausgaben auf der Konsole macht!

                    Aufgabe 2: Alle Elemente einer Liste ausgeben
                    meine_liste = [3, 5, 7, 9, 11]

                    for element in meine_liste:
                        # TODO: Ausgabe des Elements
                        pass

                    🔄 Nicht abgeschlossen: Du hast die Schleife richtig eingerichtet, um durch die Liste zu iterieren. Auch hier fehlt nur noch der print-Befehl, um jedes Element der Liste auszugeben. Denk daran, dass element die einzelnen Werte der Liste repräsentiert!

                    Tipps zum Weiterarbeiten
                    🖨️ Ausgabe in Python: Um in Python etwas auszugeben, kannst du den print-Befehl verwenden. Zum Beispiel, um die Zahl i auszugeben, könntest du print(i) innerhalb der Schleife verwenden.
                    📝 Dokumentation: Wenn du dir unsicher bist, wie etwas funktioniert, schau in der offiziellen Python-Dokumentation nach oder such online nach Beispielen.
                    Du bist auf einem guten Weg! Mach weiter so und probiere die print-Anweisungen in deinen Schleifen aus. Du wirst sehen, wie schnell du Fortschritte machst! 🚀

                    Viel Erfolg und bleib motiviert! 💪"""
        )
    ])
    st.write_stream(response)

# Execute code and capture output
def execute_code(code):
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    try:
        exec(code)
    except Exception as e:
        return str(e)
    finally:
        sys.stdout = old_stdout
    return redirected_output.getvalue()

# Run the app
if __name__ == "__main__":
    main()
