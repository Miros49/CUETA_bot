from sqlalchemy import Column, String, BigInteger, DECIMAL, Double, Integer, SmallInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Admin(Base):
    __tablename__ = 'admins'
    id = Column(BigInteger, primary_key=True)
    username = Column(String)


class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, unique=True)
    lolz_profile = Column(String)
    tutor = Column(String)
    status = Column(String, default="Воркер")
    nickname = Column(String)
    balance = Column(DECIMAL(10, 2), default=0.00)
    username = Column(String, unique=True, nullable=False)
    banned = Column(Integer, default=0)
    users_count = Column(Integer, default=0)
    total_turnover = Column(DECIMAL(10, 2), default=0.00)
    your_ref = Column(BigInteger, default=0)
    ref_num = Column(SmallInteger, default=0)


class Promocodes(Base):
    __tablename__ = 'promocodes'
    id = Column(BigInteger, primary_key=True, unique=True)
    num = Column(SmallInteger, nullable=False, default=0)
    promocodes = Column(String)


class Statistics(Base):
    __tablename__ = 'statistics'
    id = Column(BigInteger, primary_key=True)
    balance = Column(Double, default=0.00)
    cash_flow = Column(Double, default=0.00)
    percent = Column(Integer, default=50)
    registrations_number = Column(Integer, default=0)


class Wallets(Base):
    __tablename__ = 'wallets'
    id = Column(BigInteger, primary_key=True)
    btc = Column(String)
    eth = Column(String)
    trc20 = Column(String)
    trx = Column(String)


class Limits(Base):
    __tablename__ = 'limits'
    id = Column(BigInteger, primary_key=True)
    proxies = Column(Integer)
    numbers = Column(Integer)
