import streamlit as st
import pandas as pd

@st.experimental_singleton
def get_dataset():
    df = pd.read_csv("data/processed/VN_housing_dataset.csv")
    
    return df
