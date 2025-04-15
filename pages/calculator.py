import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Настройка страницы (должна быть первой командой)
st.set_page_config(page_title="Кредитный калькулятор", layout="wide")

# Проверка аутентификации
if not st.session_state.get("is_authenticated", False):
    st.warning("Вы не авторизованы. Пожалуйста, войдите.")
    st.stop()

# Ввод данных пользователем
st.title("Кредитный калькулятор")
st.sidebar.header("Параметры кредита")
loan_amount = st.sidebar.number_input("Сумма кредита", min_value=1000, value=1000000)
annual_interest_rate = st.sidebar.slider(
    "Годовая процентная ставка (%)",
    min_value=0.1,
    max_value=50.0,
    value=10.0,
    step=0.1
)
loan_term_years = st.sidebar.number_input("Срок кредита (в годах)", min_value=1, value=5)
payment_type = st.sidebar.selectbox("Тип платежей", ["Аннуитетный", "Дифференцированный"])
interest_type = st.sidebar.selectbox("Тип процентов", ["Простой", "Сложный"])

# Преобразование годовой ставки в месячную
monthly_interest_rate = annual_interest_rate / 100 / 12
loan_term_months = loan_term_years * 12

# Функция расчета аннуитетного платежа
def calculate_annuity_payment(loan_amount, monthly_interest_rate, loan_term_months):
    if monthly_interest_rate == 0:
        return loan_amount / loan_term_months
    annuity_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months) / ((1 + monthly_interest_rate) ** loan_term_months - 1)
    return annuity_payment

# Функция расчета дифференцированного платежа
def calculate_differentiated_payment(loan_amount, monthly_interest_rate, loan_term_months):
    # Расчет основного долга за месяц
    principal_payment = loan_amount / loan_term_months
    payments = []
    remaining_loan = loan_amount

    for month in range(1, loan_term_months + 1):
        # Расчет процентов за текущий месяц
        interest_payment = remaining_loan * monthly_interest_rate
        # Общий платеж за месяц
        total_payment = principal_payment + interest_payment
        # Добавляем платеж в список
        payments.append(total_payment)
        # Уменьшаем остаток кредита
        remaining_loan -= principal_payment

    return payments

# Основной расчет
if payment_type == "Аннуитетный":
    monthly_payment = calculate_annuity_payment(loan_amount, monthly_interest_rate, loan_term_months)
    total_payment = monthly_payment * loan_term_months
    payments = [monthly_payment] * loan_term_months
else:  # Дифференцированный
    payments = calculate_differentiated_payment(loan_amount, monthly_interest_rate, loan_term_months)
    total_payment = sum(payments)

# Расчет переплаты
total_interest_paid = total_payment - loan_amount

# Отображение результатов
st.write(f"Ежемесячный платеж: {monthly_payment:.2f}" if payment_type == "Аннуитетный" else "Ежемесячные платежи различаются.")
st.write(f"Общая сумма выплат: {total_payment:.2f}")
st.write(f"Переплата по кредиту: {total_interest_paid:.2f}")

# Круговая диаграмма
labels = ["Основной долг", "Проценты"]
sizes = [loan_amount, total_interest_paid]
colors = ["#4682B4", "#FFA07A"]  # Синий и оранжевый
explode = (0.1, 0)  # Выделение первого сегмента

fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
ax_pie.pie(
    sizes,
    explode=explode,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors,
    shadow=True,
    wedgeprops={"edgecolor": "white"}
)
ax_pie.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
st.subheader("Распределение выплат")
st.pyplot(fig_pie)

# Таблица с распределением выплат
months = np.arange(1, loan_term_months + 1)
principal_payments = [loan_amount / loan_term_months] * loan_term_months if payment_type == "Дифференцированный" else [monthly_payment - loan_amount * monthly_interest_rate] * loan_term_months
interest_payments = [p - principal_payments[i] for i, p in enumerate(payments)]

data = {
    "Месяц": months,
    "Основной долг": principal_payments,
    "Проценты": interest_payments,
    "Итого выплата": payments
}
df = pd.DataFrame(data)
st.subheader("Ежемесячные выплаты")
st.dataframe(df.style.format({
    "Основной долг": "{:.2f}",
    "Проценты": "{:.2f}",
    "Итого выплата": "{:.2f}"
}))

# График ежемесячных выплат
fig_payments, ax_payments = plt.subplots(figsize=(10, 6))
ax_payments.bar(months, principal_payments, label="Основной долг", color="#4682B4", alpha=0.6)
ax_payments.bar(months, interest_payments, bottom=principal_payments, label="Проценты", color="#FFA07A", alpha=0.6)
ax_payments.set_xlabel("Месяцы")
ax_payments.set_ylabel("Сумма выплат")
ax_payments.set_title("Ежемесячные выплаты по кредиту")
ax_payments.legend()
st.subheader("График ежемесячных выплат")
st.pyplot(fig_payments)

# График накопленных выплат
cumulative_payments = np.cumsum(payments)
fig_cumulative, ax_cumulative = plt.subplots(figsize=(10, 6))
ax_cumulative.plot(months, cumulative_payments, label="Накопленные выплаты", color="green")
ax_cumulative.axhline(y=loan_amount, color="red", linestyle="--", label="Сумма кредита")
ax_cumulative.set_xlabel("Месяцы")
ax_cumulative.set_ylabel("Накопленная сумма")
ax_cumulative.set_title("Накопленные выплаты по кредиту")
ax_cumulative.legend()
st.subheader("График накопленных выплат")
st.pyplot(fig_cumulative)