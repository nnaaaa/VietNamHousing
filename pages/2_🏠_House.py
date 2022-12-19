import streamlit as st
from src.session.index import get_data
from streamlit_pandas_profiling import st_profile_report

st.set_page_config(
    layout="wide",
)

if "is_display_table" not in st.session_state:
    st.session_state.is_display_table = False

if "is_display_chart" not in st.session_state:
    st.session_state.is_display_chart = False

st.title("Viet Nam Housing")

st.header("Dataset")
st.write("Giá nhà tại khu vực Hà Nội cung cấp bởi Kaggle.")

st.write(get_data())
st.markdown("<br><br>", unsafe_allow_html=True)

st.subheader("1. Tỉ lệ loại hình nhà ở (mặt tiền, hẻm) ở các quận")

# st.bar_chart(get_data().groupby(["Quận","Loại hình nhà ở"])["Loại hình nhà ở"].count().unstack(), use_container_width=True)
grouped_df = get_data().groupby(["Quận","Loại hình nhà ở"])["Loại hình nhà ở"].count().unstack()
grouped_df = grouped_df.fillna(0).astype(int)

# b_left, b_right, _, _, _ = st.columns(5)
table, chart = st.columns(2)


# table_button = b_left.button("Show Table", key="table", type="primary")
# chart_button = b_right.button("Show Chart", type="primary")

# if table_button:
#     st.session_state.is_display_table = not st.session_state.is_display_table
    
# if st.session_state.is_display_table:
#     table.table(grouped_df)
    
# if chart_button:
#     st.session_state.is_display_chart = not st.session_state.is_display_chart
    
# if st.session_state.is_display_chart:
#     chart.bar_chart(grouped_df, height=700)
    
table.dataframe(grouped_df, height=800)  
chart.line_chart(grouped_df, height=800)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
