import streamlit as st
from src.session.index import get_data
import plotly.express as px

st.set_page_config(
    layout="wide",
    page_title="Top 5 khu vực",
    page_icon="cat",
)
df = get_data()

st.title("Viet Nam Housing")

st.header("Top 5 khu vực")

st.subheader("1. Top 5 khu vực có giá nhà trung bình cao nhất")

st.write(df)
df_top = df[['district','price_per_m2']].groupby(['district']).mean().sort_values('price_per_m2',ascending=False).head(10)

st.write(df_top)
#fig = px.bar(dfg, x=dfg['town'], y=dfg['price_per_m2'])

#st.plotly_chart(fig)
