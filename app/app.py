import streamlit as st
import glob
import datetime
import os

def check_time_file(file_):
    return (datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(file_))).total_seconds() / 3600.0


st.title("Tool hỗ trợ công việc")
st.header("Danh sách các app đã làm:")
st.write("1. Tạo hồ sơ theo file")

st.header("Danh sách các app đang làm:")
st.write("1. Tạo hồ sơ đơn lẻ")
st.write("2. Tạo hồ sơ từ nhiều CMT")
st.write("3. Tạo hồ sơ từ 1 CMT")
st.write("4. Chuyển ảnh thành PDF")
st.write("5. Nén file PDF")


FILE_GOC = ['merge_mail/IMPOT_CHAN_CHAN_fix.xls', 'merge_mail/HO_SO_PL_PY.docx']

DANH_SACH_FILE = glob.glob('merge_mail/*.*')
for file_ in DANH_SACH_FILE:
    if file_ not in FILE_GOC:
        if check_time_file(file_) > 3.0:
            os.remove(file_)
            print(f'remve {file_}')
