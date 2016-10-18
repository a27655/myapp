import hashlib
import os

from . import ModelMixin
from . import db


class Follow(db.Model, ModelMixin):
    __tablename__ = 'follows'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer, default=0)
    #外键（这个follow model类似Message）
    star_id = db.Column(db.String(), db.ForeignKey('users.id'))
    fans_id = db.Column(db.String(), db.ForeignKey('users.id'))

    def __init__(self, form):
        self.created_time = self.time()
        self.star_id = form.get('user_id', '')


