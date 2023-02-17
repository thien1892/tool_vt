import streamlit as st
import pandas as pd
from datetime import datetime
from docxtpl import DocxTemplate
from docxcompose.composer import Composer
from docx import Document
import os
# import base64
# import uuid
# import re

BT_KHONG = '□'
BT_CO = '■'

CHUC_VU = ['1.Chủ cơ sở',
 '2.Chuyên viên',
 '3.GĐ Kinh doanh',
 '4.GĐ Điều hành',
 '5.Giám đốc',
 '6.Kế toán',
 '7.Kế toán trưởng',
 '8.Lao động tự do',
 '9.Nhân viên',
 '10.NV Hành chính',
 '11.Phó Chủ tịch HĐQT',
 '12.Chủ tịch HĐQT',
 '13.Phó Giám đốc',
 '14.Phó Phòng',
 '15.Tổng giám đốc',
 '16.Trưởng ban',
 '17.Trưởng đại diện',
 '18.Trưởng phòng',
 '19.Khác',
 '20.Chủ tich quận',
 '21.Chủ tịch huyện',
 '22.Chủ tịch xã',
 '23.Phó chủ tịch quận',
 '24.Phó chủ tịch huyện',
 '25.Phó chủ tịch xã',
 '26.Hiệu trưởng',
 '27.Phó hiệu trưởng',
 '28.Học sinh',
 '29.Sinh viên']

NGHE_NGHIEP = ['1.Nhân viên văn phòng',
 '2.Bác sĩ, dược sĩ, y tá',
 '3.Công chức, viên chức',
 '4.Lực lượng vũ trang',
 '5.Làm việc tự do',
 '6.Học sinh, sinh viên',
 '7.Kỹ sư xây dựng, cơ khí',
 '8.Công nhân',
 '9.Hưu trí',
 '10.Nội trợ',
 '11.Nông dân',
 '12.Khác']


CONTENT_UP = {'SĐT_Đăng_ký': ' ',
    'Họ_tên': ' ',
    # 'Giới_tính': '0',
    'Ngày_sinh': ' ',
    'Nơi_sinh': ' ',
    # 'Mã_số_thuế': ' ',
    # 'Tình_trạng_cư_trú': 'C',
    # 'Loại_GTTT': '0',
    'Số_GTTT': ' ',
    'Ngày_cấp': ' ',
    'Nơi_cấp': ' ',
    'Nơi_ở_hiện_tại': ' ',
    'Địa_chỉ_thường_trú': ' ',
    'SĐT_liên_hệ': ' ',
    # 'TT_hôn_nhân': 'DKH',
    # 'TT_hôn_nhân_khác': ' ',
    'Email': ' ',
    # 'Nghề_nghiệp': '5',
    # 'Chức_vụ': '8',
    'User_phát_triển_TB': ' ',
    # 'Mã_công_văn/tờ_trình': 'cho sau',
    # 'Phát_hành_thẻ_vật_lý': 'K',
    # 'Tên_in_trên_thẻ': ' ',
    'Địa_chỉ': ' ',
    # 'Tỉnh/TP': ' ',
    # 'Quận/Huyện': ' ',
    # 'Phường/Xã': ' ',
    # 'SĐT_nhận_thẻ': ' ',
    'NGAY': ' ',
    'THANG': ' ',
    'NAM': ' ',
    'NV': ' ',
    # 'NV_DUYET': ' ',
    # 'TEN_IN_HOA': 'VÕ VĂN THÔM',
    'NAM1': '□',
    'NU': '□',
    'CU_TRU': '□',
    'KHONG_CU_TRU': '□',
    'CMT': '□',
    'HO_CHIEU': '□',
    'CAN_CUOC': '□',
    'TICK_CM_KHAC': '□',
    'CMT_KHAC': ' ',
    'DOC_THAN': '□',
    'KET_HON': '□',
    'HN_KHAC': '□',
    'NGHE_NGHIEP': 'Làm việc tự do',
    'CHUC_VU': 'Lao động tự do',
    'THE_VAT_LY': '□',
    '__M_1': ' ',
    '__M_2': ' ',
    '__M_3': ' ',
    '__M_4': ' ',
    '__M_5': ' ',
    '__M_6': ' ',
    '__M_7': ' ',
    '__M_8': ' ',
    '__M_9': ' ',
    '__M_10': ' ',
    '__M_11': ' ',
    '__M_12': ' ',
    '__M_13': ' ',
    '__M_14': ' ',
    '__M_15': ' ',
    '__M_16': ' ',
    '__M_17': ' ',
    '__M_18': ' ',
    '__M_19': ' ',
    '__M_20': ' ',
    '__M_21': ' ',
    '__M_22': ' ',
    '__M_23': ' '}


DICT_KHONG_DAU = {'Â': 'A',
 'Ă': 'A',
 'À': 'A',
 'Á': 'A',
 'Ạ': 'A',
 'Ã': 'A',
 'Ả': 'A',
 'Ầ': 'A',
 'Ấ': 'A',
 'Ẫ': 'A',
 'Ậ': 'A',
 'Ẩ': 'A',
 'Ắ': 'A',
 'Ằ': 'A',
 'Ẳ': 'A',
 'Ặ': 'A',
 'Ẵ': 'A',
 'E': 'E',
 'Ẽ': 'E',
 'É': 'E',
 'Ẹ': 'E',
 'Ẻ': 'E',
 'È': 'E',
 'Ê': 'E',
 'Ế': 'E',
 'Ề': 'E',
 'Ể': 'E',
 'Ễ': 'E',
 'Ệ': 'E',
 'U': 'U',
 'Ú': 'U',
 'Ù': 'U',
 'Ũ': 'U',
 'Ủ': 'U',
 'Ụ': 'U',
 'Ư': 'U',
 'Ứ': 'U',
 'Ừ': 'U',
 'Ử': 'U',
 'Ữ': 'U',
 'Ự': 'U',
 'I': 'I',
 'Í': 'I',
 'Ì': 'I',
 'Ỉ': 'I',
 'Ị': 'I',
 'Ĩ': 'I',
 'O': 'O',
 'Ó': 'O',
 'Ò': 'O',
 'Õ': 'O',
 'Ỏ': 'O',
 'Ọ': 'O',
 'Ô': 'O',
 'Ố': 'O',
 'Ồ': 'O',
 'Ổ': 'O',
 'Ỗ': 'O',
 'Ộ': 'O',
 'Ơ': 'O',
 'Ớ': 'O',
 'Ờ': 'O',
 'Ở': 'O',
 'Ỡ': 'O',
 'Ợ': 'O',
 'Y': 'Y',
 'Ý': 'Y',
 'Ỳ': 'Y',
 'Ỵ': 'Y',
 'Ỹ': 'Y',
 'Ỷ': 'Y'}

def chuyen_khong_dau(text_):
    text_ = text_.strip()
    text_ = text_.upper()
    text_ = text_[:23]
    # print(len(text_))
    text_ = text_ + ' '*(23 - len(text_))
    split_text = [i if i not in DICT_KHONG_DAU.keys() else DICT_KHONG_DAU[i] for i in text_]

    return split_text


# PATH_FILE_MAU = "merge_mail/IMPOT_CHAN_CHAN_fix.xls"
PATH_FILE_WORD = "merge_mail/HO_SO_PL_PY.docx"

doc = DocxTemplate(PATH_FILE_WORD)


def text_field(label, columns=None, **input_params):
    c1, c2 = st.columns(columns or [2,5], gap="small")

    # Display field name with some alignment
    c1.markdown("##")
    c1.markdown(label)
    # Sets a default key parameter to avoid duplicate key errors
    input_params.setdefault("key", label)

    # Forward text input parameters
    return c2.text_input(" ",value = ' ', **input_params)

def date_field(label, columns=None, **input_params):
    c1, c2 = st.columns(columns or [2,5], gap="small")

    # Display field name with some alignment
    c1.markdown("##")
    c1.markdown(label)
    # Sets a default key parameter to avoid duplicate key errors
    input_params.setdefault("key", label)

    # Forward text input parameters
    return c2.date_input(" ", **input_params)

def selectbox_field(label, list_name, columns=None, **input_params):
    c1, c2 = st.columns(columns or [2, 5], gap="small")

    # Display field name with some alignment
    c1.markdown("##")
    c1.markdown(label)

    # Sets a default key parameter to avoid duplicate key errors
    input_params.setdefault("key", label)

    # Forward text input parameters
    return c2.selectbox(" ",list_name, **input_params)


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

    cmt, hc, can_cuoc, cm_khac = BT_KHONG, BT_KHONG, BT_KHONG, BT_KHONG
    if loai_giay_to == "CMND":
        cmt = BT_CO
    elif loai_giay_to == 'Hộ chiếu':
        hc = BT_CO
    elif loai_giay_to == 'Căn cước':
        can_cuoc = BT_CO
    else:
        cm_khac = BT_CO

    nam1, nu = BT_KHONG, BT_KHONG
    if nam_nu == "Nam":
        nam1 = BT_CO
    else:
        nu = BT_CO
    
    cu_tru, khong_cu_tru = BT_KHONG, BT_KHONG
    if tinh_trang_cu_tru == "Cư trú":
        cu_tru = BT_CO
    else:
        khong_cu_tru = BT_CO
    
    doc_than, da_ket_hon = BT_KHONG, BT_KHONG
    if tinh_trang_hon_nhan == "Độc thân":
        doc_than = BT_CO
    elif tinh_trang_hon_nhan == 'Đã kết hôn':
        da_ket_hon = BT_CO
    
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
    'NGHE_NGHIEP': 'Làm việc tự do',
    'CHUC_VU': 'Lao động tự do',
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

    st.write("File hồ sơ đã tạo xong! Bấm để tải file về:")
    with open(name_file_luu, 'rb') as my_file:
        st.download_button(label = name_file_tai_ve,
                            data = my_file,
                            file_name = name_file_tai_ve)



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