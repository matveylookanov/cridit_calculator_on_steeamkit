from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

# Модель для хранения расчетов
# Настройка базы данных SQLite
DATABASE_URL = "sqlite:///users.db"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
class Calculation(Base):
    __tablename__ = "calculations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # Связь с пользователем
    loan_amount = Column(Float)  # Сумма кредита
    annual_interest_rate = Column(Float)  # Годовая процентная ставка
    loan_term_years = Column(Integer)  # Срок кредита (в годах)
    payment_type = Column(String)  # Тип платежей
    total_payment = Column(Float)  # Общая сумма выплат
    total_interest_paid = Column(Float)  # Переплата по кредиту
    unique_link = Column(String, unique=True)  # Уникальная ссылка на расчет

    user = relationship("User", back_populates="calculations")


# Модель пользователя
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

# Добавляем связь между User и Calculation
User.calculations = relationship("Calculation", order_by=Calculation.id, back_populates="user")
# Модель сессии
class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=False)

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Создание сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для регистрации пользователя
def register_user(username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if user:
        return False  # Пользователь уже существует
    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return True

# Функция для аутентификации пользователя
def authenticate_user(username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if user and user.password == password:
        return True
    return False

# Функция для активации сессии
def activate_session(username):
    db = SessionLocal()
    session = db.query(Session).filter(Session.username == username).first()
    if not session:
        session = Session(username=username, is_active=True)
        db.add(session)
    else:
        session.is_active = True
    db.commit()
    db.close()

# Функция для деактивации сессии
def deactivate_session(username):
    db = SessionLocal()
    session = db.query(Session).filter(Session.username == username).first()
    if session:
        session.is_active = False
        db.commit()
    db.close()

# Функция для проверки состояния авторизации
def is_authenticated():
    db = SessionLocal()
    active_session = db.query(Session).filter(Session.is_active == True).first()
    db.close()
    return active_session is not None, getattr(active_session, "username", None)

import uuid

# Функция для сохранения расчета
def save_calculation(username, loan_amount, annual_interest_rate, loan_term_years, payment_type, total_payment, total_interest_paid):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if not user:
        db.close()
        return False

    unique_link = str(uuid.uuid4())  # Генерация уникальной ссылки
    calculation = Calculation(
        user_id=user.id,
        loan_amount=loan_amount,
        annual_interest_rate=annual_interest_rate,
        loan_term_years=loan_term_years,
        payment_type=payment_type,
        total_payment=total_payment,
        total_interest_paid=total_interest_paid,
        unique_link=unique_link
    )
    db.add(calculation)
    db.commit()
    db.refresh(calculation)
    db.close()
    return unique_link

# Функция для получения всех расчетов пользователя
def get_user_calculations(username):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if not user:
        db.close()
        return []
    calculations = user.calculations
    db.close()
    return calculations

# Функция для получения расчета по ссылке
def get_calculation_by_link(unique_link):
    db = SessionLocal()
    calculation = db.query(Calculation).filter(Calculation.unique_link == unique_link).first()
    db.close()
    return calculation