import streamlit as st
from src.session.index import get_data
import plotly.express as px
from sklearn.preprocessing import LabelEncoder
import pandas as pd

st.set_page_config(
    layout="wide",
)

data = get_data()
le = LabelEncoder()
data["district_label"] = le.fit_transform(data["district"])
data["house_type_label"] = le.fit_transform(data["house_type"])
data["town_label"] = le.fit_transform(data["town"])
st.title("Viet Nam Housing")
st.header("Dataset")
st.write(data)

st.markdown("***")
st.header("Danh sách tất cả các quận:")
district_list = data[["district","district_label"]]
print(district_list)
st.markdown(district_list)

st.markdown("***")
st.header("Danh sách tất cả loại nhà:")
st.text('Nhà biệt thự: 0\nNhà mặt phố, mặt tiền: 1\nNhà ngõ, hẻm: 2\nNhà phố liền kề: 3\nKhông rõ: 4\n')
st.markdown(sorted(data['house_type'].unique()))

#df['Range Price'] = pd.cut(x=df['price_per_m2'], bins=[0, 50000])
# st.write(df[df[""]])