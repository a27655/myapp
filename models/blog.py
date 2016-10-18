from . import ModelMixin
from . import db


class Blog(db.Model, ModelMixin):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(10000))
    created_time = db.Column(db.Integer, default=0)
    updated_time = db.Column(db.Integer, default=0)
    comments_num = db.Column(db.Integer, default=0)
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # 关系
    comments = db.relationship('Comment', backref='blog', foreign_keys='Comment.blog_id')

    def __init__(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.created_time = self.time()
        self.comments_num = len(self.comments)
        self.updated_time = self.created_time

    def valid(self):
        return len(self.title) > 5 and len(self.content) > 10
