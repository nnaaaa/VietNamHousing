import streamlit as st
from src.session.index import get_data
import plotly.express as px
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder, MinMaxScaler
import pandas as pd
import numpy as np

st.set_page_config(
    layout="wide",
)
df = get_data().copy()

st.title("Viet Nam Housing")

st.header("Dự đoán số tầng nhà")

st.subheader("1. LabelEncode cho các cột dữ liệu (district, house_type, town)")

oe = OrdinalEncoder()
# le = LabelEncoder()
sl = MinMaxScaler()
 

df.drop(["address"], inplace=True, axis=1)
df.drop(["date"], inplace=True, axis=1)
df.drop(["length"], inplace=True, axis=1)
df.drop(["width"], inplace=True, axis=1)

df.dropna(inplace=True)

Y = df.filter(["price_per_m2"])
X = df.drop(["price_per_m2"], axis=1).copy()

X[['district', 'house_type', 'town']] = oe.fit_transform(X[['district', 'house_type', 'town']]).astype(int)
X[["num_floors", "num_rooms", "squares"]] = sl.fit_transform(X[["num_floors", "num_rooms", "squares"]])
# X = df.filter(["num_floors", "num_rooms"])

Y = sl.fit_transform(Y[["price_per_m2"]])
Y = pd.DataFrame(Y, columns=["price_per_m2"])

st.dataframe(X)

st.dataframe(Y)

# split train test data
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# train with linear regression
from sklearn.linear_model import LinearRegression
# import SGDRegressor


model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test) 

st.dataframe(predictions)

compare_df = pd.DataFrame({"Actual": y_test["price_per_m2"], "Predicted": predictions.flatten()})

st.dataframe(compare_df)

# r2 score 
from sklearn.metrics import r2_score, mean_squared_error

score = r2_score(np.array(y_test["price_per_m2"]).reshape(-1, 1), np.array(predictions).reshape(-1, 1))

st.write(score)
st.write(mean_squared_error(np.array(y_test["price_per_m2"]).reshape(-1, 1), np.array(predictions).reshape(-1, 1)))

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)