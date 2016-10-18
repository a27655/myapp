from . import ModelMixin
from . import db


class Weibo(db.Model, ModelMixin):
    __tablename__ = 'weibos'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    weibo = db.Column(db.String())
    created_time = db.Column(db.String(), default=0)
    comments_num = db.Column(db.Integer, default=0)
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # 关系
    comments = db.relationship('Comment', backref='weibo', foreign_keys='Comment.weibo_id')

    def __init__(self, form):

        self.weibo = form.get('weibo', '')

        self.created_time = self.time()
        self.comments_num = 0

    def valid(self):
        return len(self.weibo) > 2 and len(self.weibo) < 140



    def error_message(self):
        if len(self.weibo) <= 2:
            return '微博太短了，至少要 3 个字符'
        elif len(self.weibo) >= 140:
            return '微博不能大于140个字符'

    def json(self):
        """
        id = db.Column(db.Integer, primary_key=True)
        weibo = db.Column(db.String())
        name = db.Column(db.String())
        created_time = db.Column(db.String(), default=0)


        i.comment = i.comments()
        for j in i.comment:
            j.avatar = j.get_avatar()
        i.comments_num = len(i.comment)
        i.avatar = i.get_avatar()

        """
        d = dict(
            id=self.id,
            weibo=self.weibo,
            name=self.user.username,
            created_time=self.created_time,
            comments_num=len(self.comments),
            avatar = self.user.avatar,
            username = self.user.username
        )
        # print('看看comments_num:', d['comments_num'])
        return d




