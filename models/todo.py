from . import ModelMixin
from . import db


class Todo(db.Model, ModelMixin):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    tag = db.Column(db.String())
    #外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, form):
        self.task = form.get('task', '')
        self.created_time = self.time()
        self.tag='unfinished'
    def valid(self):
        if len(self.task) == 0:
            return False
        else:
            return True

    def json(self):
        d = dict(
            id=self.id,
            task=self.task,
            created_time = self.created_time
        )
        return d

    def error_message(self):
        if len(self.task) <= 0:
            return 'todo不能输入为空'
        elif len(self.task) > 50:
            return '你的todo太长了'


