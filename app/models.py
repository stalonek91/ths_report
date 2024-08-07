from app.database import Base

from sqlalchemy.sql.expression import text
from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime, Date, Numeric


class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    receiver = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_type = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    ref_number = Column(String(100), nullable=False, unique=True)


class Etoro(Base):

    __tablename__ = "etoro"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    initial_amount = Column(Numeric(10, 2), nullable=False)
    deposit_amount = Column(Numeric(10, 2), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    growth_percentage = Column(Numeric(5, 2), nullable=True)

class Xtb(Base):

    __tablename__ = "xtb"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    initial_amount = Column(Numeric(10, 2), nullable=False)
    deposit_amount = Column(Numeric(10, 2), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    growth_percentage = Column(Numeric(5, 2), nullable=True)


class Vienna(Base):

    __tablename__ = "vienna"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    initial_amount = Column(Numeric(10, 2), nullable=False)
    deposit_amount = Column(Numeric(10, 2), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    growth_percentage = Column(Numeric(5, 2), nullable=True)

class Revolut(Base):

    __tablename__ = "revolut"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    initial_amount = Column(Numeric(10, 2), nullable=False)
    deposit_amount = Column(Numeric(10, 2), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    growth_percentage = Column(Numeric(5, 2), nullable=True)

class Obligacje(Base):

    __tablename__ = "obligacje"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    initial_amount = Column(Numeric(10, 2), nullable=False)
    deposit_amount = Column(Numeric(10, 2), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    growth_percentage = Column(Numeric(5, 2), nullable=True)


class Generali(Base):

    __tablename__ = "generali"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    initial_amount = Column(Numeric(10, 2), nullable=False)
    deposit_amount = Column(Numeric(10, 2), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    growth_percentage = Column(Numeric(5, 2), nullable=True)

class Nokia(Base):

    __tablename__ = "nokia"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    initial_amount = Column(Numeric(10, 2), nullable=False)
    deposit_amount = Column(Numeric(10, 2), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    growth_percentage = Column(Numeric(5, 2), nullable=True)


class PortfolioSummary(Base):
    
    __tablename__ = "portfolio"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    sum_of_acc = Column(Numeric(10, 2), nullable=False)
    last_update_profit = Column(Numeric(10, 2), nullable=False)
    sum_of_deposits = Column(Numeric(10, 2), nullable=False)
    all_time_profit = Column(Numeric(10, 2), nullable=False)
    
