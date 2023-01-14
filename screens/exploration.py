import streamlit as st
import pandas as pd
import re
import math
import seaborn as sns
import matplotlib.pyplot as plt

def Exploration_Screen():
    st.title("Data exploration")
    st.header("Quá trình xử lý, khám phá dữ liệu.")
    df = pd.read_csv("./data/raw/VN_housing_dataset.csv")
    df = df.iloc[:-1, 1:]
    df_without_pre_proccessing = df
    st.markdown("Data without processing (Raw)")
    st.write(df_without_pre_proccessing)
    st.subheader("How many rows and columns?")
    n_rows, n_cols = df.shape
    st.markdown("Rows: " + str(n_rows))
    st.markdown("Columns: " + str(n_cols))
    st.subheader("What is the meaning of each row?")
    st.markdown("Each row is mmanagement some significant information of a house like address, number of rooms, number of floors, squares, price,...etc")
    st.subheader("Are there duplicated rows?")
    code = '''num_duplicated_rows = df.duplicated().sum()
    num_duplicated_rows'''
    st.code(code, language='python')
    num_duplicated_rows = df.duplicated().sum()
    st.markdown("Duplicated rows: ")
    st.markdown(str(num_duplicated_rows) + " rows")
    st.subheader("Remove duplicated rows")
    code = '''df = df.drop_duplicates()'''
    st.code(code, language='python')
    df = df.drop_duplicates()
    st.write(df)
    st.subheader("What is the meaning of each column?")
    code = '''rename_lst = ['date', 'address', 'district', 'town', 'house_type', 'paper_type', 'num_floors', 'num_rooms', 
            'squares', 'length', 'width', 'price_per_m2']
df.columns = rename_lst'''
    st.code(code, language='python')
    rename_lst = ['date', 'address', 'district', 'town', 'house_type', 'paper_type', 'num_floors', 'num_rooms', 
            'squares', 'length', 'width', 'price_per_m2']
    df.columns = rename_lst
    
    st.write(df)
    st.header("The meaning of all columns")
    st.markdown("date: The date the house is published to sell.")
    st.markdown("address: House's address.")
    st.markdown("district: House's district.")
    st.markdown("town: House's town.")
    st.markdown("house_type: House's type")
    st.markdown("paper_type: House's paper work")
    st.markdown("num_floors: How many floors are there in this house?")
    st.markdown("num_rooms: How many rooms are there in this house?")
    st.markdown("squares: Houes's squares ($m^2$)")
    st.markdown("length: House's length ($m^2$)")
    st.markdown("width: House's width ($m^2$)")
    st.markdown("price_per_m2: price per $m^2$ (millions)")
    st.subheader("What is the current data type of each column? Are there columns having inappropriate data types?")
    code = '''df.dtypes'''
    st.code(code, language='python')
    st.write(df.dtypes)
  
    st.subheader('What is the percentage of missing values?')
    for column in df.columns:
        st.write("Missing values in column {}: {} ({}%)".format(column, df[column].isnull().sum(), df[column].isnull().sum() / len(df) * 100))
    
    
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
    num_floors = df["num_floors"].tolist()
    num_rooms = df["num_rooms"].tolist()
    squares = df["squares"].tolist()
    length = df["length"].tolist()
    width = df["width"].tolist()
    price_per_m2 = df["price_per_m2"].tolist()
    paper_type = df["paper_type"].tolist()


    num_floors = map(nan_to_0, num_floors)
    num_rooms = map(nan_to_0, num_rooms)
    squares =  map(nan_to_0, squares)
    length =  map(nan_to_0, length)
    width =  map(nan_to_0, width) 
    price_per_m2 =  map(nan_to_0, price_per_m2)
    paper_type = map(nan_to_0_or_1, paper_type)


    df["num_floors"] = list(num_floors)
    df["num_rooms"] = list(num_rooms)
    df["squares"] = list(squares)
    df["length"] = list(length)
    df["width"] = list(width)
    df["price_per_m2"] = list(price_per_m2)
    
    
    st.subheader("Remove NaN and filling missing values")
    indexAge = df[ (df['length'] >= 1000) | (df['width'] >= 1000) | (df['squares'] >= 1000)].index
    df.drop(indexAge , inplace=True)
    # Phan Huy drop price_per_m2 value 0!
    df = df[(df['price_per_m2'] != 0.00)]
    st.subheader("Drop price_per_m2 value 0!")
    code = '''df = df[(df['price_per_m2'] > 0.00)]'''
    st.code(code, language='python')
    
    st.subheader("Drop num_floors > 10")
    code = '''df = df[df["num_floors"] <= 10]'''
    st.code(code, language='python')
    df = df[df["num_floors"] <= 10]
    
    st.subheader("Fill paper_type")
    code = '''df["paper_type"] = df["paper_type"].fillna("Chưa có sổ")'''
    st.code(code, language='python')
    df["paper_type"] = df["paper_type"].fillna("Chưa có sổ")
    
    st.subheader("Drop Length and width")
    df.drop(['length', 'width'], inplace=True, axis=1)
    st.dataframe(df)
    
    st.subheader("Drop missing rows")
    df = df.dropna()
    st.code("df = df.dropna()", language='python')
    
    for column in df.columns:
        st.write("Missing values in column {}: {} ({}%)".format(column, df[column].isna().sum(), df[column].isna().sum() / len(df) * 100))
        
    st.subheader("Add price column")
    df['price'] = df['price_per_m2'] * df['squares']
    st.dataframe(df[["squares", "price_per_m2", "price"]])
    
    
    st.subheader("With each numerical column, how are values distributed?")
    
    code = '''sns.set_style("whitegrid")# Set dạng hiển thị: darkgrid, whitegrid, dark, white, ticks
sns.histplot(df['price_per_m2'])'''
    st.code(code, language='python')
    st.subheader("Các biểu đồ thể hiện tổng quan các cột.")
    
    st.subheader("Giá trên m2")
    fig = plt.figure(figsize=(5, 4))
    sns.set_style("whitegrid")# Set dạng hiển thị: darkgrid, whitegrid, dark, white, ticks
    sns.histplot(df['price_per_m2'])
    plt.xlabel('Giá trên m2')
    plt.ylabel('Frequency')
    fig.suptitle("Biểu đồ về giá trên m2 của toàn bộ dữ liệu")
    st.pyplot(fig)
    fig.clf()
    
    st.subheader("Tình trạng giấy tờ")
    sns.histplot(df['paper_type'])
    plt.xlabel('Tình trạng')
    plt.ylabel('Số lượng')
    fig.suptitle("Biểu đồ về tình trạng giấy tờ của toàn bộ dữ liệu")
    st.pyplot(fig)
    fig.clf()
    
    st.subheader("Số tầng")
    sns.histplot(df['num_floors'])
    plt.xlabel('Số tầng')
    plt.ylabel('Số lượng')
    fig.suptitle("Biểu đồ về số tầng của môt nhà trên toàn bộ dữ liệu")
    st.pyplot(fig)
    fig.clf()
    
    st.subheader("Số phòng")
    sns.histplot(df['num_rooms'])
    plt.xlabel('Số phòng')
    plt.ylabel('Số lượng')
    fig.suptitle("Biểu đồ về số phòng của môt nhà trên toàn bộ dữ liệu")
    st.pyplot(fig)
    fig.clf()
    
    
    st.subheader("Diện tích")
    sns.histplot(df['squares'])
    plt.xlabel('Diện tích')
    plt.ylabel('Số lượng')
    fig.suptitle("Biểu đồ về diện tích của môt nhà trên toàn bộ dữ liệu")
    st.pyplot(fig)
    fig.clf()
    
    st.markdown('***')
    
    
    st.subheader("Min? max? Are they abnormal?")
    code = '''num_floors_max = df['num_floors'].max()
num_rooms_max = df['num_rooms'].max()
squares_max = df['squares'].max()
price_per_m2_max = df['price_per_m2'].max()

max_values = [num_floors_max, num_rooms_max, squares_max, price_per_m2_max]

header = ["num_floors(num)", "num_rooms(num)", "squares(m2)", "price_per_m2(VND)"]

max_df = pd.DataFrame(max_values, header, columns=["Max"])
num_floors_min = df['num_floors'].min()
num_rooms_min = df['num_rooms'].min()
squares_min = df['squares'].min()
price_per_m2_min = df['price_per_m2'].min()

min_values = [num_floors_min, num_rooms_min, squares_min, price_per_m2_min]

header = ["num_floors(num)", "num_rooms(num)", "squares(m2)", "price_per_m2(VND)"]

min_df = pd.DataFrame(min_values, header, columns=["Min"])
min_df
    '''
    st.code(code, language='python')
    num_floors_max = df['num_floors'].max()
    num_rooms_max = df['num_rooms'].max()
    squares_max = df['squares'].max()
    price_per_m2_max = df['price_per_m2'].max()

    max_values = [num_floors_max, num_rooms_max, squares_max, price_per_m2_max]

    header = ["num_floors(num)", "num_rooms(num)", "squares(m2)", "price_per_m2(VND)"]

    max_df = pd.DataFrame(max_values, header, columns=["Max"])
    
    
    num_floors_min = df['num_floors'].min()
    num_rooms_min = df['num_rooms'].min()
    squares_min = df['squares'].min()
    price_per_m2_min = df['price_per_m2'].min()

    min_values = [num_floors_min, num_rooms_min, squares_min, price_per_m2_min]

    header = ["num_floors(num)", "num_rooms(num)", "squares(m2)", "price_per_m2(VND)"]

    min_df = pd.DataFrame(min_values, header, columns=["Min"])
    
    st.markdown("Bảng giá trị max của các features")
    st.write(max_df)
    st.markdown("Bảng giá trị min của các features")
    st.write(min_df)
    
    
    df.to_csv("data/processed/VN_housing_dataset.csv", index=False)
    
    
    st.header("With each categorical column, how are values distributed?")
    code = '''categories = df.loc[:,df.dtypes=="object"]
categories'''
    st.code(code, language='python')
    categories = df.loc[:,df.dtypes=="object"]
    st.write(categories)
    st.markdown('***')
    
    def draw_category_with_offset_limit(category, offset, limit):
        fig, ax = plt.subplots(figsize=(20, 10))
        sns.barplot(x = category.index, y = category.values, ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation = 50)

        ax.set_xlim(offset * 40, limit * 40)
        st.pyplot(fig)
        
    house_type_category = categories.groupby('house_type')["house_type"].count()

    draw_category_with_offset_limit(house_type_category, 0, 1)
    
    district_category = categories.groupby('district')["district"].count()

    draw_category_with_offset_limit(district_category, 0, 1)
    
    town_category = categories.groupby('town')["town"].count()

    draw_category_with_offset_limit(town_category, 0, 1)
    draw_category_with_offset_limit(town_category, 1, 2)
    draw_category_with_offset_limit(town_category, 2, 3)
    draw_category_with_offset_limit(town_category, 3, 4)
    draw_category_with_offset_limit(town_category, 4, 5)
    draw_category_with_offset_limit(town_category, 5, 6)
    draw_category_with_offset_limit(town_category, 6, 7)
    draw_category_with_offset_limit(town_category, 7, 8)
    st.subheader("Data after processing")
    st.write(df)
    return