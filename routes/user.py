from flask import (
    request,
    redirect,
    url_for,
    Blueprint,
    render_template,
    session,
)

from models.user import User
from models.reply import Reply
from models.topic import Topic
from routes import current_user

main = Blueprint('coolwater_user', __name__)


@main.route("/<username>", methods=["GET"])
def index(username):
    if User.guest().username != username:
        user_id = request.args['user_id']
        u = User.one(id=user_id)
        topics = Topic.all(user_id=u.id)
        replys = Reply.all()
        topics_reply = []
        for r in replys:
            topics_reply.append(Topic.one(id=r.topic_id))
        return render_template("user_history.html", u=u, topics=topics, topics_reply=topics_reply)
    else:
        return redirect(url_for('index.login_view'))


@main.route("/setting", methods=["POST"])
def setting():
    form = request.form.to_dict()
    u = current_user()
    # 旧密码一致 更新密码
    form['password'] = u.update_password(form)
    print('setting_form_dict', form)
    print('setting_salted_pass', u.update_password(form))
    User.update(id=u.id, **form)
    return redirect(url_for('index.profile'))

