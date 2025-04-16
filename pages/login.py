import streamlit as st
from database import authenticate_user, activate_session

# Настройка страницы
st.set_page_config(page_title="Вход", layout="centered")

# Форма входа
st.title("Вход")
st.write("Введите свои данные для входа.")

with st.form("login_form"):
    username = st.text_input("Имя пользователя")
    password = st.text_input("Пароль", type="password")
    
    submitted = st.form_submit_button("Войти")
    
    if submitted:
        if authenticate_user(username, password):
            activate_session(username)  # Активируем сессию
            st.session_state.is_authenticated = True
            st.session_state.username = username  # Сохраняем имя пользователя
            st.success("Вход выполнен успешно! Перенаправляем на главную страницу...")
            st.switch_page("main.py")  # Переход на главную страницу
        else:
            st.error("Неверное имя пользователя или пароль.")

# Кнопка "Зарегистрироваться" внизу страницы
if st.button("Нет аккаунта? Зарегистрироваться"):
    st.switch_page("pages/registration.py")