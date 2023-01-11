import streamlit as st
from src.session.index import get_dataset
import plotly.express as px
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder, MinMaxScaler

st.set_page_config(
    layout="wide",
)
df = get_dataset().copy()



st.header("Ảnh hưởng của khu vực, cơ sở hạ tầng (số tầng, số phòng, số phòng ngủ, diện tích) so với giá")
st.subheader("📕 Câu trả lời sẽ: ")
st.write("- Giúp chúng ta ưu tiên lựa chọn các yếu tố ít ảnh hưởng đến giá thì đạt được căn nhà như mong muốn với giá cả phải chăng hơn")

st.subheader("1. LabelEncode cho các cột dữ liệu (district, house_type, town)")
oe = OrdinalEncoder()
df[['district', 'house_type', 'town', "paper_type"]] = oe.fit_transform(df[['district', 'house_type', 'town', 'paper_type']]).astype(int)
st.dataframe(df)


st.subheader("2. Tính độ tương quan giữa các cột dữ liệu")
c_matrix, table = st.columns([1, 1])
corr = df.corr()
fig = px.imshow(corr)
c_matrix.plotly_chart(fig)
table.dataframe(corr)


st.subheader("3. Biểu đồ tương quan của giá và các yếu tố khác của căn nhà")
price_corr = corr["price_per_m2"]
price_corr = price_corr.drop("price_per_m2").sort_values()
fig = px.bar(price_corr, x=price_corr.index, y=price_corr.values)

bar_chart, explain_container = st.columns([1, 1])
bar_chart.plotly_chart(fig)
explain_container.markdown('''
    🔥 Số lượng phòng, diện tích nhà cũng như số tầng ảnh hưởng rất nhiều đến giá <br>
    🔥 Đáng chú ý là việc nhà có giấy tờ hay chưa lại ít ảnh hưởng đến giá hơn <br>
    >  ⏩  Từ đồ thị có thể thấy rằng, khi chọn mua nhà ở khu vực này nên ưu tiên chọn số tầng hơn thay vì chọn số phòng, từ đó sẽ giảm bớt chi phí mua nhà
    🔥 Để thấy rõ sự tương quan giữa số số tầng và số phòng với giá nhà, ta hãy cùng xem qua biểu đồ phân phối giá của cả 2
''', unsafe_allow_html=True)


st.subheader("4. Biểu đồ phân phối giá của số tầng và số phòng")
num_floor_chart, num_room_chart = st.columns([1, 1])

num_floor_chart.markdown("<center>🏚 Biểu đồ phân phối giá của số tầng</center>", unsafe_allow_html=True)
floor_group = df.groupby(["num_floors"])[["price_per_m2"]].mean().reset_index()
fig = px.bar(floor_group, x="num_floors", y="price_per_m2")
num_floor_chart.plotly_chart(fig)

floor_group = df[df["num_floors"] < 11].groupby(["num_floors"])[["price_per_m2"]].mean().reset_index()
fig = px.bar(floor_group, x="num_floors", y="price_per_m2")
num_floor_chart.plotly_chart(fig)


num_room_chart.markdown("<center>🏬 Biểu đồ phân phối giá của số phòng</center>", unsafe_allow_html=True)
floor_group = df[df["num_rooms"] > 0].groupby(["num_rooms"])[["price_per_m2"]].mean().reset_index()
fig = px.bar(floor_group, x="num_rooms", y="price_per_m2")
num_room_chart.plotly_chart(fig)
st.markdown('''
    🔥 Khi đi sâu vào sự tương quan của số tầng, ta có thấy những nhà có số tầng lớn (nhà chung cư, ...) rất ít và điều đó đã gây nhiễu về sự tương quan của nó. Chúng tôi đã lọc và lấy những nhà có số tầng từ `10` trở xuống để dữ liệu thực tế hơn
    <br>
    🔥 Khi dữ liệu chỉ còn nhà `10` tầng trở xuống ta lại thấy điều ngược lại với kết luận bên trên. 
    > ⏩  Vậy nên khi chọn mua nhà ta nên ưu tiên chọn số lượng phòng thay vì số tầng để giá thành có thể giảm bớt đi. <br>
    > Lưu ý rằng: việc ưu tiên này không làm ảnh hưởng quá nhiều đến giá trừ khi số tầng hoặc số phòng lớn hơn `6 hoặc 7`
''', unsafe_allow_html=True)





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
