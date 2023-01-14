import streamlit as st
from src.session.index import get_dataset
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def District_Information_Question():
    ss = StandardScaler()
    data = get_dataset().copy()
    le = LabelEncoder()
    data["district_label"] = le.fit_transform(data["district"])
    data["house_type_label"] = le.fit_transform(data["house_type"])
    data["town_label"] = le.fit_transform(data["town"])
    st.header("Khai thác dữ liệu về giá theo quận và nhận định sự phát triển của từng khu vực.")
    st.write(data)
    st.markdown("***")

    st.header("Lợi ích của việc khai thác dữ liệu và trả lời câu hỏi trên:")
    st.subheader("Việc khai thác từng quận huyện sẽ giúp xác định, đánh giá được tổng quan quy mô và mức độ phát triển của quận, huyện đó.")

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
    each = st.selectbox(
        'Chọn quận bạn muốn?',
        district_list)
    # for each in range(0, len(district_list)):
    chart = data[data["district"] == each]
    num_houses = chart['town'].count()
    chart = chart.groupby(["town"]).price_per_m2.sum().reset_index()
    chart = chart.sort_values(["price_per_m2"])
    fig = px.bar(chart,x = chart["town"], y = chart["price_per_m2"],labels={'price_per_m2': "Tổng/m2", 'town': "Xã, Phường"}, title=str(data[data["district"] == each].iloc[0]["district"]))
    st.write(fig)
    st.markdown("Số nhà ở: " + str(num_houses))
    st.write("Tổng:  " + str(round(chart["price_per_m2"].sum(),2)) + " Triệu/m2")
    st.write("Trung bình: " + str(round((chart["price_per_m2"].sum()/num_houses), 2)) + " Triệu/m2")
    if(chart["town"].count() < 5):
        st.markdown("Đánh giá: Khu vực dân cư thưa thớt xa trung tâm ít phát triển.")
        khoDauTu.append(str(data[data["district"] == each].iloc[0]["district"]))
    elif ((chart["price_per_m2"].sum()/num_houses) - round(trungBinhQuanTable["Giá trung bình quận"].mean(), 2) <= 0):
        st.markdown("Đánh giá: Khu vực đang phát triển giá trị nhà thấp (dưới trung bình).")
        dauTuSau.append(str(data[data["district_label"] == each].iloc[0]["district"]))
    elif((chart["price_per_m2"].sum()/num_houses) - round(trungBinhQuanTable["Giá trung bình quận"].mean(), 2) > 0):
        st.markdown("Đánh giá: Khu vực phát triển, là trung tâm tập trung đông dân cư.")
        xungDang.append(str(data[data["district"] == each].iloc[0]["district"]))


    #trungBinhQuanTable["Price"] = pd.DataFrame(pd.cut(x = trungBinhQuanTable["Giá trung bình quận"], bins=[15, 50, 85, 120, 155, 190, 225, 260]))
    #trungBinhQuanTable["Price_label"] = le.fit_transform(trungBinhQuanTable["Price"])
    # trungBinhQuanTable = trungBinhQuanTable[['Giá trung bình quận']]
    quanGiaSquares = pd.DataFrame(data[["district"]])
    kmeanChart = pd.DataFrame(data[["squares","price"]])
    st.write(kmeanChart)
    wcss = []
    scaled = ss.fit_transform(kmeanChart)
    for i in range(1, 11):
        clustering = KMeans(n_clusters=i, init='k-means++', random_state=42)
        clustering.fit(kmeanChart)
        wcss.append(clustering.inertia_)
    ks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    wcss_sc = []
    for i in range(1, 11):
        clustering_sc = KMeans(n_clusters=i, init='k-means++', random_state=42)
        clustering_sc.fit(scaled)
        wcss_sc.append(clustering_sc.inertia_)
        
    ks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    st.header("Sử dụng elbow method để chia cụm để quan sát sự phân bổ của giá theo diện tích.")
    fig = plt.figure(figsize=(10, 5))
    sns.lineplot(x = ks, y = wcss)
    st.pyplot(fig)
    fig.clf()
    sns.lineplot(x = ks, y = wcss_sc)
    st.pyplot(fig)
    fig.clf()
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15,5))
    sns.scatterplot(ax=axes[0], data=kmeanChart, y='price', x='squares').set_title('Without clustering')
    sns.scatterplot(ax=axes[1], data=kmeanChart, y='price', x='squares', hue=clustering.labels_).set_title('Using the elbow method')
    sns.scatterplot(ax=axes[2], data=kmeanChart, x='squares', y='price', hue=clustering_sc.labels_).set_title('With the Elbow method and scaled data')
    st.pyplot(fig)
    st.write(kmeanChart.describe().T)
    scaled = ss.fit_transform(kmeanChart)
    wcss_sc = []
    st.header("Perform K-Means Clustering with Optimal K")
    st.subheader("Ở đây ta có thể thấy k ~= 3")
    kmeans = KMeans(init="random", n_clusters=3, n_init=10, random_state=1)
    kmeans.fit(scaled)
    kmeanChart['Cluster'] = kmeans.labels_
    kmeanChart.join(quanGiaSquares)
    st.write(kmeanChart.sort_values('Cluster'))

# charT = trungBinhQuanTable[["Price", "Price_label"]]
# st.write(charT)
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