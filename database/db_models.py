from sqlalchemy import (
    Column,
    String,
    Integer,
    BigInteger,
    Date,
    Boolean,
    Numeric,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String, unique=True)
    name = Column(String)
    date_of_birth = Column(Date)
    status = Column(String)
    phone_number = Column(String)
    balance = Column(Numeric(10, 2), default=0)


class Event(Base):
    __tablename__ = "events"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    description = Column(String)
    date = Column(Date)
    photo_id = Column(String)


class Registration(Base):
    __tablename__ = "registrations"

    id = Column(BigInteger, primary_key=True)
    event_id = Column(BigInteger, ForeignKey("events.id"))

    user_id = Column(BigInteger, ForeignKey("users.id"))
    username = Column(String)

    registration_wave = Column(Integer, nullable=False)
    registration_type = Column(String, nullable=False)
    fundraiser_id = Column(BigInteger)  # ForeignKey('fundraisers.id')
    split = Column(Boolean, default=False)
    status = Column(String, nullable=False)
    first_warning = Column(Date)


class FundRaiser(Base):
    __tablename__ = "fundraisers"

    id = Column(BigInteger, primary_key=True)
    username = Column(String, unique=True)
    status = Column(Boolean, nullable=False)
    phone_number = Column(String, nullable=False)
    preferred_bank = Column(String, nullable=False)

    number_of_registrations = Column(Integer, nullable=False, default=0)
    waiting_for_verification = Column(Integer, nullable=False, default=0)
    verified = Column(Integer, nullable=False, default=0)

    pending_transactions = Column(Integer, nullable=False, default=0)
    transactions_to_confirm = Column(Integer, nullable=False, default=0)
    confirmed_transactions = Column(Integer, nullable=False, default=0)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String, nullable=False, default="RUB")
    coins_amount = Column(Integer, nullable=False)

    fundraiser_id = Column(BigInteger, ForeignKey("fundraisers.id"), nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


# class BeerPongTeam(Base):
#     __tablename__ = 'beer_pong'
#
#     id = Column(BigInteger, primary_key=True)
#
#     player_1_id = Column(BigInteger, ForeignKey('users.id'))
#     player_1_username = Column(String)
#
#     player_2_id = Column(BigInteger, ForeignKey('users.id'))
#     player_2_username = Column(String)
#
#     status = Column(Boolean)
#     created_manually = Column(Boolean)
