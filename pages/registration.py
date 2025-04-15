import streamlit as st
from database import register_user

# Настройка страницы (должна быть первой командой)
st.set_page_config(page_title="Регистрация", layout="centered")

# Форма регистрации
st.title("Регистрация")
st.write("Заполните форму ниже, чтобы зарегистрироваться.")

with st.form("registration_form"):
    username = st.text_input("Имя пользователя")
    password = st.text_input("Пароль", type="password")
    confirm_password = st.text_input("Подтвердите пароль", type="password")
    
    submitted = st.form_submit_button("Зарегистрироваться")
    
    if submitted:
        if password != confirm_password:
            st.error("Пароли не совпадают.")
        elif len(username) < 3:
            st.error("Имя пользователя должно быть длиннее 3 символов.")
        else:
            success = register_user(username, password)
            if success:
                st.session_state.is_authenticated = True
                st.session_state.username = username
                st.success("Регистрация успешна! Перенаправляем на главную страницу...")
                st.switch_page("main.py")  # Переход на главную страницу
            else:
                st.error("Пользователь с таким именем уже существует.")