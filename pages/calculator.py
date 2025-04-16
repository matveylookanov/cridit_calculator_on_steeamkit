import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from database import is_authenticated
from database import save_calculation

# Настройка страницы (должна быть первой командой)
st.set_page_config(page_title="Кредитный калькулятор", layout="wide")

# Проверка аутентификации
authenticated, username = is_authenticated()
if not authenticated:
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
    step=0.5
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

# Создание таблицы с детализацией выплат
months = np.arange(1, loan_term_months + 1)
remaining_loan = loan_amount
table_data = []

for month in range(1, loan_term_months + 1):
    if payment_type == "Аннуитетный":
        interest_payment = remaining_loan * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
    else:  # Дифференцированный
        principal_payment = loan_amount / loan_term_months
        interest_payment = remaining_loan * monthly_interest_rate
    
    # Обновление остатка долга
    remaining_loan -= principal_payment
    table_data.append({
        "Месяц": month,
        "Платеж": round(monthly_payment, 2) if payment_type == "Аннуитетный" else round(payments[month - 1], 2),
        "Остаток долга": round(max(remaining_loan, 0), 2),  # Защита от отрицательных значений
        "Проценты": round(interest_payment, 2),
        "Тело кредита": round(principal_payment, 2)
    })

# Преобразование данных в DataFrame
df = pd.DataFrame(table_data)


# Отображение результатов
st.write(f"Ежемесячный платеж: {monthly_payment:.2f}" if payment_type == "Аннуитетный" else "Ежемесячные платежи различаются.")
st.write(f"Общая сумма выплат: {total_payment:.2f}")
st.write(f"Переплата по кредиту: {total_interest_paid:.2f}")

# Кнопка для сохранения расчета
if st.button("Сохранить расчет"):
    unique_link = save_calculation(
        username=st.session_state.username,
        loan_amount=loan_amount,
        annual_interest_rate=annual_interest_rate,
        loan_term_years=loan_term_years,
        payment_type=payment_type,
        total_payment=total_payment,
        total_interest_paid=total_interest_paid
    )
    if unique_link:
        st.success(f"Расчет сохранен! Поделитесь ссылкой: {unique_link}")
    else:
        st.error("Не удалось сохранить расчет.")


# Круговая диаграмма (уменьшенный размер и шрифт)
labels = ["Основной долг", "Проценты"]
sizes = [loan_amount, total_interest_paid]
colors = ["#4682B4", "#FFA07A"]  # Синий и оранжевый
explode = (0.1, 0)  # Выделение первого сегмента

fig_pie, ax_pie = plt.subplots(figsize=(3, 3))  # Уменьшенный размер
ax_pie.pie(
    sizes,
    explode=explode,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors,
    shadow=True,
    wedgeprops={"edgecolor": "white"},
    textprops={'fontsize': 6}  # Уменьшенный размер шрифта текста
)
ax_pie.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
ax_pie.set_title("Распределение выплат", fontsize=8)  # Уменьшенный размер шрифта заголовка
st.subheader("Распределение выплат")
st.pyplot(fig_pie)

# Таблица с распределением выплат
st.subheader("Детализация выплат")
st.dataframe(df.style.format({
    "Платеж": "{:.2f}",
    "Остаток долга": "{:.2f}",
    "Проценты": "{:.2f}",
    "Тело кредита": "{:.2f}"
}))

# График ежемесячных выплат (уменьшенный размер и шрифт)
fig_payments, ax_payments = plt.subplots(figsize=(5, 3))  # Уменьшенный размер
principal_payments = df["Тело кредита"].values
interest_payments = df["Проценты"].values
months = df["Месяц"].values

ax_payments.bar(months, principal_payments, label="Тело кредита", color="#4682B4", alpha=0.6)
ax_payments.bar(months, interest_payments, bottom=principal_payments, label="Проценты", color="#FFA07A", alpha=0.6)
ax_payments.set_xlabel("Месяцы", fontsize=6)  # Уменьшенный размер шрифта метки оси X
ax_payments.set_ylabel("Сумма выплат", fontsize=6)  # Уменьшенный размер шрифта метки оси Y
ax_payments.set_title("Ежемесячные выплаты по кредиту", fontsize=8)  # Уменьшенный размер шрифта заголовка
ax_payments.legend(fontsize=6)  # Уменьшенный размер шрифта легенды
st.subheader("График ежемесячных выплат")
st.pyplot(fig_payments)

# График накопленных выплат (уменьшенный размер и шрифт)
cumulative_payments = np.cumsum(df["Платеж"].values)
fig_cumulative, ax_cumulative = plt.subplots(figsize=(5, 3))  # Уменьшенный размер
ax_cumulative.plot(months, cumulative_payments, label="Накопленные выплаты", color="green")
ax_cumulative.axhline(y=loan_amount, color="red", linestyle="--", label="Сумма кредита")
ax_cumulative.set_xlabel("Месяцы", fontsize=6)  # Уменьшенный размер шрифта метки оси X
ax_cumulative.set_ylabel("Накопленная сумма", fontsize=6)  # Уменьшенный размер шрифта метки оси Y
ax_cumulative.set_title("Накопленные выплаты по кредиту", fontsize=8)  # Уменьшенный размер шрифта заголовка
ax_cumulative.legend(fontsize=6)  # Уменьшенный размер шрифта легенды
st.subheader("График накопленных выплат")
st.pyplot(fig_cumulative)