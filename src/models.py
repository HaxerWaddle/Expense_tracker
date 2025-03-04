from sqlalchemy import ForeignKey, Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship, Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from typing import List

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

class USER(Base, UserMixin):
    __tablename__ = 'user_table'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    expenses: Mapped[List["EXPENSE"]] = relationship(back_populates='user')

    def __repr__(self):
        return f'USER(id={self.id!r}, username={self.username!r}, password={self.password!r})'

class EXPENSE(Base):
    __tablename__ = 'expense_table'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    info: Mapped[str] = mapped_column(String(100), nullable=False)
    time: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_table.id'))
    user: Mapped['USER'] = relationship(back_populates='expenses')

    def __repr__(self):
        return f'EXPENSE(id={self.id!r}, user_id={self.user_id!r}, name={self.name!r}, info={self.name!r})'