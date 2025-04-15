import pytest
from database import register_user, authenticate_user, SessionLocal, User
from pages.calculator import calculate_annuity_payment, calculate_differentiated_payment

# Фикстура для очистки базы данных перед каждым тестом
@pytest.fixture(autouse=True)
def clear_database():
    """Очищает базу данных перед каждым тестом."""
    db = SessionLocal()
    db.query(User).delete()
    db.commit()
    db.close()

# Фикстура для регистрации тестового пользователя
@pytest.fixture
def test_user():
    """Создает тестового пользователя."""
    username = "testuser"
    password = "password123"
    register_user(username, password)
    return {"username": username, "password": password}

# Тесты для регистрации и аутентификации
def test_register_user_success():
    """Тест успешной регистрации нового пользователя."""
    assert register_user("newuser", "password123") is True

def test_register_user_duplicate(test_user):
    """Тест попытки регистрации с уже существующим именем пользователя."""
    assert register_user(test_user["username"], "password123") is False

def test_authenticate_user_success(test_user):
    """Тест успешного входа."""
    assert authenticate_user(test_user["username"], test_user["password"]) is True

def test_authenticate_user_failure(test_user):
    """Тест неудачного входа (неверные данные)."""
    assert authenticate_user(test_user["username"], "wrongpassword") is False
    assert authenticate_user("nonexistentuser", "password123") is False

# Параметризация для тестов кредитного калькулятора
@pytest.mark.parametrize(
    "loan_amount, annual_interest_rate, loan_term_years, expected_payment",
    [
        (1000000, 10, 1, 87915.89),  # Аннуитетный платеж за 1 год
        (1000000, 10, 5, 21247.04),  # Аннуитетный платеж за 5 лет
        (1000000, 5, 10, 10606.55),  # Аннуитетный платеж за 10 лет с низкой ставкой
    ]
)
def test_calculate_annuity_payment(loan_amount, annual_interest_rate, loan_term_years, expected_payment):
    """Тест расчета аннуитетного платежа."""
    monthly_interest_rate = annual_interest_rate / 100 / 12
    loan_term_months = loan_term_years * 12
    payment = calculate_annuity_payment(loan_amount, monthly_interest_rate, loan_term_months)
    assert round(payment, 2) == expected_payment

@pytest.mark.parametrize(
    "loan_amount, annual_interest_rate, loan_term_years, first_payment, last_payment",
    [
        (1000000, 10, 1, 91666.67, 84027.78),  # Первый и последний платеж за 1 год
        (1000000, 10, 5, 25000.0, 16805.56),  # Первый и последний платеж за 5 лет
    ]
)
def test_calculate_differentiated_payment(loan_amount, annual_interest_rate, loan_term_years, first_payment, last_payment):
    """Тест расчета дифференцированного платежа."""
    monthly_interest_rate = annual_interest_rate / 100 / 12
    loan_term_months = loan_term_years * 12
    payments = calculate_differentiated_payment(loan_amount, monthly_interest_rate, loan_term_months)
    assert round(payments[0], 2) == first_payment
    assert round(payments[-1], 2) == last_payment

@pytest.mark.parametrize(
    "loan_amount, annual_interest_rate, loan_term_years, expected_overpayment",
    [
        (1000000, 10, 1, 54990.65),  # Переплата за 1 год
        (1000000, 10, 5, 274822.68),  # Переплата за 5 лет
    ]
)
def test_calculate_overpayment(loan_amount, annual_interest_rate, loan_term_years, expected_overpayment):
    """Тест расчета переплаты."""
    monthly_interest_rate = annual_interest_rate / 100 / 12
    loan_term_months = loan_term_years * 12
    annuity_payment = calculate_annuity_payment(loan_amount, monthly_interest_rate, loan_term_months)
    total_payment = annuity_payment * loan_term_months
    overpayment = total_payment - loan_amount
    assert round(overpayment, 2) == expected_overpayment