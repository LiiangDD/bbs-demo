from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import secret

from models.base_model import db, SQLBase
from models.board import Board
from models.reply import Reply
from models.topic import Topic
from models.user import User
from models.messages import Messages
from utils import log


from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.user import main as user_routes
from routes.message import main as mail_routes, mail

def count(input):
    log('count using jinja filter')
    return len(input)


def configured_app():
    app = Flask(__name__)

    app.secret_key = secret.secret_key
    register_routes(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@localhost/{}?charset=utf8mb4'.format(
        secret.mysql_password, secret.project_name
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    mail.init_app(app)

    return app


def register_routes(app):

    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(user_routes, url_prefix='/user')
    # app.register_blueprint(board_routes, url_prefix='/board')
    app.register_blueprint(mail_routes, url_prefix='/mail')

    app.template_filter()(count)

    admin = Admin(app, name='coolwater_bbs_demo', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Topic, db.session))
    admin.add_view(ModelView(Reply, db.session))
    admin.add_view(ModelView(Board, db.session))
    admin.add_view(ModelView(Messages, db.session))


if __name__ == '__main__':
    app = configured_app()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=3000,
    )
    app.run(**config)
