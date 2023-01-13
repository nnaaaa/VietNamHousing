import streamlit as st
from src.session.index import get_dataset
import plotly.express as px
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder, MinMaxScaler

st.set_page_config(
    layout="wide",
)
df = get_dataset().copy()

st.title("Viet Nam Housing")

st.header("Độ tương quan của khu vực, cơ sở hạ tầng (số tầng, số phòng, số phòng ngủ, diện tích) so với giá")

st.subheader("1. LabelEncode cho các cột dữ liệu (district, house_type, town)")

oe = OrdinalEncoder()
# df["district"] = le.fit_transform(df["district"])
# df["house_type"] = le.fit_transform(df["house_type"])
# df["town"] = le.fit_transform(df["town"])
# df[['district', 'house_type', 'town']] = oe.fit_transform(df[['district', 'house_type', 'town']]).astype(int)
# for column in df.columns:
#     print("Missing values in column {}: {} ({}%)".format(column, df[column].isna().sum(), df[column].isna().sum() / len(df) * 100))
st.dataframe(df)

st.subheader("2. Tính độ tương quan giữa các cột dữ liệu")
c_matrix, table = st.columns([1, 1])
corr = df2.corr()
fig = px.imshow(corr)
c_matrix.plotly_chart(fig)

table.dataframe(corr)



hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

#df["district"] = le.inverse_transform(df["district"])
#df["house_type"] = le.inverse_transform(df["house_type"])
#df["town"] = le.inverse_transform(df["town"])
