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

df_top = df[['district','price_per_m2']].groupby(['district']).mean().sort_values('price_per_m2',ascending=False).head(5)

st.write(df_top)
fig = px.bar(df_top)

fig.update_layout(
    xaxis_title = 'Khu vực',
    yaxis_title = 'Giá trung bình',
    showlegend = False
)

fig.update_traces(marker_color='blue')

st.plotly_chart(fig)    
