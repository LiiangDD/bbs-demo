import time

from sqlalchemy import Unicode, Column

from models.base_model import db, SQLMixin, SQLBase


class Board(SQLMixin, SQLBase):
    __tablename__ = 'Board'
    title = Column(Unicode(50), nullable=False)
