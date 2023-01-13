import streamlit as st
from questions.index import get_questions

from streamlit_option_menu import option_menu


def Analysis_Screen():
    questions = get_questions()
    with st.sidebar:
        global selected_question
        selected_question = option_menu("Questions", questions['name'], 
            icons=questions['icon'], menu_icon="patch-question")
    # question_expander = st.sidebar.expander("Questions", expanded=True)
    questions["component"][selected_question]()
    # st.write()
    # for question_name in questions["name"]:
    #     button = question_expander.button(question_name)
        
    #     if button:
    #         
        