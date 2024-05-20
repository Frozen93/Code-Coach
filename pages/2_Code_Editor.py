import streamlit as st
from code_editor import code_editor


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
        key="e1"
    )
    return response_dict["text"]

def main():
    st.title("Schreibe deinen eigenen Code")
    display_code_editor()
    if "exercises" not in st.session_state:
        st.session_state["exercises"] = []
    if "skill_level" not in st.session_state:
        st.session_state["skill_level"] = 0

main()
