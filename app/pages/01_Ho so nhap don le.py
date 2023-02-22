import streamlit as st
import pandas as pd
from datetime import datetime
from docxtpl import DocxTemplate
from docxcompose.composer import Composer
from docx import Document
import os
from CONFIG.config import config
from doc2pdf import convert
# import base64
# import uuid
# import re
from core import text_field, date_field, selectbox_field, get_info, chuyen_khong_dau


st.header('Làm hồ sơ đơn lẻ')
st.write('''
    Điền các thông tin dưới đây sau đó bấm nút **Tạo hồ sơ** để xác nhận.
    ''')
with st.sidebar:
    st.write("**Give me a coffee:**")
    st.write(f'''
    <img src= {config.IMAGE_COFFEE}
    alt="Give me a coffee" 
    width="90%" 
    height="auto" />
    ''',
        unsafe_allow_html=True)


BT_KHONG = config.BT_KHONG
BT_CO = config.BT_CO
CHUC_VU = config.CHUC_VU
NGHE_NGHIEP = config.NGHE_NGHIEP
CONTENT_UP = config.CONTENT_UP

# PATH_FILE_MAU = "merge_mail/IMPOT_CHAN_CHAN_fix.xls"
PATH_FILE_WORD = config.PATH_FILE_WORD
doc = DocxTemplate(PATH_FILE_WORD)

with st.form(key='my_form', clear_on_submit=True):
    ho_ten = text_field('Họ tên')
    ngay_sinh = text_field('Ngày sinh')
    noi_sinh = text_field('Nơi sinh')
    nam_nu = selectbox_field('Nam/nữ', ['Nam', 'Nữ'], index= 1)
    tinh_trang_cu_tru = selectbox_field('Tình trạng cư trú', ['Cư trú', 'Không cư trú'], index= 0)
    loai_giay_to = selectbox_field('Loại giấy tờ', ['CMND', 'Hộ chiếu', 'Căn cước', 'Khác'], index= 0)
    so_giay_to = text_field('Số giấy tờ tùy thân')
    dia_chi_thuong_tru = text_field('Địa chỉ thường trú')
    noi_o_hien_tai = text_field("Nơi ở hiện tại")
    ngay_cap = text_field('Ngày cấp')
    noi_cap = text_field('Nơi cấp')
    so_dien_thoai_dang_ky = text_field("Số điện thoại đăng ký")
    so_dien_thoai_lien_he = text_field("Số điện thoại liên hệ")
    tinh_trang_hon_nhan = selectbox_field('Tình trạng hôn nhân', ['Độc thân', 'Đã kết hôn', 'Khác'], index= 0)
    email = text_field("Email")
    nghe_nghiep = selectbox_field("Nghề nghiệp", NGHE_NGHIEP, index= 4)
    chuc_vu = selectbox_field("Chức vụ", CHUC_VU, index= 7)
    nhan_the_vat_ly = selectbox_field('Nhận thẻ vật lý', ['Có', 'Không'], index= 1)
    # if nhan_the_vat_ly == 'Có':
    dia_chi_nhan_the = text_field("Địa chỉ nhận thẻ")
    ngay_ho_so = date_field("Ngày thực hiện hồ sơ")
    nhan_vien = text_field("Tên nhân viên")
    submitted =st.form_submit_button('Tạo hồ sơ')
if submitted is not None and so_dien_thoai_dang_ky != ' ':
    # print(submitted)
    # print(ho_ten.upper())
    # ho_ten = ho_ten.upper()
    cmt, hc, can_cuoc, cm_khac = get_info(['CMND', 'Hộ chiếu', 'Căn cước', 'Khác'], loai_giay_to)
    nam1, nu = get_info(['Nam', 'Nữ'], nam_nu) 
    cu_tru, khong_cu_tru = get_info(['Cư trú', 'Không cư trú'], tinh_trang_cu_tru)
    doc_than, da_ket_hon, _ = get_info(['Độc thân', 'Đã kết hôn', 'Khác'], tinh_trang_hon_nhan)

    the_vat_ly = BT_KHONG
    if nhan_the_vat_ly == "Có":
        the_vat_ly = BT_CO
        split_ten = chuyen_khong_dau(ho_ten)
    else:
        split_ten = ' '* 23

    content = {'SĐT_Đăng_ký': so_dien_thoai_dang_ky,
    # 'Họ_tên': ho_ten,
    # 'Giới_tính': '0',
    'Ngày_sinh': ngay_sinh,
    'Nơi_sinh': noi_sinh,
    # 'Mã_số_thuế': ' ',
    # 'Tình_trạng_cư_trú': 'C',
    # 'Loại_GTTT': '0',
    'Số_GTTT': so_giay_to,
    'Ngày_cấp': ngay_cap,
    'Nơi_cấp': noi_cap,
    'Nơi_ở_hiện_tại': noi_o_hien_tai,
    'Địa_chỉ_thường_trú': dia_chi_thuong_tru,
    'SĐT_liên_hệ': so_dien_thoai_lien_he,
    # 'TT_hôn_nhân': 'DKH',
    # 'TT_hôn_nhân_khác': ' ',
    'Email': email,
    # 'Nghề_nghiệp': '5',
    # 'Chức_vụ': '8',
    'User_phát_triển_TB': ' ',
    # 'Mã_công_văn/tờ_trình': 'cho sau',
    # 'Phát_hành_thẻ_vật_lý': 'K',
    # 'Tên_in_trên_thẻ': ' ',
    'Địa_chỉ': dia_chi_nhan_the,
    # 'Tỉnh/TP': ' ',
    # 'Quận/Huyện': ' ',
    # 'Phường/Xã': ' ',
    # 'SĐT_nhận_thẻ': ' ',
    'NGAY': ngay_ho_so.day,
    'THANG': ngay_ho_so.month,
    'NAM': ngay_ho_so.year,
    'NV': nhan_vien.upper(),
    # 'NV_DUYET': ' ',
    'TEN_IN_HOA': ho_ten.upper(),
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

    CONTENT_UP.update(content)
    doc.render(CONTENT_UP)
    name_file_luu = f"merge_mail/ho_so_{so_dien_thoai_dang_ky}.docx"
    doc.save(name_file_luu)
    name_file_tai_ve = f"ho_so_{so_dien_thoai_dang_ky}.docx"

    print(f"nv {nhan_vien} da tao ho so {so_dien_thoai_dang_ky}.docx")

    convert(name_file_luu)
    name_file_luu_pdf = f"merge_mail/ho_so_{so_dien_thoai_dang_ky}.pdf"
    name_file_tai_ve_pdf = f"ho_so_{so_dien_thoai_dang_ky}.pdf"

    st.write("File hồ sơ đã tạo xong! Bấm để tải file về:")
    with open(name_file_luu, 'rb') as my_file:
        st.download_button(label = name_file_tai_ve,
                            data = my_file,
                            file_name = name_file_tai_ve)
    
    if os.path.exists(name_file_luu_pdf):
        with open(name_file_luu_pdf, 'rb') as my_file:
            st.download_button(label = name_file_tai_ve_pdf,
                            data = my_file,
                            file_name = name_file_tai_ve_pdf)

    
    

    # ho_ten = st.text_input('Họ tên')
    # ngay_sinh = st.text_input('Ngày sinh')
    # noi_sinh = st.text_input('Nơi sinh')
    # loai_giay_to = st.selectbox('Loại giấy tờ', ['CMND', 'Hộ chiếu', 'Căn cước', 'Khác'], index= 0)
    # so_giay_to = st.text_input('Số giấy tờ tùy thân')
    # dia_chi_thuong_tru = st.text_input('Địa chỉ thường trú')
    # noi_o_hien_tai = st.text_input("Nơi ở hiện tại")
    # so_dien_thoai_dang_ky = st.text_input("Số điện thoại đăng ký")
    # so_dien_thoai_lien_he = st.text_input("Số điện thoại liên hệ")
    # email = st.text_input("Email")
    # nghe_nghiep = st.selectbox("Nghề nghiệp", NGHE_NGHIEP, index= 4)
    # chuc_vu = st.selectbox("Chức vụ", CHUC_VU, index= 7)
    # st.form_submit_button('Tạo hồ sơ')