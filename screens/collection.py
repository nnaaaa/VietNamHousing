import streamlit as st
import pandas as pd

def Collection_Screen():
    df = pd.read_csv("data/raw/VN_housing_dataset.csv")
    st.header("Dataset is collected from Kaggle")
    
    st.markdown("Contributed by [LE ANH DUC](https://www.kaggle.com/ladcva) and community 👉 [Visit here](https://www.kaggle.com/datasets/ladcva/vietnam-housing-dataset-hanoi?select=VN_housing_dataset.csv&fbclid=IwAR1rf0QHrY45ycc8gA_GeFE9NuRlh41_RIkrNbSB5-0t_vYw79L6PVljvGs)")
    st.dataframe(df)
    