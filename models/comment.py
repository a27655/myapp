from . import ModelMixin
from . import db


class Comment(db.Model, ModelMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    created_time = db.Column(db.Integer, default=0)
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    weibo_id = db.Column(db.Integer, db.ForeignKey('weibos.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = self.time()

    def valid(self, w):
        if len(self.content) == 0:
            print('len(self.content):', len(self.content))
            return False

        else:
            cn = int(w.comments_num)
            cn += 1
            w.comments_num = cn
            w.save()
            return True

    def error_message(self):
        if len(self.content) == 0:
            return '评论不能为空'
        elif len(self.content) >= 50:
            return '评论最多不能多于50个字'

    def json(self):

        c = dict(
            id=self.id,
            content=self.content,
            name=self.user.username,
            created_time=self.created_time,
            avatar = self.user.avatar,


        )
        return c



