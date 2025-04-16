import streamlit as st
from database import is_authenticated, deactivate_session

# Настройка страницы
st.set_page_config(
    page_title="Кредитный калькулятор",
    layout="wide"
)

# Инициализация состояния пользователя
if 'is_authenticated' not in st.session_state:
    authenticated, username = is_authenticated()
    st.session_state.is_authenticated = authenticated
    st.session_state.username = username  # Инициализация имени пользователя

# Функция для выхода
def logout():
    deactivate_session(st.session_state.username)
    st.session_state.is_authenticated = False
    st.session_state.username = None  # Очищаем имя пользователя

# Размещение кнопок в правом верхнем углу
col1, col2, col3 = st.columns([7, 1, 1])  # col1 - основное пространство, col2 и col3 - кнопки
with col2:
    if st.session_state.is_authenticated:
        if st.button("Выход"):
            logout()
with col3:
    if not st.session_state.is_authenticated:
        if st.button("Регистрация"):
            st.switch_page("pages/registration.py")
        if st.button("Вход"):
            st.switch_page("pages/login.py")

# Основной контент главной страницы
st.title("Добро пожаловать в кредитный калькулятор!")
if st.session_state.is_authenticated:
    st.write(f"Привет, {st.session_state.username}!")
else:
    st.write("Пожалуйста, войдите или зарегистрируйтесь, чтобы использовать все функции.")