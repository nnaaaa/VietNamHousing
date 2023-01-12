import streamlit as st
from src.session.index import get_dataset
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.preprocessing import LabelEncoder
import pandas as pd

st.set_page_config(
    layout="wide",
)

data = get_dataset().copy()
le = LabelEncoder()
data["district_label"] = le.fit_transform(data["district"])
data["house_type_label"] = le.fit_transform(data["house_type"])
data["town_label"] = le.fit_transform(data["town"])
st.title("Khai thác dữ liệu về giá theo quận và nhận định sự phát triển của từng khu vực.")
st.header("Dataset")
st.write(data)

st.markdown("***")
st.header("1. Danh sách tất cả các quận:")
district_list = pd.DataFrame(data[["district","district_label"]].drop_duplicates())
# print(district_list.sort_values("district_label"))
st.write(district_list.sort_values("district_label"))

st.markdown("***")
st.header("2. Danh sách tất cả loại nhà:")
house_list = pd.DataFrame(data[["house_type","house_type_label"]].drop_duplicates())
st.write(house_list.sort_values("house_type_label"))

st.markdown("***")
st.header("3. Khai thác thông tin giá trên m2 của toàn bộ dữ liệu:")
# Giá cao nhất và thấp nhất của toàn bộ dataset
max_price = max(data['price_per_m2'])
st.markdown("Giá lớn nhất trên m2 trên toàn bộ dữ liệu: " + str(max_price) +" Triệu/m2")
st.markdown("Giá nhỏ nhất trên m2 trên toàn bộ dữ liệu: " + str(min(data["price_per_m2"])) +" Triệu/m2")
st.markdown("Tổng giá toàn bộ dữ liệu: "+ str(round(data["price_per_m2"].sum(), 2))+" Triệu/m2")
st.markdown("Trung vị của GIÁ/m2: " + str(data["price_per_m2"].median()) + " Triệu/m2")
st.markdown("Mode của thuộc tính GIÁ/m2 trong bộ dữ liệu: " + str(data["price_per_m2"].mode()[0])+ " Triệu/m2")
st.markdown("Giá trị trung bình của GIÁ trên toàn bộ dữ liệu: " + str(round(data["price_per_m2"].mean(), 2))+ " Triệu/m2")

trungBinhQuanTable = data.groupby(["district"])['price_per_m2'].agg(['sum','count'])
trungBinhQuanTable["Giá trung bình quận"] = trungBinhQuanTable["sum"]/trungBinhQuanTable["count"]
# print(trungBinhQuanTable)
st.write(trungBinhQuanTable)
trungBinhQuanTable = trungBinhQuanTable.sort_values(by=['Giá trung bình quận'], ascending=True)
fig = px.bar(trungBinhQuanTable, x = trungBinhQuanTable.index, y = trungBinhQuanTable["Giá trung bình quận"], title="Giá nhà trung bình trên 1m2 theo quận.")
st.write(fig)
st.markdown("Giá trị trung bình của GIÁ theo quận: " + str(round(trungBinhQuanTable["Giá trung bình quận"].mean(), 2))+ " Triệu/m2")
# table1["mean"] = 




xungDang = list()
dauTuSau = list()
khoDauTu = list()
for each in range(0, len(district_list)):
    chart = data[data["district_label"] == each]
    num_houses = chart['town'].count()
    chart = chart.groupby(["town"]).price_per_m2.sum().reset_index()
    fig = px.bar(chart,x = chart["town"], y = chart["price_per_m2"], title=str(data[data["district_label"] == each].iloc[0]["district"]))
    st.write(fig)
    st.markdown("Số nhà ở: " + str(num_houses))
    st.write("Tổng:  " + str(round(chart["price_per_m2"].sum(),2)) + " Triệu/m2")
    st.write("Trung bình: " + str(round((chart["price_per_m2"].sum()/num_houses), 2)) + " Triệu/m2")
    if(chart["town"].count() < 5):
        st.markdown("Đánh giá: Khu vực dân cư thưa thớt xa trung tâm ít phát triển.")
        khoDauTu.append(str(data[data["district_label"] == each].iloc[0]["district"]))
    elif ((chart["price_per_m2"].sum()/num_houses) - round(trungBinhQuanTable["Giá trung bình quận"].mean(), 2) <= 0):
        st.markdown("Đánh giá: Khu vực đang phát triển giá trị nhà thấp (dưới trung bình).")
        dauTuSau.append(str(data[data["district_label"] == each].iloc[0]["district"]))
    elif((chart["price_per_m2"].sum()/num_houses) - round(trungBinhQuanTable["Giá trung bình quận"].mean(), 2) > 0):
        st.markdown("Đánh giá: Khu vực phát triển, là trung tâm tập trung đông dân cư.")
        xungDang.append(str(data[data["district_label"] == each].iloc[0]["district"]))


# cats = ['15-50', '51-85', '86-120', '121-155', '156-190', '191-225', '226-260']
# bins=[15, 50, 85, 120, 155, 190, 225, 260]
# trungBinhQuanTable["Price"] = pd.DataFrame(pd.cut(x = trungBinhQuanTable["Giá trung bình quận"], bins=[15, 50, 85, 120, 155, 190, 225, 260]))
# trungBinhQuanTable["Price_label"] = le.fit_transform(trungBinhQuanTable["Price"])
# st.write(trungBinhQuanTable)
# charT = trungBinhQuanTable[["Price", "Price_label"]]
# charT = charT.reset_index()
# charT = charT.drop(columns=['district'])
# charT = charT.set_index('Price_label')
# st.write(charT)
# charT = charT.groupby(["Price_label"])
# charT = charT.count()
# st.write(charT)

# charT = pd.DataFrame(charT["Price"], =cats)
# st.write(charT)
#df['Range Price'] = pd.cut(x=df['price_per_m2'], bins=[0, 50000])
# st.write(df[df[""]])