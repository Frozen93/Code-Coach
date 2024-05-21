import streamlit as st
from code_editor import code_editor
import sys
import io
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI


openai_api_key = st.secrets["openai_key"]
llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4o")


def display_code_editor():
    exercise_code = st.session_state["exercises"][-1] if st.session_state["exercises"] else ""
    response_dict = code_editor(
        exercise_code[10:-4],
        height=[10, 20],
        buttons=[
            {
                "name": "Send",
                "feather": "Send",
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
        key="e2"
    )
    return response_dict["text"]

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

def ask_ai_question(question, user_code):
    response = llm.stream([
        HumanMessage(
            content=f"Antworte auf die Frage des Nutzers hier: - {question} - im Bezug auf dessen Code: {user_code}."
        )
    ])
    st.write_stream(response)

def main():
    
    st.title("Schreibe deinen eigenen Code")
    
    if "exercises" not in st.session_state:
        st.session_state["exercises"] = []
    if "skill_level" not in st.session_state:
        st.session_state["skill_level"] = 0
    if "code" not in st.session_state:
        st.session_state["code"] = "No code here yet"
   
    code = display_code_editor()
    if st.button("Führe Code aus"):
        returned_code = execute_code(code)
        st.session_state["code"] = returned_code
        st.code(returned_code)
    
    question = st.text_input("Stelle Fragen zu deinem Coding Projekt:")
    if st.button("Antwort generieren"):
        ask_ai_question(question, st.session_state["code"])


main()
