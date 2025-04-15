import streamlit as st

# Настройка страницы (должна быть первой командой)
st.set_page_config(page_title="Профиль", layout="centered")

# Проверка аутентификации
if not st.session_state.get("is_authenticated", False):
    st.warning("Вы не авторизованы. Пожалуйста, войдите.")
    st.stop()

# Основной контент страницы профиля
st.title(f"Профиль пользователя: {st.session_state.username}")
st.write("Здесь вы можете управлять своими данными.")

if st.button("Выйти"):
    st.session_state.is_authenticated = False
    st.session_state.username = None
    st.experimental_rerun()