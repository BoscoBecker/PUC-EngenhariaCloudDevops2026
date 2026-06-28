from sqlalchemy.orm import Mapped
from sqlalchemy import Column, Integer, String, DateTime
from db import BaseModel
from flask_login import UserMixin

class User(BaseModel,UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = Column(String(256), nullable=False)
    email: Mapped[str] = Column(String(256), nullable=False)
    password: Mapped[str] = Column(String(256), nullable=False)
    date_joined: Mapped[DateTime] = Column(DateTime, nullable=False)

    def __str__(self):
        return f"User(id={self.id}, username='{self.username}', email='{self.email}', date_joined='{self.date_joined}')"