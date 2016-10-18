from models.weibo import Weibo
from models.comment import Comment
from routes import *


main = Blueprint('weibo', __name__)


def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if int(current_user().id) < 0:
            return render_template('user_login.html', message='您尚未登录，无法使用博客')
        elif int(current_user().id) != int(1) :
            abort(401)
        return f(*args, **kwargs)

    return function


def admin_required_login(f):
    @wraps(f)
    def function(*args, **kwargs):
        if int(current_user().id) < 0:
            return render_template('user_login.html', message='您尚未登录，无法评论')
        return f(*args, **kwargs)

    return function




@main.route('/')
def index():
    u = current_user()
    weibo_u = User.query.get(int(1))
    weibo_list = weibo_u.weibos
    return render_template('weibo_index.html', weibos=weibo_list, user=u)


@main.route('/add', methods=['POST'])
@admin_required
def add():
    form = request.form
    u = current_user()
    t = Weibo(form)
    t.user = u
    if t.valid():
        t.save()
    return redirect(url_for('.index'))


@main.route('/comment', methods=['POST'])
@admin_required_login
def comment():
    form = request.form
    wid = form.get('weibo_id')
    w = Weibo.query.get(wid)
    u = current_user()
    c = Comment(form)
    c.user = u
    c.weibo_id = wid
    w.comments_num = len(w.comments)
    if c.valid(w):
        c.save()
        w.comments_num = len(w.comments)
    return redirect(url_for('.index'))


@main.route('/delete/<int:weibo_id>')
@admin_required
def delete(weibo_id):
    w = Weibo.query.get(weibo_id)
    w.delete()
    return redirect(url_for('.index'))


@main.route('/update', methods=['POST'])
@admin_required
def update():
    form = request.form
    u = current_user()
    wid = form.get('weibo_id', '')
    w = Weibo.query.get(id=wid)
    w.created_time = w.time()
    w.weibo = form.get('weibo','')
    if w.valid():
        w.save()
    return redirect(url_for('.index'))
