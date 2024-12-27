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
    username = Column(String, unique=True)
    name = Column(String)
    date_of_birth = Column(Date)
    status = Column(String)
    phone_number = Column(String)


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
    user_id = Column(BigInteger, ForeignKey('users.id'))


class BeerPongTeam(Base):
    __tablename__ = 'beer_pong'
    id = Column(BigInteger, primary_key=True)
    player_1_id = Column(BigInteger, ForeignKey('users.id'))
    player_1_username = Column(String, ForeignKey('users.username'))
    player_2_id = Column(BigInteger, ForeignKey('users.id'))
    player_2_username = Column(String, ForeignKey('users.username'))
    status = Column(Boolean)
    created_manually = Column(Boolean)
