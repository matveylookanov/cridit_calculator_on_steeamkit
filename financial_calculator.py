# streamlit run app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Настройка страницы
st.set_page_config(page_title="Кредитный калькулятор", layout="wide")
st.title("Кредитный калькулятор")

# Ввод данных пользователем
st.sidebar.header("Параметры кредита")
loan_amount = st.sidebar.number_input("Сумма кредита", min_value=1000, value=1000000)
annual_interest_rate = st.sidebar.number_input("Годовая процентная ставка (%)", min_value=0.1, value=10.0)
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
    principal_payment = loan_amount / loan_term_months
    payments = []
    remaining_loan = loan_amount
    for month in range(1, loan_term_months + 1):
        interest_payment = remaining_loan * monthly_interest_rate
        total_payment = principal_payment + interest_payment
        payments.append(total_payment)
        remaining_loan -= principal_payment
    return payments

# Функция расчета простого процента
def calculate_simple_interest(loan_amount, annual_interest_rate, loan_term_years):
    total_interest = loan_amount * (annual_interest_rate / 100) * loan_term_years
    total_payment = loan_amount + total_interest
    return total_payment

# Функция расчета сложного процента
def calculate_compound_interest(loan_amount, annual_interest_rate, loan_term_years):
    total_payment = loan_amount * (1 + annual_interest_rate / 100) ** loan_term_years
    return total_payment

# Основной расчет
if payment_type == "Аннуитетный":
    monthly_payment = calculate_annuity_payment(loan_amount, monthly_interest_rate, loan_term_months)
    total_payment = monthly_payment * loan_term_months
    payments = [monthly_payment] * loan_term_months
else:  # Дифференцированный
    payments = calculate_differentiated_payment(loan_amount, monthly_interest_rate, loan_term_months)
    total_payment = sum(payments)

if interest_type == "Простой":
    total_payment_simple = calculate_simple_interest(loan_amount, annual_interest_rate, loan_term_years)
    st.write(f"Общая сумма выплат (простой процент): {total_payment_simple:.2f}")
else:  # Сложный
    total_payment_compound = calculate_compound_interest(loan_amount, annual_interest_rate, loan_term_years)
    st.write(f"Общая сумма выплат (сложный процент): {total_payment_compound:.2f}")

# Отображение результатов
st.write(f"Ежемесячный платеж: {monthly_payment:.2f}" if payment_type == "Аннуитетный" else "Ежемесячные платежи различаются.")
st.write(f"Общая сумма выплат: {total_payment:.2f}")
st.write(f"Переплата по кредиту: {total_payment - loan_amount:.2f}")

# Построение графиков
months = np.arange(1, loan_term_months + 1)
principal_payments = [loan_amount / loan_term_months] * loan_term_months if payment_type == "Дифференцированный" else [monthly_payment - loan_amount * monthly_interest_rate] * loan_term_months
interest_payments = [p - principal_payments[i] for i, p in enumerate(payments)]

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(months, principal_payments, label="Основной долг", color="blue", alpha=0.6)
ax.bar(months, interest_payments, bottom=principal_payments, label="Проценты", color="orange", alpha=0.6)
ax.set_xlabel("Месяцы")
ax.set_ylabel("Сумма выплат")
ax.set_title("График выплат по кредиту")
ax.legend()
st.pyplot(fig)

# Дополнительные графики (например, накопленные выплаты)
cumulative_payments = np.cumsum(payments)
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(months, cumulative_payments, label="Накопленные выплаты", color="green")
ax2.axhline(y=loan_amount, color="red", linestyle="--", label="Сумма кредита")
ax2.set_xlabel("Месяцы")
ax2.set_ylabel("Накопленная сумма")
ax2.set_title("Накопленные выплаты по кредиту")
ax2.legend()
st.pyplot(fig2)