import pathlib


class config:
    APP_DIR = pathlib.Path(__file__).parent.absolute()
    PROJECT_DIR = APP_DIR.parent.absolute()
    # file goc merge mail
    FILE_GOC = ['merge_mail/IMPOT_CHAN_CHAN_fix.xls', 
                'merge_mail/IMPOT_CHAN_CHAN_new.xls',
                'merge_mail/HO_SO_NO_PL_PY.docx',
                'merge_mail/HO_SO_PL_PY.docx']
    # image to give coffee
    IMAGE_COFFEE = "https://i.imgur.com/DMb19zW.jpg"
    # time to save file, after to delete
    TIME_TO_SAVE_FILE = 3.0
    # path file goc
    PATH_FILE_MAU = "merge_mail/IMPOT_CHAN_CHAN_fix.xls"
    PATH_FILE_MAU_NEW = "merge_mail/IMPOT_CHAN_CHAN_new.xls"
    PATH_FILE_WORD = "merge_mail/HO_SO_PL_PY.docx"
    PATH_FILE_WORD_NOPL = "merge_mail/HO_SO_NO_PL_PY.docx"

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

    GIOI_TINH = {
        '1': 'Nữ',
        '0': 'Nam'
    }

    TINH_TRANG_CU_TRU = {
        'C':'Cư trú', 
        'K':'Không cư trú'
    }

    GIAY_TO_TUY_THAN = {
        '0':'CMND',
        '1':'Hộ chiếu',
        '6':'Căn cước',
        '2':'Khác',
        '9':'Khác'
    }

    TINH_TRANG_HON_NHAN = {
        'DT':'Độc thân', 
        'DKH':'Đã kết hôn', 
        'KHAC':'Khác'
    }


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

