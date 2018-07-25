import hashlib

from sqlalchemy import Column, String, Text, Enum

import secret
from models.base_model import SQLMixin, SQLBase
from models.user_role import UserRole


class User(SQLMixin, SQLBase):
    __tablename__ = 'User'
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    image = Column(String(100), nullable=False, default='/images/biu.gif')
    signature = Column(String(100), nullable=False, default='这家伙很懒，什么个性签名都没有留下。')
    email = Column(String(50), nullable=False, default=secret.test_mail)
    user_role = Column(Enum(UserRole), nullable=False, default=UserRole.normal)

    # content = Column(Text, nullable=False)

    def add_default_value(self):
        super().add_default_value()
        self.password = self.salted_password(self.password)

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        salted = hashlib.sha256((password + salt).encode('ascii')).hexdigest()
        return salted

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        if len(name) > 2 and not User.exist(username=name):
            # 错误，只应该 commit 一次
            # u = User.new(**form)
            # u.password = u.salted_password(pwd)
            # User.session.add(u)
            # User.session.commit()
            form = form.to_dict()
            u = User.new(**form)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        query = dict(
            username=form['username'],
            password=User.salted_password(form['password']),
        )
        e = User.exist(**query)
        if e:
            return User.one(**query)
        else:
            return None

    def update_password(self, form):
        old_pass = self.salted_password(form['old_pass'])
        if self.password == old_pass:
            return self.salted_password(form['new_pass'])
        else:
            return self.password

    def _init(self, form):
        self.username = form['username']
        self.password = form['password']
        self.user_role = form.get('user_role', UserRole.normal)
        self.signature = form['signature']
        self.image = form['image']
        return self

    @staticmethod
    def guest():

        form = dict(
            user_role=UserRole.guest,
            username='【访客】',
            password='【访客】',
            signature=' 访客，你好~~ ',
            image='/images/default.jpg'
        )
        u = User()
        u = u._init(form)
        return u

    def is_guest(self):
        if self.user_role == UserRole.guest:
            return True
        else:
            return False
