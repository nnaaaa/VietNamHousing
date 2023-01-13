import streamlit as st
from src.session.index import get_dataset
from streamlit_option_menu import option_menu
from screens.index import get_routes
# from st_on_hover_tabs import on_hover_tabs

st.set_page_config(
    layout="wide",
)

# st.markdown('<style>' + open('./styles.css').read() + '</style>', unsafe_allow_html=True)

routes = get_routes()

with st.sidebar:
    global selected_screen
    
    selected_screen = option_menu("Data Science", routes['name'], 
        icons=routes['icon'], menu_icon="book")
    
    # selected_screen = on_hover_tabs(tabName=routes['name'], 
    #                      iconName=routes['icon'], default_choice=0)

routes['component'][selected_screen]()

# st.title("Viet Nam Housing")

# st.title("Viet Nam Housing")

# st.header("Dataset")
# st.write("Giá nhà tại khu vực Hà Nội cung cấp bởi Kaggle.")

# df = get_dataset().copy()

# st.dataframe(df)


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

