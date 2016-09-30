from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from . import app
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
import datetime
from flask.ext.login import UserMixin

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base, UserMixin):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(128))
    last_name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))
    datetime_created = Column(DateTime, default=datetime.datetime.now)
    
    notifications = relationship("Notification", backref="user")
    contacts = relationship("Contact", backref="user", lazy="dynamic")
    
class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True)
    subject = Column(String(128))
    timezone = Column(String(128))
    frequency = Column(String(128))
    days = Column(String(128))
    status = Column(String(128))
    datetime_created = Column(DateTime, default=datetime.datetime.now)
    
    user_id = Column(Integer, ForeignKey('users.id'))

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True)
    number1 = Column(String(128))
    number2 = Column(String(128))
    datetime_created = Column(DateTime, default=datetime.datetime.now)

    user_id = Column(Integer, ForeignKey('users.id'))

#all classes before this line
Base.metadata.create_all(engine)