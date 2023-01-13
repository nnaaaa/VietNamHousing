import streamlit as st
from src.session.index import get_dataset
import plotly.express as px


def House_Type_Question():
    if "is_display_table" not in st.session_state:
        st.session_state.is_display_table = False

    if "is_display_chart" not in st.session_state:
        st.session_state.is_display_chart = False

    df = get_dataset().copy()
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.header("Tỉ lệ loại hình nhà ở (mặt tiền, hẻm) ở các quận, huyện")

    st.subheader("1. Cái nhìn sơ lược về số lượng nhà ở của các quận, huyện")
    table_1, chart_1 = st.columns([1,4])
    fig = px.pie(df.groupby("district").count().reset_index(),values="address",  names="district", title='Số lượng nhà ở của các quận, huyện')
    chart_1.plotly_chart(fig)



    st.subheader("2. Biểu đồ thể hiện tỉ lệ loại hình nhà ở (mặt tiền, hẻm) ở các quận, huyện")
    district_df = df[["district","house_type"]]
    table_2, chart_2 = st.columns(2)

    districts = table_2.multiselect(label="Chọn quận", options=district_df["district"].unique())
    is_select_all_districts = table_2.checkbox(label="Chọn tất cả", value=True, key="is_select_all_districts")
    types = chart_2.multiselect(label="Chọn loại hình nhà ở", options=district_df["house_type"].dropna().unique())
    is_select_all_types = chart_2.checkbox(label="Chọn tất cả", value=True, key="is_select_all_types")

    if is_select_all_districts:
        districts = district_df["district"].unique()

    if is_select_all_types:
        types = district_df["house_type"].unique()

    filterd_df = district_df.loc[district_df["district"].isin(districts) & district_df["house_type"].isin(types)]   
    grouped_df = district_df.groupby(["district","house_type"])["house_type"].count().unstack()
    grouped_df = grouped_df.fillna(0).astype(int)
    grouped_df = grouped_df.loc[grouped_df.index.isin(districts), grouped_df.columns.isin(types)]   
    grouped_df["Tổng"] = grouped_df.sum(axis=1)

    fig = px.histogram(filterd_df, x=filterd_df["district"], color=filterd_df["house_type"], barmode='group',
                height=400) 
    table_2.dataframe(grouped_df, use_container_width=True, height=500)  
    chart_2.plotly_chart(fig)


    st.subheader("3. Tỉ lệ mỗi loại hình nhà ở tại một quận cụ thể")
    district_df = df[["district","house_type"]]
    selected_district = st.selectbox(label="Chọn quận", options=district_df["district"].unique())
    fig = px.pie(district_df.loc[district_df["district"] == selected_district].groupby("house_type").count().reset_index(),values="district",  names="house_type", title=f'house_type tại {selected_district}')
    st.plotly_chart(fig)



    st.subheader("4. district nào có tỉ lệ nhà nào cao nhất?")
    THRESHOLD = 10
    filterd_df = district_df.loc[district_df["district"].isin(districts) & district_df["house_type"].isin(types)]   
    grouped_df = district_df.groupby(["district","house_type"])["house_type"].count().unstack()
    grouped_df = grouped_df.fillna(0).astype(int)
    grouped_df["Tổng"] = grouped_df.sum(axis=1)
    grouped_df = grouped_df.loc[grouped_df["Tổng"] > THRESHOLD]

    # Chart 1
    best_chart, best_table = st.columns(2)
    grouped_df["Tỉ lệ nhà hẻm (%)"] = grouped_df["Nhà ngõ, hẻm"] / grouped_df["Tổng"] * 100
    grouped_df["Tỉ lệ nhà hẻm (%)"] = grouped_df["Tỉ lệ nhà hẻm (%)"].apply(lambda x: x)
    grouped_df = grouped_df.sort_values(by="Tỉ lệ nhà hẻm (%)", ascending=False)

    best_table.dataframe(grouped_df["Tỉ lệ nhà hẻm (%)"], use_container_width=True)
    grouped_df = grouped_df.drop(["Tỉ lệ nhà hẻm (%)"], axis=1)
    the_best_district = grouped_df.head(1).drop(["Tổng"], axis=1).transpose()
    fig = px.pie(the_best_district, values=the_best_district.columns[0], names=the_best_district.index, title=f'district có tỉ lệ nhà hẻm cao nhất là {the_best_district.columns[0]}')
    best_chart.plotly_chart(fig, use_container_width=True)


    # Chart 2
    best_chart, best_table = st.columns(2)
    grouped_df["Tỉ lệ nhà mặt phố, mặt tiền (%)"] = grouped_df["Nhà mặt phố, mặt tiền"] / grouped_df["Tổng"] * 100  
    grouped_df["Tỉ lệ nhà mặt phố, mặt tiền (%)"] = grouped_df["Tỉ lệ nhà mặt phố, mặt tiền (%)"].apply(lambda x: x)
    grouped_df = grouped_df.sort_values(by="Tỉ lệ nhà mặt phố, mặt tiền (%)", ascending=False)

    best_table.dataframe(grouped_df["Tỉ lệ nhà mặt phố, mặt tiền (%)"], use_container_width=True)
    grouped_df = grouped_df.drop(["Tỉ lệ nhà mặt phố, mặt tiền (%)"], axis=1)
    the_best_district = grouped_df.head(1).drop(["Tổng"], axis=1).transpose()
    fig = px.pie(the_best_district, values=the_best_district.columns[0], names=the_best_district.index, title=f'district có tỉ lệ nhà mặt phố, mặt tiền cao nhất là {the_best_district.columns[0]}')
    best_chart.plotly_chart(fig, use_container_width=True)



    # Chart 3
    best_chart, best_table = st.columns(2)
    grouped_df["Tỉ lệ biệt thự (%)"] = grouped_df["Nhà biệt thự"] / grouped_df["Tổng"] * 100
    grouped_df["Tỉ lệ biệt thự (%)"] = grouped_df["Tỉ lệ biệt thự (%)"].apply(lambda x: x)
    grouped_df = grouped_df.sort_values(by="Tỉ lệ biệt thự (%)", ascending=False)

    best_table.dataframe(grouped_df["Tỉ lệ biệt thự (%)"], use_container_width=True)
    grouped_df = grouped_df.drop(["Tỉ lệ biệt thự (%)"], axis=1)
    the_best_district = grouped_df.head(1).drop(["Tổng"], axis=1).transpose()
    fig = px.pie(the_best_district, values=the_best_district.columns[0], names=the_best_district.index, title=f'district có tỉ lệ biệt thự cao nhất là {the_best_district.columns[0]}')
    best_chart.plotly_chart(fig, use_container_width=True)



