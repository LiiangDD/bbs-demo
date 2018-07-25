from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.board import Board
from routes import current_user

from models.topic import Topic


main = Blueprint('coolwater_topic', __name__)


@main.route("/")
def index():
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)
    bs = Board.all()
    u = current_user()
    return render_template("topic/index.html", ms=ms, u=u, bs=bs, bid=board_id)


@main.route('/<int:id>')
def detail(id):
    # http://localhost:3000/topic/1
    m = Topic.get(id)
    u = current_user()
    # 不应该放在路由里面
    # m.views += 1
    # m.save()

    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m, u=u)


@main.route("/add", methods=["POST"])
def add():
    form = request.form.to_dict()
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/new")
def new():
    bs = Board.all()
    return render_template("topic/new.html", bs=bs)

