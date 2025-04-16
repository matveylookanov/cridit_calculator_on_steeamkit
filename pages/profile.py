import streamlit as st
from database import is_authenticated, get_user_calculations

# Настройка страницы
st.set_page_config(page_title="Профиль", layout="wide")

# Проверка аутентификации
authenticated, username = is_authenticated()
if not authenticated:
    st.warning("Вы не авторизованы. Пожалуйста, войдите.")
    st.stop()

# Заголовок
st.title(f"Профиль пользователя: {username}")

# Получение расчетов пользователя
calculations = get_user_calculations(username)

if not calculations:
    st.info("У вас пока нет сохраненных расчетов.")
else:
    st.subheader("Сохраненные расчеты:")
    for calc in calculations:
        st.write(f"""
        - **Сумма кредита**: {calc.loan_amount:.2f}
        - **Ставка**: {calc.annual_interest_rate}%
        - **Срок**: {calc.loan_term_years} лет
        - **Тип платежей**: {calc.payment_type}
        - **Общая сумма выплат**: {calc.total_payment:.2f}
        - **Переплата**: {calc.total_interest_paid:.2f}
        - [Посмотреть расчет]({calc.unique_link})
        """)
if st.button("Выйти"):
    st.session_state.is_authenticated = False
    st.session_state.username = None
    st.experimental_rerun()