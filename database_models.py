from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from datetime import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    default_city = Column(String, nullable=False, server_default="Karachi")

    posts = relationship("Weather", back_populates="assigned_user", cascade="all, delete-orphan")


class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=False)
    current_temp = Column(Float, nullable=False)
    feels_like = Column(Float, nullable=False)
    minimum_temp = Column(Float, nullable=False)
    maximum_temp = Column(Float, nullable=False)
    checked_at = Column(DateTime, default=datetime.utcnow)
    

    user_id = Column(Integer, ForeignKey("users.id"))
    assigned_user = relationship("User", back_populates="posts")










