import streamlit as st
import pandas as pd
from datetime import datetime
from docxtpl import DocxTemplate
from docxcompose.composer import Composer
from docx import Document
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
    Click vào **Browes files** để up file excel. Bấm **UPLOAD!** để xác nhận.
    ''')

with st.form("Tải file cập nhật", clear_on_submit=True):
    file_name = st.file_uploader('',type = ['.xls'])
    ma_bao_ve = st.text_input("Mã bảo vệ gửi mail", value = "Không bắt buộc điền")
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

    name_file_ho_so = f"merge_mail/hoso-{row['User_phát_triển_TB']}-{str_time}.docx"
    name_file_tai_ve = f"hoso-{row['User_phát_triển_TB']}-{str_time}.docx"
    composer.save(name_file_ho_so)

    print(name_file_ho_so)

    convert(name_file_ho_so)
    name_file_luu_pdf = f"merge_mail/hoso-{row['User_phát_triển_TB']}-{str_time}.pdf"
    name_file_tai_ve_pdf = f"hoso-{row['User_phát_triển_TB']}-{str_time}.pdf"
    
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
    
    # st.write("DB username:", st.secrets["MA_BAO_VE"])
    
    # with st.expander("Gửi mail:"):
    # ma_bao_ve = st.empty()
    # with st.form("Gửi mail vt", clear_on_submit= True):
    #     ma_bao_ve = st.text_input("Vui lòng nhập mã bảo vệ:")
    #     submitted2 =st.form_submit_button('Gui mail')
    # st.write("DB username:", ma_bao_ve)
    


    if ma_bao_ve == st.secrets["MA_BAO_VE"]:
        st.write(ma_bao_ve == st.secrets["MA_BAO_VE"])
        subject = "An email with attachment from Python by thien1892"
        body = "This is an email with attachment sent from Python by thien1892"
        sender_email = st.secrets["MAIL_VT"]
        receiver_email = st.secrets["MAIL_VT"]
        password = st.secrets["PASS_MAIL_VT"]

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email

        message.attach(MIMEText(body, "plain"))

        filename = name_file_luu_pdf  # In same directory as script

        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.viettel.com.vn", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
        st.write("Da gui mail thanh cong!!!")
    # else:
    #     st.write("Sai ma bao ve")

