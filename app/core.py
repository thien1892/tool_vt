import streamlit as st
from CONFIG.config import config
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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


def chuyen_khong_dau(text_):
    text_ = text_.strip()
    text_ = text_.upper()
    text_ = text_[:23]
    # print(len(text_))
    text_ = text_ + ' '*(23 - len(text_))
    split_text = [i if i not in config.DICT_KHONG_DAU.keys() else config.DICT_KHONG_DAU[i] for i in text_]

    return split_text

def get_info(list_choice, choice):
    b = len(list_choice)* [config.BT_KHONG]
    b[list_choice.index(choice)] = config.BT_CO
    return b

def send_email(sender_email: str, 
               receiver_email: str,
               password: str,
               body: str,
               files_attach: list,
               ):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Bcc"] = receiver_email

    msg.attach(MIMEText(body, "plain"))
    for _file in files_attach:
        with open(_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())  
        encoders.encode_base64(part)
        name_file = _file.split('/')[-1]
        part.add_header('content-disposition', 'attachment', filename=f'{name_file}')
        msg.attach(part)
    
    msg["Subject"] = name_file.split('.')[0]


    _text = msg.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.viettel.com.vn", 465, context = context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, _text)
    st.write("Đã gửi mail thành công, vui lòng check email!")