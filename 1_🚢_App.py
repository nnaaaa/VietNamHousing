import streamlit as st
from src.session.index import get_dataset

st.title("Viet Nam Housing")

st.title("Viet Nam Housing")

st.header("Dataset")
st.write("Giá nhà tại khu vực Hà Nội cung cấp bởi Kaggle.")

df = get_dataset().copy()

st.dataframe(df)