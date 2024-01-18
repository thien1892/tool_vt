import streamlit as st
from CONFIG.config import config
from core import text_field, date_field, selectbox_field, get_info, save_img
from core import chuyen_khong_dau, up_field, get_rois, check_user_pass, send_email, read_qr
from docxtpl import DocxTemplate
from docxcompose.composer import Composer
from docx import Document
import os
from datetime import datetime
from doc2pdf import convert
from PIL import Image
import zbarlight
# from kraken import binarization

with st.sidebar:
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
    Click vào **Browes files** để up file ảnh. Bấm **UPLOAD!** để xác nhận. File ảnh CCCD gồm mặt trước & mặt sau, file ảnh QR code chỉ chụp phần QR code trên mặt trước.
    ''')

BT_KHONG = config.BT_KHONG
BT_CO = config.BT_CO
CHUC_VU = config.CHUC_VU
NGHE_NGHIEP = config.NGHE_NGHIEP
CONTENT_UP = config.CONTENT_UP

PATH_FILE_WORD = config.PATH_FILE_WORD
doc = DocxTemplate(PATH_FILE_WORD)


with st.form("Tải file cập nhật", clear_on_submit=True):

    file_name = up_field('File ảnh CCCD',type = ['.jpg', '.png'], accept_multiple_files= True)
    file_qr = up_field('File ảnh QR code',type = ['.jpg', '.png'])
    # text_qr = text_field("Thông tin QR")
    tinh_trang_cu_tru = selectbox_field('Tình trạng cư trú', ['Cư trú', 'Không cư trú'], index= 0)
    so_dien_thoai_dang_ky = text_field("Số điện thoại đăng ký")
    tinh_trang_hon_nhan = selectbox_field('Tình trạng hôn nhân', ['Độc thân', 'Đã kết hôn', 'Khác'], index= 0)
    email = text_field("Email")
    nghe_nghiep = selectbox_field("Nghề nghiệp", NGHE_NGHIEP, index= 4)
    chuc_vu = selectbox_field("Chức vụ", CHUC_VU, index= 7)
    nhan_the_vat_ly = selectbox_field('Nhận thẻ vật lý', ['Có', 'Không'], index= 1)
    # if nhan_the_vat_ly == 'Có':
    dia_chi_nhan_the = text_field("Địa chỉ nhận thẻ")
    ngay_ho_so = date_field("Ngày thực hiện hồ sơ")
    nhan_vien = text_field("Tên nhân viên")
    user_mail = text_field("User mail viettel", value = '')
    pass_mail = text_field("Pass mail viettel", value = '', type = 'password')
    # ma_bao_ve = text_field("Mã bảo vệ gửi mail")
    submitted = st.form_submit_button("UPLOAD!")

if submitted is not None and so_dien_thoai_dang_ky != ' ':
    # st.write(file_name[0])
    # print(submitted)
    # print(ho_ten.upper())
    # ho_ten = ho_ten.upper()
    # if len(text_qr.split('|') ) < 5:
    #     tt_cccd = read_qr(file_qr)
    # else:
    #     tt_cccd = text_qr
    # for _img in file_name:
    # img = Image.open(file_qr)
    # rois = get_rois(img)
    # for roi in rois:
    #     try:
    #         image = Image.fromarray(roi)
    #         image = image.resize((200,200))
    #         codes = zbarlight.scan_codes(['qrcode'], image)[0].decode('utf8')
    #         tt_cccd.append(codes)
    #     except:
    #         pass
    tt_cccd = read_qr(file_qr)
    
    st.write(tt_cccd)
    if tt_cccd != -1:
        so_giay_to, _, ho_ten, ngay_sinh, nam_nu, dia_chi_thuong_tru, ngay_cap = tt_cccd.split('|')        

        ngay_sinh = f'{ngay_sinh[:2]}/{ngay_sinh[2:4]}/{ngay_sinh[4:]}'
        ngay_cap  = f'{ngay_cap[:2]}/{ngay_cap[2:4]}/{ngay_cap[4:]}'

        cmt, hc, can_cuoc, cm_khac = get_info(['CMND', 'Hộ chiếu', 'Căn cước', 'Khác'], 'Căn cước')
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
        'Nơi_sinh': dia_chi_thuong_tru,
        # 'Mã_số_thuế': ' ',
        # 'Tình_trạng_cư_trú': 'C',
        # 'Loại_GTTT': '0',
        'Số_GTTT': so_giay_to,
        'Ngày_cấp': ngay_cap,
        'Nơi_cấp': "Cục Trưởng Cục Cảnh Sát ĐKQL Cư Trú Và DLQG Về Dân Cư",
        'Nơi_ở_hiện_tại': dia_chi_thuong_tru,
        'Địa_chỉ_thường_trú': dia_chi_thuong_tru,
        'SĐT_liên_hệ': so_dien_thoai_dang_ky,
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
        user_mail = user_mail+'@viettel.com.vn'
        if check_user_pass(user_mail, pass_mail):
            file_save_name = [save_img(_img, f'cccd_{_index}.jpg', 'merge_mail') for _index, _img in enumerate(file_name)]

            # st.write(st.secrets["MA_BAO_VE"] in ma_bao_ve.lower())
            send_email(sender_email= user_mail,
                    receiver_email= user_mail,
                    password= pass_mail,
                    body= "Send email from thien1892",
                    files_attach= [*file_save_name, name_file_luu_pdf, name_file_luu])
        else:
            st.write('User hoặc pasword sai, không thể gửi mail!')
    else:
        st.write('Không thể đọc được file QR-Code')