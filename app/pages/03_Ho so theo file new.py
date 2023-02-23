import streamlit as st
import pandas as pd
from datetime import datetime
from docxtpl import DocxTemplate
from docxcompose.composer import Composer
from docx import Document
from core import text_field, get_info, chuyen_khong_dau
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

PATH_FILE_MAU = config.PATH_FILE_MAU_NEW
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
    ma_bao_ve = text_field("Mã bảo vệ gửi mail")
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
        ho_ten = context['Họ_tên'].upper()
        nghe_nghiep = config.NGHE_NGHIEP[int(context.get('Nghề_nghiệp'))]
        chuc_vu = config.CHUC_VU[int(context.get('Chức_vụ'))]

        cmt, hc, can_cuoc, cm_khac = get_info(['CMND', 'Hộ chiếu', 'Căn cước', 'Khác'], config.GIAY_TO_TUY_THAN.get(context['Loại_GTTT']))
        nam1, nu = get_info(['Nam', 'Nữ'], config.GIOI_TINH.get(context['Giới_tính'])) 
        cu_tru, khong_cu_tru = get_info(['Cư trú', 'Không cư trú'], config.TINH_TRANG_CU_TRU.get(context['Tình_trạng_cư_trú']))
        doc_than, da_ket_hon, _ = get_info(['Độc thân', 'Đã kết hôn', 'Khác'], config.TINH_TRANG_HON_NHAN.get(context['TT_hôn_nhân']))

        the_vat_ly = config.BT_KHONG
        if context['Phát_hành_thẻ_vật_lý'] == "C":
            the_vat_ly = config.BT_CO
            split_ten = chuyen_khong_dau(ho_ten)
        else:
            split_ten = ' '* 23
        
        context.update(
            {
            'TEN_IN_HOA': ho_ten,
            'NAM1': nam1,
            'NU': nu,
            'CU_TRU': cu_tru,
            'KHONG_CU_TRU': khong_cu_tru,
            'CMT': cmt,
            'HO_CHIEU': hc,
            'CAN_CUOC': can_cuoc,
            'TICK_CM_KHAC': cm_khac,
            'CMT_KHAC': ' ',
            'DOC_THAN': doc_than,
            'KET_HON': da_ket_hon,
            # 'HN_KHAC': '□',
            'NGHE_NGHIEP': nghe_nghiep.split('.')[-1],
            'CHUC_VU': chuc_vu.split('.')[-1],
            'THE_VAT_LY': the_vat_ly,
            '__M_1': split_ten[0],
            '__M_2': split_ten[1],
            '__M_3': split_ten[2],
            '__M_4': split_ten[3],
            '__M_5': split_ten[4],
            '__M_6': split_ten[5],
            '__M_7': split_ten[6],
            '__M_8': split_ten[7],
            '__M_9': split_ten[8],
            '__M_10': split_ten[9],
            '__M_11': split_ten[10],
            '__M_12': split_ten[11],
            '__M_13': split_ten[12],
            '__M_14': split_ten[13],
            '__M_15': split_ten[14],
            '__M_16': split_ten[15],
            '__M_17': split_ten[16],
            '__M_18': split_ten[17],
            '__M_19': split_ten[18],
            '__M_20': split_ten[19],
            '__M_21': split_ten[20],
            '__M_22': split_ten[21],
            '__M_23': split_ten[22]}
        )

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
    
    # st.write("DB username:", st.secrets["MA_BAO_VE"])
    
    # with st.expander("Gửi mail:"):
    # ma_bao_ve = st.empty()
    # with st.form("Gửi mail vt", clear_on_submit= True):
    #     ma_bao_ve = st.text_input("Vui lòng nhập mã bảo vệ:")
    #     submitted2 =st.form_submit_button('Gui mail')
    # st.write("DB username:", ma_bao_ve)
    

    # st.write(st.secrets["MA_BAO_VE"])
    # st.write(st.secrets["MA_BAO_VE"] in ma_bao_ve.lower())
    if st.secrets["MA_BAO_VE"] in ma_bao_ve.lower():
        st.write(st.secrets["MA_BAO_VE"] in ma_bao_ve.lower())
        subject = f"{name_file_tai_ve_pdf}"
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

        # filename = name_file_ho_so # In same directory as script

        # Open PDF file in binary mode
        with open(name_file_luu_pdf, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {name_file_tai_ve_pdf}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.viettel.com.vn", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
        st.write("Đã gửi mail thành công, vui lòng check email!")
    # else:
    #     st.write("Sai ma bao ve")

