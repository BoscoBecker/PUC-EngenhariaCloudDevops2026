from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy import Column, Integer, String, datetime
from app import BaseModel, DB


class Book(BaseModel):
    __tablename__ = 'books'

    id: Mapped[int] = Column(Integer, primary_key=True)
    title: Mapped[str] = Column(String(256), nullable=False)
    author: Mapped[str] = Column(String(256), nullable=False)
    issn: Mapped[str] = Column(String(16), nullable=False)
    date_published: Mapped[datetime] = Column(String(10), nullable=False)
    pages: Mapped[int] = Column(Integer, nullable=False)
    def __str__(self):
        return f"Book(id={self.id}, title='{self.title}', author='{self.author}', issn='{self.issn}', date_published='{self.date_published}', pages={self.pages})"