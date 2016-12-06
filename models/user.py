import hashlib
import os
from flask import session

from . import ModelMixin
from . import db


class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    avatar = db.Column(db.String(500))
    created_time = db.Column(db.Integer, default=0)
    qq = db.Column(db.String(20))
    email = db.Column(db.String(50))
    # 签名
    sign = db.Column(db.String(500))
    captcha = db.Column(db.String(20))
    # 下面定义关系
    comments = db.relationship('Comment', backref='user', foreign_keys='Comment.user_id')
    blogs = db.relationship('Blog', backref='user', foreign_keys='Blog.user_id')
    todos = db.relationship('Todo', backref='user', foreign_keys='Todo.user_id')
    weibos = db.relationship('Weibo', backref='user', foreign_keys='Weibo.user_id')
    asstars = db.relationship('Follow', backref='star', foreign_keys='Follow.star_id')
    asfans = db.relationship('Follow', backref='fans', foreign_keys='Follow.fans_id')

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.created_time = self.time()
        self.avatar = form.get('avatar', '/static/img/3.jpg')
        self.qq = form.get('qq', '他还没来的及输入他的QQ')
        self.email = form.get('email', '他还没来得及输入他的Email')
        self.sign = form.get('sign', '他还没有签名')
        self.captcha = form.get('captcha', '')
    # 验证注册用户的合法性的
    def valid(self):
        u = User.query.filter_by(username=self.username).first()
        valid_username = User.query.filter_by(username=self.username).first() == None
        valid_username_len = len(self.username) >= 6
        valid_password_len = len(self.password) >= 6
        valid_captcha = self.captcha == '吃瓜群众'
        msgs = ['注册成功，请登录']
        if not valid_username:
            message = '用户名已经存在'
            msgs.append(message)
        elif not valid_username_len:
            message = '用户名长度必须大于等于 6'
            msgs.append(message)
        elif not valid_password_len:
            message = '密码长度必须大于等于 6'
            msgs.append(message)
        elif not valid_captcha:
            message = '验证码必须输入 ‘吃瓜群众’'
            msgs.append(message)
        status = valid_username and valid_username_len and valid_password_len and valid_captcha
        return status, msgs

    # 验证用户登录
    def validate_login(self, form):
        username = form.get('username')
        password = form.get('password')
        username_equals = username == self.username
        password_equals = password == self.password
        if username_equals and password_equals:
            status = True
            msg = '登录成功'
        else:
            status = False
            msg = '用户名或密码错误'
        return status, msg


    def update_valid(self, cu):
        u = User.query.filter_by(username=self.username).first()

        if u is not None:
            if u.username == cu.username:
                valid_username = True
            else:
                valid_username = False

        if u is None:
            valid_username = True

        valid_username_len = len(self.username) >= 6
        valid_password_len = len(self.password) >= 6
        valid_captcha = self.captcha == '吃瓜群众'
        msgs = ['资料修改成功']
        if not valid_username:
            message = '用户名已经存在'
            msgs.append(message)
        elif not valid_username_len:
            message = '用户名长度必须大于等于 6'
            msgs.append(message)
        elif not valid_password_len:
            message = '密码长度必须大于等于 6'
            msgs.append(message)
        elif not valid_captcha:
            message = '验证码必须输入 ‘吃瓜群众’'
            msgs.append(message)
        status = valid_username and valid_username_len and valid_password_len and valid_captcha
        return status, msgs




