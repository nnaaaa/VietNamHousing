import streamlit as st
from src.session.index import get_data
import plotly.express as px
from sklearn.preprocessing import LabelEncoder

st.set_page_config(
    layout="wide",
)
df = get_data()

st.title("Viet Nam Housing")

st.header("Dự đoán số tầng nhà")

st.subheader("1. LabelEncode cho các cột dữ liệu (district, house_type, town)")

le = LabelEncoder()
df["district"] = le.fit_transform(df["district"])
df["house_type"] = le.fit_transform(df["house_type"])
df["town"] = le.fit_transform(df["town"])

st.dataframe(df)

    


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)