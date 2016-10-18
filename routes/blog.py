from models.blog import Blog
from models.comment import Comment
from routes import *


main = Blueprint('blog', __name__)


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
    blog_u = User.query.get(int(1))
    blog_list = blog_u.blogs
    return render_template('blog_index.html', blogs=blog_list, user=u)


@main.route('/add', methods=['POST'])
@admin_required
def add():
    form = request.form
    u = current_user()
    b = Blog(form)
    b.user = u
    if b.valid():
        b.save()
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 todo
    return redirect(url_for('.index'))




@main.route('/delete/<int:blog_id>')
@admin_required
def delete(blog_id):
    b = Blog.query.get(blog_id)
    b.delete()
    u = current_user()
    return redirect(url_for('.index'))


@main.route('/edit/<int:blog_id>')
@admin_required
def edit(blog_id):
    return render_template('blog_edit.html', blog_id=blog_id)


@main.route('/update', methods=['POST'])
def update():
    form = request.form
    u = current_user()
    b_id = form.get('blog_id', '')
    b = Blog.query.get(id=b_id)
    b.created_time = b.time()
    b.title = form.get('title', '')
    b.content = form.get('content','')
    if b.valid():
        b.save()
    return redirect(url_for('.index'))

@main.route('/cell/<int:blog_id>')
def cell(blog_id):
    blog = Blog.query.get(blog_id)
    return render_template('blog_cell.html', b=blog)


@main.route('/comment', methods=['POST'])
@admin_required_login
def comment():
    form = request.form

    bid = form.get('blog_id')
    b = Blog.query.get(bid)
    u = current_user()
    c = Comment(form)
    c.user = u
    c.blog = b
    b.comments_num = len(b.comments)
    if c.valid(w=b):
        c.save()
        b.comments_num = len(b.comments)
    return render_template('blog_cell.html', b=b)
