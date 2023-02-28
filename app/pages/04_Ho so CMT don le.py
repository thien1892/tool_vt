import streamlit as st
from CONFIG.config import config
from core import text_field, get_info, chuyen_khong_dau

with st.sidebar:
    st.write("Download file mẫu:") 
    st.write("**Give me a coffee:**")
    st.write(f'''
    <img src= {config.IMAGE_COFFEE} 
    alt="Give me a coffee" 
    width="90%" 
    height="auto" />
    ''',
        unsafe_allow_html=True)

st.header('Làm hồ sơ từ CCCD')
st.write('''
    Click vào **Browes files** để up file excel. Bấm **UPLOAD!** để xác nhận.
    ''')


with st.form("Tải file cập nhật", clear_on_submit=True):

    file_name = st.file_uploader('',type = ['.xls'])
    ma_bao_ve = text_field("Mã bảo vệ gửi mail")
    submitted = st.form_submit_button("UPLOAD!") 