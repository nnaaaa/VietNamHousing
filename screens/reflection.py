import streamlit as st
import pandas as pd
import re
import math
import seaborn as sns
import matplotlib.pyplot as plt

def Reflection_Screen():
    st.header("Reflection của mỗi thành viên trong team")
    
    st.subheader("Phan Gia Huy")
    st.markdown('''
- 🎖 Difficulty: Có nhiều features có trong dataset nhưng không biết cách khai thác và xử lý cũng chưa tốt.
- 🎖 Gain: Học được thêm nhiều techniques liên quan đến các thư viện khác nhau như streamlit, seaborn,...
                ''')
    
    st.subheader("Lê Nguyễn Nguyên Anh")
    st.markdown('''
- 🎖 Difficulty: đặt ra những câu hỏi chất lượng để có thể hiểu sâu về bộ dữ liệu.
- 🎖 Gain: học được cách quản lý team cũng như các kỹ năng coding trong python (streamlit, dash, pandas, sklearn, matplotlib)
                ''')
    
    st.subheader("Nguyễn Thành Hiệu")
    st.markdown('''
- 🎖 Difficulty: thiếu kiến thức về phân tích dữ liệu nên chưa khai thác sâu và tối đa được bộ dataset
- 🎖 Gain: biết thêm được về các thư viện để xử lí và trực quan hoá dữ liệu như: seaborn, sklearn, streamlit, pandas,...
                ''')
    
    button = st.button("⭐️ Thanks for following")
    if button:
        st.balloons()