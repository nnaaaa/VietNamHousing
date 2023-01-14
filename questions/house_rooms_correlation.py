import streamlit as st
import re
from src.session.index import get_dataset
import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder, MinMaxScaler
import plotly.express as px

def nan_to_0(value):
    result = 0

    try:
        result = re.findall(r"[-+]?\d*\,?\d+|\d+", value)[0].replace(",", ".")
        result = int(result) if result.find(".") == -1 else float(result) 

    except:
        result = 0

    return result

def nan_to_0_or_1(value):
    result = 0

    try:
        float(value)
        result = 0
    except:
        result = 1

    return result


def houseRoomsCorrelation():
  st.header("Có phải khu vực có nhiều nhà thì giá càng cao")
  df = get_dataset().copy()

  rename_lst = ['No', 'date', 'address', 'district', 'town', 'house_type', 'paper_type', 'num_floors', 'num_rooms',
            'squares', 'length', 'width', 'price_per_m2']
  df.columns = rename_lst

  num_rooms = df["num_rooms"].tolist()
  price_per_m2 = df["price_per_m2"].tolist()
  paper_type = df["paper_type"].tolist()

  num_rooms = map(nan_to_0, num_rooms)
  price_per_m2 =  map(nan_to_0, price_per_m2)
  paper_type = map(nan_to_0_or_1, paper_type)

  df["num_rooms"] = list(num_rooms)
  df["price_per_m2"] = list(price_per_m2)
  df["paper_type"] = list(paper_type)

  st.subheader("1. Số lượng phòng tương ứng ở những khu vực")

  num_rooms = df.groupby(["district"])["num_rooms"].count()

  st.bar_chart(num_rooms)

  st.write("Tại sao Quận Đống Đa có số lượng phòng nhiều nhất: Quận đống đa là nơi tập trung nhiều phòng nhất vì đây là quận trung của Hà Nội với diện tích 378.100. là nơi tập trung nhiều doanh nghiệp sản xuất quốc doanh và đặc biệt các hệ thống trường đại học lớn như trường Đại học Giao thông vận tải, trường Đại học Ngoại Thương, trường Đại học Thủy lợi Hà Nội, trường Đại học Y Hà Nội, Đại học Luật Hà Nội")

  dicstrict_by_name = df[df["district"] == "Quận Đống Đa"]

  house_type = dicstrict_by_name.groupby(["house_type"])["num_rooms"].count()
  st.bar_chart(house_type)

  st.write("Chúng ta có thể thấy các loại nhà ở khu vực Đống Đa là nhà nhỏ hẻm")


  st.subheader("2. Có phải khu vực có nhiều nhà thì giá càng cao")

  price = df.groupby(["district"])["price_per_m2"].mean()
  st.bar_chart(price)


  st.write("Nhưng tại sao giá nhà của khu vực này lại có vẻ ở mức trung bình so với khu vực là Hoàng Kiếm")

  paper_type = dicstrict_by_name.groupby(["paper_type"])["paper_type"].count()
  st.dataframe(paper_type)

  disctict_diff = df[df["district"] == "Quận Hoàn Kiếm"]
  paper_type_diff = disctict_diff.groupby(["paper_type"])["paper_type"].count()

  st.dataframe(paper_type_diff)

  st.write("Mọi người có thể thấy một phần quan trọng không kém là tỉ lệ nhà đã có giấy tờ")

  st.write("Tỉ lệ nhà có giấy tờ ở Quận Đống Đa là 62% còn của quận Hoàng Kiếm là 74%")
  st.write("Rõ ràng là nhà có giấy tờ pháp lý đầy đủ vẫn có giá cao hơn so với nhà không có giấy tờ. Đây là một yếu tố quan trong khác ngoài các yếu tố liên quan như diện tích số phòng ngủ")
