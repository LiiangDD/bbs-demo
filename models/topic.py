import time

from sqlalchemy import String, Integer, Column, Text, UnicodeText, Unicode, desc

from models.base_model import SQLMixin, SQLBase
from models.user import User
from models.reply import Reply


class Topic(SQLMixin, SQLBase):
    __tablename__ = 'Topic'
    views = Column(Integer, nullable=False, default=0)
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    user_id = Column(Integer, nullable=False)
    board_id = Column(Integer, nullable=False)

    @classmethod
    def new(cls, form, user_id):
        form['user_id'] = user_id
        m = super().new(**form)
        return m

    @classmethod
    def get(cls, id):
        m = cls.one(id=id)
        m.views += 1
        m.save()
        return m

    def user(self):
        u = User.one(id=self.user_id)
        return u

    def replies(self):
        ms = Reply.all(topic_id=self.id)
        return ms

    def reply_count(self):
        count = len(self.replies())
        return count

    # 改写继承的父类方法 按时间倒序获取topic数组
    @classmethod
    def all(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).order_by(desc(cls.created_time)).all()
        return ms
