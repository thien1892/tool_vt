import streamlit as st
from CONFIG.config import config

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