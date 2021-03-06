from flask import (
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.messages import Messages
from models.user import User
from routes import current_user

from models.reply import Reply


main = Blueprint('coolwater_reply', __name__)


def users_from_content(content):
    # 内容 @123 内容
    # 如果用户名含有空格 就不行了 @name 123
    # 'a b c' -> ['a', 'b', 'c']
    parts = content.split()
    users = []

    for p in parts:
        if p.startswith('@'):
            username = p[1:]
            u = User.one(username=username)
            print('users_from_content <{}> <{}> <{}>'.format(username, p, parts))
            if u is not None:
                users.append(u)

    return users


def send_mails(sender, receivers, content):
    print('send_mail', sender, receivers, content)
    for r in receivers:
        form = dict(
            title='你被 {} AT 了'.format(sender.username),
            content=content,
            sender_id=sender.id,
            receiver_id=r.id
        )
        Messages.new(**form)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()

    content = form['content']
    users = users_from_content(content)
    send_mails(u, users, content)
    form = form.to_dict()
    m = Reply.new(form, user_id=u.id)
    return redirect(url_for('coolwater_topic.detail', id=m.topic_id))

