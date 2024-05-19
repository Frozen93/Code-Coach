import streamlit as st
import sys
import io
from code_editor import code_editor
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

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

def generate_tutorial(topic, language):
    prompt = f"""Generate a python tutorial about the topic: {topic}, using only the language {language}.
              The target group are school students between 12-18 years who are new to python.
              Example:
              Lesson
    Open Lesson in New Tab
    Close
    Introduction
    Welcome to our first lesson of the Python introductory course! Today, we will uncover the simplicity and power of Python, a universally esteemed programming language renowned for its expressiveness and readability. We'll learn and practice in the CodeSignal environment, where the Python libraries are pre-installed. By the end of this lesson, you'll grasp the foundational aspects of Python and be able to execute your very first Python code. Intriguing, isn't it?
    Understanding Python Syntax
    Every language, whether it's English, Spanish, or Python, operates under a unique syntax. This cohesive framework consists of rules and principles that delineate what is grammatically correct. Similarly, Python's syntax describes how Python programs should be composed and structured.
    Let's start with something simple! Statements are instructions that a Python interpreter can execute. For example:
    Python
    Copy
    1print("Hello, and welcome to the Python World!")
    In this statement, print() is a function that Python provides to print the provided input to the console, and "Hello, and welcome to the Python World!" is a string that is printed on the console.
    Explaining Comments in Python
    Coding is a form of art, and akin to every artist, coders leave reflections and significant explanations in their code in the form of comments. Comments are annotations or explanations providing additional insights about the code. They make your code more informative and demonstrative to others (or even to your future self). Comments do not affect your code execution or its outcome in any way but are helpful to better understand what's happening in the code.
    Python features two types of comments: single-line and multi-line. Here is what they look like:
    Python
    Copy
    1# This is a single-line comment in Python.
    2
    3'''
    4This is a 
    5multi-line comment in Python.
    6'''
    7\"""
    8This is another
    9multi-line comment in Python.
    10\"""
    In this Python code snippet, you see a single-line comment initiated with #, and a block of lines enclosed within triple quotes (single or double), forming a multi-line comment.
    Introducing Indentation in Python
    Python uniquely approaches code organization by using indentation rather than braces or keywords to determine blocks of code. This method enhances Python's readability and enforces a uniform coding style. Here's an example (you don't have to understand the meaning of the if block for now, we'll cover it in the next lessons):
    Python
    1if 5 > 2:
    2    print("Five is indeed greater than two!") # this belongs to the if block
    3print("End of program") # this does not belong to the if block
    In this code snippet, due to the indentation, the first print statement belongs to the if block, while the second print statement, which is not indented, falls outside the if block.
    Getting Familiar with Simple Print Statements
    The print() function in Python greatly resembles its real-world counterpart; it assists us in displaying data on the console. Whether it is strings, numbers, the result of an operation, or even a complex structure, if it can be represented as a string, Python can print it! Here are some examples:
    Python
    1print("Hello, world!") # prints a constant string
    2print(5) # prints a constant number
    3x = 10   # defines a variable
    4print(x) # prints a variable
    5print(3 * 7) # prints the result of an expression - 21
    6
    7# The next line prints: "Cosmo can make you 10 times more effective!"
    8print("Cosmo can make you", x, "times more effective!") # Combine the text and a variable
    In all these examples, print() accepts an argument and prints it to the console accordingly.
    Lesson Summary
    Congratulations on completing your first Python lesson! You've grasped Python's unique, beginner-friendly syntax and noted the importance of commenting for code clarity. You've learned the crucial role of indentation in Python and have observed the print() function in action. Now, prepare for engaging coding exercises to apply and consolidate these foundations. It's time to dive deeper into the thrilling journey of Python programming!
                """
    tutorial = llm.stream([HumanMessage(content=prompt)])     
    st.sidebar.write_stream(tutorial)     
    
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
                "name": "Run",
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
        options={"showLineNumbers":"True"},
        key="e1"
    )
    return response_dict["text"]

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
