import time

from sqlalchemy import String, Column, Integer, UnicodeText

from models import Model
from models.base_model import SQLMixin, SQLBase
from models.user import User


class Reply(SQLMixin, SQLBase):
    __tablename__ = 'Reply'
    content = Column(UnicodeText, nullable=False)
    topic_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    def user(self):
        u = User.one(id=self.user_id)
        return u

    @classmethod
    def new(cls, form, user_id):
        form['user_id'] = user_id
        m = super().new(**form)
        return m
