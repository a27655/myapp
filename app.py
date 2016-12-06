from flask import Flask
from flask import render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


from models import db

from models.todo import Todo
from models.user import User
from models.weibo import Weibo
from models.blog import Blog
from models.comment import Comment
from models.follow import Follow


from routes.todo import main as routes_todo
from routes.api import main as routes_api
from routes.weibo import  main as routes_weibo
from routes.user import  main as routes_user
from routes.blog import  main as routes_blog
from routes.follow import main as routes_follow


# from routes.admin_views import admin
# from routes.chest_views import chest
# from routes.question_views import question
# from routes.topic_views import topic

app = Flask(__name__)
db_path = 'myapp.sqlite'
manager = Manager(app)


def configure_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = 'poipyqwetrlkjhsadfzxcv'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:yang@localhost/myapp'
    db.init_app(app)
    app.register_blueprint(routes_todo, url_prefix='/todo')
    app.register_blueprint(routes_api, url_prefix='/api')
    app.register_blueprint(routes_weibo, url_prefix='/weibo')
    app.register_blueprint(routes_blog, url_prefix='/blog')
    app.register_blueprint(routes_user)
    app.register_blueprint(routes_follow, url_prefix='/follow')

def configured_app():
    configure_app()
    return app


# 自定义的命令行命令用来运行服务器
@manager.command
def server():
    app = configured_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=5000,
    )
    app.run(**config)


def configure_manager():
    """
    这个函数用来配置命令行选项
    """
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    configure_manager()
    configure_app()
    manager.run()
