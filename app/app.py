import streamlit as st
import glob
import datetime
import os
from CONFIG.config import config

with st.sidebar:
    st.write("**Give me a coffee:**")
    st.write(f'''
    <img src= {config.IMAGE_COFFEE} 
    alt="Give me a coffee" 
    width="90%" 
    height="auto" />
    ''',
        unsafe_allow_html=True)

st.title("Tool hỗ trợ công việc")
st.header("Danh sách các app đã làm:")
st.write("1. Tạo hồ sơ theo file")
st.write("2. Tạo hồ sơ đơn lẻ")

st.header("Danh sách các app đang làm:")

st.write("1. Tạo hồ sơ từ nhiều CMT")
st.write("2. Tạo hồ sơ từ 1 CMT")
st.write("3. Chuyển ảnh thành PDF")
st.write("4. Nén file PDF")

# import streamlit as st
# from PIL import Image

# image = Image.open('app/data_image/cafe50k.jpg')
# st.header("**Những phần mềm này là free, nếu bạn ủng hộ tôi, hãy mua cho tôi 1 ly cà phê:**")
# st.image(image, caption='Quét mã ở đây!', width = 300)

def check_time_file(file_):
    return (datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(file_))).total_seconds() / 3600.0


FILE_GOC = config.FILE_GOC

DANH_SACH_FILE = glob.glob('merge_mail/*.*')
for file_ in DANH_SACH_FILE:
    if file_ not in FILE_GOC:
        if check_time_file(file_) > config.TIME_TO_SAVE_FILE:
            os.remove(file_)
            print(f'remve {file_}')
