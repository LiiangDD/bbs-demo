import os
import uuid

from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    send_from_directory)

from models.user import User
from models.user_role import UserRole
from routes import current_user

main = Blueprint('index', __name__)

"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    u = current_user()
    return render_template("index.html", u=u)


@main.route("/login/view")
def login_view():
    u = current_user()
    return render_template("login.html", u=u)


@main.route("/register", methods=['POST'])
def register():
    # form = request.args
    form = request.form
    # 用类函数来判断
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    print('enter_login')
    form = request.form
    u = User.validate_login(form)
    if u is None:
        # 转到 topic.index 页面
        print('login_None')
        return redirect(url_for('coolwater_topic.index'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        print('login_session', session['user_id'])
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('coolwater_topic.index'))


@main.route('/profile')
def profile():
    u = current_user()
    if u.user_role is UserRole.guest:
        return redirect(url_for('index.login_view'))
    else:
        return render_template('profile.html', u=u)


@main.route('/user/<int:id>')
def user_detail(id):
    u = User.find(id)
    if u is None:
        abort(404)
    else:
        return render_template('profile.html', u=u)


@main.route('/image/add', methods=['POST'])
def avatar_add():
    file = request.files['avatar']

    # ../../root/.ssh/authorized_keys
    # filename = secure_filename(file.filename)
    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)

    u = current_user()
    User.update(u.id, image='/images/{}'.format(filename))

    return redirect(url_for('.profile'))


@main.route('/images/<filename>')
def image(filename):
    # 不要直接拼接路由，不安全，比如
    # open(os.path.join('images', filename), 'rb').read()
    return send_from_directory('images', filename)


@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index.login_view'))


@main.app_context_processor
def base_inject_user():
    return dict(base_inject_user=current_user())
