from sqlalchemy import Column, String, BigInteger, Date, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# class Admin(Base):
#     __tablename__ = 'admins'
#     id = Column(BigInteger, primary_key=True)
#     username = Column(String)


class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    name = Column(String)
    date_of_birth = Column(Date)
    status = Column(String)
    phone_number = Column(String)
    allow_notifications = Column(Boolean, default=True)


class Event(Base):
    __tablename__ = 'events'
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    description = Column(String)
    date = Column(Date)


class Registration(Base):
    __tablename__ = 'registrations'
    id = Column(BigInteger, primary_key=True)
    event_id = Column(BigInteger, ForeignKey('events.id'))
    user = Column(BigInteger, ForeignKey('users.id'))
