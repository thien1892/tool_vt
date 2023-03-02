import streamlit as st
import pandas as pd
from datetime import datetime
from docxtpl import DocxTemplate
from docxcompose.composer import Composer
from docx import Document
from core import text_field, send_email, check_user_pass
import os
from CONFIG.config import config
from doc2pdf import convert

import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# import base64
# import uuid
# import re

PATH_FILE_MAU = config.PATH_FILE_MAU
PATH_FILE_WORD = config.PATH_FILE_WORD

doc = DocxTemplate(PATH_FILE_WORD)


with st.sidebar:
    st.write("Download file mẫu:")
    with open(PATH_FILE_MAU, 'rb') as my_file:
        st.download_button(label = 'file_mau_ho_so.xls',
                        data = my_file,
                        file_name = 'file_mau_ho_so.xls')
    
    st.write("**Give me a coffee:**")
    st.write(f'''
    <img src= {config.IMAGE_COFFEE} 
    alt="Give me a coffee" 
    width="90%" 
    height="auto" />
    ''',
        unsafe_allow_html=True)

st.header('Làm hồ sơ theo file')
st.write('''
    Click vào **Browes files** để up file excel. Bấm **UPLOAD!** để xác nhận. \n
    Nếu gửi mail, điền user và password vào (**tùy chọn không bắt buộc điền**)
    ''')

with st.form("Tải file cập nhật", clear_on_submit=True):
    file_name = st.file_uploader('',type = ['.xls'])
    user_mail = text_field("User mail viettel", value = '')
    pass_mail = text_field("Pass mail viettel", value = '', type = 'password')
    submitted = st.form_submit_button("UPLOAD!")   

# file = st.file_uploader("Upload file excel", key="file_uploader", type = 'xls')
if submitted and file_name is not None:
    df = pd.read_excel(file_name, dtype = {'SĐT Đăng ký': str, 'Số GTTT': str, 'SĐT liên hệ': str})
    df = df.dropna(subset=['SĐT Đăng ký', 'Họ tên'])
    df = df.fillna(" ")

    name_col = df.columns.to_list()
    name_col = ["_".join(i.split(' ')) for i in name_col]
    text_col = [" "] * len(name_col)

    df.columns = name_col

    for index, row in df.iterrows():
        # doc = DocxTemplate(PATH_FILE_WORD)
        row_ct = [str(row[i]) for i in name_col]
        
        context = dict(zip(name_col, row_ct))
        #fix in hoa
        context['TEN_IN_HOA'] = context['Họ_tên'].upper()
        doc.render(context)
        if index == 0:
            doc.save(f"merge_mail/ho_so_{row['SĐT_Đăng_ký']}.docx")
            master = Document(f"merge_mail/ho_so_{row['SĐT_Đăng_ký']}.docx")
            composer = Composer(master)
            os.remove(f"merge_mail/ho_so_{row['SĐT_Đăng_ký']}.docx")
        else:
            composer.append(doc)
        # doc.save(f"merge_mail/ho_so_{row['SĐT_Đăng_ký']}.docx")
    str_time = datetime.now().strftime("%H-%M_%d-%m-%Y")

    name_file_ho_so = f"merge_mail/hoso-{row['NV']}-{str_time}.docx"
    name_file_tai_ve = f"hoso-{row['NV']}-{str_time}.docx"
    composer.save(name_file_ho_so)

    print(name_file_ho_so)

    convert(name_file_ho_so)
    name_file_luu_pdf = f"merge_mail/hoso-{row['NV']}-{str_time}.pdf"
    name_file_tai_ve_pdf = f"hoso-{row['NV']}-{str_time}.pdf"
    
    st.write("File hồ sơ đã tạo xong! Bấm để tải file về:")
    with open(name_file_ho_so, 'rb') as my_file:
        st.download_button(label = name_file_tai_ve,
                            data = my_file,
                            file_name = name_file_tai_ve)
        
    if os.path.exists(name_file_luu_pdf):
        with open(name_file_luu_pdf, 'rb') as my_file:
            st.download_button(label = name_file_tai_ve_pdf,
                            data = my_file,
                            file_name = name_file_tai_ve_pdf)
            
    user_mail = user_mail+'@viettel.com.vn'  
    if check_user_pass(user_mail, pass_mail):
        # st.write(st.secrets["MA_BAO_VE"] in ma_bao_ve.lower())
        send_email(sender_email= user_mail,
                   receiver_email= user_mail,
                   password= pass_mail,
                   body= "Send email from thien1892",
                   files_attach= [name_file_luu_pdf, name_file_ho_so])
    else:
        st.write('User hoặc pasword sai, không thể gửi mail!')

