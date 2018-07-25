import functools

from flask import (
        session,
        redirect,
        url_for,
)

from models.user import User
from utils import log


def current_user():
    uid = session.get('user_id', '')
    print('session_get', uid)
    if uid:
        u = User.one(id=uid)
        return u
    else:
        return User.guest()


def login_required(route_function):
    @functools.wraps(route_function)
    def f():
        log('login_required')
        u = current_user()
        if u.is_guest():
            log('游客用户')
            return redirect(url_for('index.login_view'))
        else:
            log('登录用户', route_function)
            return route_function()

    return f


