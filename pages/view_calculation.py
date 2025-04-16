import streamlit as st
from database import get_calculation_by_link

# Настройка страницы
st.set_page_config(page_title="Просмотр расчета", layout="wide")

# Получение уникальной ссылки из URL
query_params = st.experimental_get_query_params()
unique_link = query_params.get("link", [None])[0]

if not unique_link:
    st.warning("Неверная ссылка. Расчет не найден.")
    st.stop()

# Получение расчета по ссылке
calculation = get_calculation_by_link(unique_link)
if not calculation:
    st.warning("Расчет не найден.")
    st.stop()

# Отображение расчета
st.title("Просмотр расчета")
st.write(f"- **Сумма кредита**: {calculation.loan_amount:.2f}")
st.write(f"- **Ставка**: {calculation.annual_interest_rate}%")
st.write(f"- **Срок**: {calculation.loan_term_years} лет")
st.write(f"- **Тип платежей**: {calculation.payment_type}")
st.write(f"- **Общая сумма выплат**: {calculation.total_payment:.2f}")
st.write(f"- **Переплата**: {calculation.total_interest_paid:.2f}")