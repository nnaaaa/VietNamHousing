import streamlit as st
from questions.index import get_questions
from streamlit_option_menu import option_menu


def Analysis_Screen():
    questions = get_questions()
    tabs = st.tabs(questions["name"])

    for name_i in range(len(questions["name"])):
        with tabs[name_i]:
            questions["component"][questions["name"][name_i]]()

    # expander = st.expander("Questions", expanded=True)
    # for question_name in questions["name"]:
    #     clicked = expander.button(question_name)
    #     # selected_question = option_menu("Questions", questions['name'], 
    #     #     icons=questions['icon'], menu_icon="patch-question")
    #     if clicked:
    #         questions["component"][question_name]()
        