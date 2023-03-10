import streamlit as st
import pandas as pd
from datetime import datetime
from docxtpl import DocxTemplate
from docxcompose.composer import Composer
from docx import Document
from core import text_field, get_info, chuyen_khong_dau, send_email, check_user_pass, select_radio
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
PATH_FILE_WORD_NOPL = config.PATH_FILE_WORD_NOPL



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
    Click vào **Browes files** để up file excel. Bấm **UPLOAD!** để xác nhận.\n
    Nếu gửi mail, điền user và password vào (**tùy chọn không bắt buộc điền**)
    ''')

with st.form("Tải file cập nhật", clear_on_submit=True):
    file_name = st.file_uploader('',type = ['.xls', '.xlsx'])
    co_pl = select_radio("Hình thức hồ sơ:", ["Có phụ lục", 'Không phụ lục'])
    # ma_bao_ve = text_field("Mã bảo vệ gửi mail")
    user_mail = text_field("User mail viettel", value = '')
    pass_mail = text_field("Pass mail viettel", value = '', type = 'password')
    submitted = st.form_submit_button("UPLOAD!")   

# file = st.file_uploader("Upload file excel", key="file_uploader", type = 'xls')
if submitted and file_name is not None:
    if co_pl == "Có phụ lục":
        doc = DocxTemplate(PATH_FILE_WORD)
    else:
        doc = DocxTemplate(PATH_FILE_WORD_NOPL)
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
        nghe_nghiep = config.NGHE_NGHIEP[int(context.get('Nghề_nghiệp')) - 1]
        chuc_vu = config.CHUC_VU[int(context.get('Chức_vụ')) - 1]

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
        

