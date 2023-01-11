import streamlit as st
from src.session.index import get_data
import plotly.express as px
from sklearn.preprocessing import LabelEncoder

st.set_page_config(
    layout="wide",
)

df = get_data()
st.title("Viet Nam Housing")
st.header("Dataset")
st.write(df)
st.markdown("***")
st.header("Danh sách tất cả các quận:")
district_list = list(set(df["district"]))
st.markdown(district_list)
st.header("Danh sách tất cả loại nhà:")
st.text('Nhà biệt thự: 0\nNhà mặt phố, mặt tiền: 1\nNhà ngõ, hẻm: 2\nNhà phố liền kề: 3\nKhông rõ: 4\n')
st.markdown(sorted(df["house_type"].unique()))
df['Range Price'] = pd.cut(x=df['price_per_m2'], bins=[0, 50000])
# st.write(df[df[""]])