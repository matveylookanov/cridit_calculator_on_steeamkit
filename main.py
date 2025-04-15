import streamlit as st

# Настройка страницы
st.set_page_config(
    page_title="Кредитный калькулятор",
    layout="wide"
)

# Инициализация состояния пользователя
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Функция для выхода
def logout():
    st.session_state.is_authenticated = False
    st.session_state.username = None

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
    if st.button("Перейти к калькулятору"):
        st.switch_page("pages/calculator.py")
else:
    st.write("Пожалуйста, войдите или зарегистрируйтесь, чтобы использовать все функции.")