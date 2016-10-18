from functools import wraps

from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for
from flask import abort

from models.user import User

def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u
    else:
        nimy = User.query.get(int(-1))
        return nimy


