import streamlit as st
from src.session.index import get_dataset
import plotly.express as px
import pandas as pd
import altair as alt

def Price_Fluctuation_Question():
  df = get_dataset().copy()

  st.header("Biến động giá nhà")

  #st.subheader("1. Biến động giá nhà")

  df_fl = df.copy()
  df_fl['date'] = pd.to_datetime(df_fl['date']).dt.date
  df_fl['month'] = pd.DatetimeIndex(df_fl['date']).month
  df_fl['year'] = pd.DatetimeIndex(df_fl['date']).year

  df_fl = df_fl[['district', 'year', 'month', 'price_per_m2']].groupby(['district', 'year', 'month']).mean().sort_values('district',ascending=False).reset_index().rename(columns={'district':'district', 'year':'year', 'month':'month', 'price_per_m2':'average_price_per_m2'})

  df_fl['period'] = df_fl['year'].astype(str) + ' - T' + df_fl['month'].astype(str)
  st.write(df_fl)

  selected_district = st.selectbox(label="Chọn khu vực", options=df_fl["district"].unique())

  df_fl_selected = df_fl.loc[df_fl['district'] == selected_district]

  lines = alt.Chart(df_fl_selected).mark_line().encode(
    x=alt.X('period:N'),
    y=alt.Y('average_price_per_m2:Q'),
    color=alt.Color("district:N")
  ).properties(title="Biến động giá nhà trung bình của " + selected_district + " qua các thời điểm")

  points = alt.Chart(df_fl_selected).mark_point(filled=True, opacity=1).encode(
    x=alt.X('period:N'),
    y=alt.Y('average_price_per_m2:Q'),
    color=alt.Color("district:N")
  )

  st.altair_chart(lines + points, use_container_width=True)
