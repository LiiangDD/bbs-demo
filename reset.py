from models.base_model import reset_database
from models.board import Board
from models.messages import Messages
from models.reply import Reply
from models.topic import Topic
from models.user import User


def generate_fake_data():
    u = User.new(
        username='test1',
        password='123'
    )

    b = Board.new(
        title='demo'
    )
    Board.new(
        title='demo2'
    )

    with open('markdown_demo.md', encoding='utf8') as f:
        content = f.read()
    form = dict(
        title='markdown demo',
        content=content,
        board_id=b.id
    )
    Topic.new(form, u.id)
    form = dict(
        title='板块测试 demo2',
        content='**biu biu biu**',
        board_id='2'
    )
    Topic.new(form, u.id)
    form = dict(
        topic_id=1,
        content='**hello world**',
    )

    u = User.new(
        username='test2',
        password='123',
    )

    Reply.new(form, u.id)
    form = dict(
        topic_id=2,
        content='**hello world2**',
    )
    Reply.new(form, u.id)

    form = dict(
        title='hey',
        content='happy',
        sender_id=1,
        receiver_id=2
    )
    Messages.new(**form)


def main():
    # app = configured_app()
    # with app.app_context():
    reset_database()
    generate_fake_data()


if __name__ == '__main__':
    main()
